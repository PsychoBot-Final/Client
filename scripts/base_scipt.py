import os
import cv2 as cv
import torch
from win_cap import WinCap
from threading import Thread, Event
from uiautomator2 import Device
from abc import ABC, abstractmethod


class ScriptThread:
    def __init__(self, func) -> None:
        self.stop_event = Event()
        self.script_thread = Thread(target=func)
        self.script_thread.daemon = True

    def start(self) -> None:
        self.script_thread.start()

    def stop(self) -> None:
        self.stop_event.set()
        self.script_thread.join()

    def is_running(self) -> bool:
        return not self.stop_event.is_set()

class BaseScript(ABC):
    def __init__(
        self,
        adb_device: Device,
        script_name: str,
        window_name: str,
        templates_path: str=None,
        model_path: str=None,
    ) -> None:
        self.adb_device = adb_device
        self.script_name = script_name
        self.window_name = window_name
        self.templates = {}
        self.model = None
        self.win_cap = WinCap(self.window_name)
        self.templates_path = templates_path
        self.model_path = model_path
        self.is_paused = False
        self.script_threads = []
        self.main_thread = ScriptThread(self.run)
        self.script_threads.append(self.main_thread)

    @abstractmethod
    def start(self) -> bool:
        ...
    
    @abstractmethod
    def run(self) -> None:
        ...

    @abstractmethod
    def stop(self) -> None:
        ...

    def pause_script(self) -> None:
        self.is_paused = not self.is_paused

    def is_script_paused(self) -> bool:
        return self.is_paused

    def new_script_thread(self, func) -> ScriptThread:
        script_thread = ScriptThread(func)
        self.script_threads.append(script_thread)
        return script_thread
    
    def kill_script_threads(self) -> None:
        for thread in self.script_threads:
            thread.stop()

    def load_model(self, model_path=None, multi_label=False) -> None:
        path_to_use = model_path if model_path is not None else self.model_path
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=path_to_use, force_reload=True)
        try:
            self.model.cuda()
        except Exception as _:
            ...
        self.model.multi_label = multi_label
        return self.model
    
    def load_templates(self, templates_path=None) -> None:
        path_to_use = templates_path if templates_path is not None else self.templates_path
        for t in os.listdir(path_to_use):
            name, extension = os.path.splitext(t)
            if extension.lower() in ['.png', '.jpg', '.bmp']:
                template_path = os.path.join(path_to_use, t)
                if name not in self.templates:
                    self.templates[name] = cv.imread(template_path, cv.IMREAD_UNCHANGED)
        return self.templates