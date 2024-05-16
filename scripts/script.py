import os
import torch
import cv2 as cv
from win_cap import WinCap
import customtkinter as ctk
from uiautomator2 import Device
from error_handler import ADBError
from abc import ABC, abstractmethod
from threading import Thread, Event
from constants import TEMPLATES_DIR_PATH
import logger_configs


class ScriptContainer:
    def __init__(self, version: float, file_name: str, module_class: str, source: str, model_path: str, templates_path: str) -> None:
        self.version = version
        self.file_name = file_name
        self.module_class = module_class
        self.source = source
        self.model_path = model_path
        self.templates_path = templates_path

class ScriptThread:
    def __init__(self, func) -> None:
        self.stop_event = Event()
        self.script_thread = Thread(target=func, daemon=True)

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
        id: int,
        adb_device: Device,
        script_name: str,
        window_name: str,
        parent,
        templates_path: str=None,
        model_path: str=None,
    ) -> None:
        self.id = id
        self.adb_device = adb_device
        self.script_name = script_name
        self.window_name = window_name
        self.parent = parent
        self.app = ctk.CTkToplevel(self.parent.frame)
        self.templates = {}
        self.model = None
        self.win_cap = WinCap(self.window_name)
        self.templates_path = templates_path
        self.model_path = model_path
        self.is_paused = False
        self.script_threads = []
        self.main_thread = ScriptThread(self.run)
        self.script_threads.append(self.main_thread)
        self.app.protocol("WM_DELETE_WINDOW", self.on_close)
        self.logger = logger_configs.get_script_logger(script_name)

    @abstractmethod
    def create_gui(self, parent: ctk.CTkFrame) -> None:
        ...

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
        self.logger.info(f'Attempting to pause/unpause script for script: {self.script_name} - Paused: {self.is_paused}')

    def is_script_paused(self) -> bool:
        return self.is_paused

    def new_script_thread(self, func) -> ScriptThread:
        script_thread = ScriptThread(func)
        self.script_threads.append(script_thread)
        return script_thread

    def kill_script_threads(self) -> None:
        self.logger.info(f'Attempting to kill script threads for script: {self.script_name}')
        for thread in self.script_threads:
            thread.stop()

    def set_window_position(self, width, height):
        screen_width = self.app.winfo_screenwidth()
        screen_height = self.app.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.app.geometry(f"{width}x{height}+{x}+{y}")

    def on_close(self) -> None:
        self.parent.stop_script()
        self.close_gui()

    def close_gui(self) -> None:
        self.app.destroy()

    def send_adb_input(self, cmd: str) -> None:
        if not self.adb_device:
            self.logger.warning('ADB device is not registered.')
            raise ADBError('Device not registered...', code=5)
        self.adb_device.shell(cmd)

    def click_point(self, abs_x, abs_y) -> None:
        self.send_adb_input(f'input tap {abs_x} {abs_y}')

    def click_hold_point(self, abs_x: int, abs_y: int, duration: float) -> None:
        self.click_hold_swipe(abs_x, abs_y, abs_x, abs_y, duration)

    def click_hold_swipe(self, abs_x: int, abs_y: int, to_abs_x: int, to_abs_y: int, duration: float) -> None:
        self.send_adb_input(f'input touchscreen swipe {abs_x} {abs_y} {to_abs_x} {to_abs_y} {duration}')

    def send_keyboard_text(self, text: str, click_enter: bool=False) -> None:
        self.send_adb_input(
            f'input text "{text}"'
            if not click_enter
            else f'input text "{text}" && input keyevent KEYCODE_ENTER'
        )

    def send_keyboard_input(self, type: str) -> None:
        types = {
            'SPACE': 'KEYCODE_SPACE',
            'ESCAPE': 'KEYCODE_ESCAPE',
            'BACKSPACE': 'KEYCODE_DEL'
        }
        self.send_adb_input(f'input keyevent {types[type]}')

    def load_model(self, model_path=None, multi_label=False) -> None:
        path_to_use = model_path if model_path is not None else self.model_path
        self.logger.info(f'Loading model from: {path_to_use}')
        self.model = torch.hub.load('ultralytics/yolov5', 'custom', path=path_to_use, force_reload=True)
        try:
            self.model.cuda()
        except Exception as _:
            self.logger.info(f'Cannot load CUDA for model: {path_to_use}')
        self.model.multi_label = multi_label
    
    def load_templates(self, dir_name: str=None) -> None:
        path_to_use = f'{TEMPLATES_DIR_PATH}/{dir_name}' if dir_name is not None else self.templates_path
        self.logger.info(f'Loading templates from: {path_to_use}')
        for t in os.listdir(path_to_use):
            name, extension = os.path.splitext(t)
            if extension.lower() in ['.png', '.jpg', '.bmp']:
                template_path = os.path.join(path_to_use, t)
                if name not in self.templates:
                    self.templates[name] = cv.imread(template_path, cv.IMREAD_UNCHANGED)
        return self.templates
