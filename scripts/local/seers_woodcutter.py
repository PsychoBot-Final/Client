import mouse
from time import sleep
from uiautomator2 import Device
from scripts.base_scipt import BaseScript


class SeersWoodcutter(BaseScript):
    def __init__(self, adb_device: Device, script_name: str, window_name: str) -> None:
        super().__init__(adb_device, script_name, window_name)

    def start(self) -> None:
        self.main_thread.start()

    def run(self) -> None:
        while True:
            mouse.click()
            sleep(1)

    def stop(self) -> None:
        self.kill_script_threads()