from threading import Thread, Event
from uiautomator2 import Device
from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor


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
    ) -> None:
        self.adb_device = adb_device
        self.script_name = script_name
        self.window_name = window_name
        self.is_paused = False
        self.script_threads = []
        self.main_thread = ScriptThread(self.run)
        self.script_threads.append(self.main_thread)

    @abstractmethod
    def start(self) -> None:
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
