import mouse # type: ignore
import cv2 as cv
from time import sleep
from uiautomator2 import Device
from scripts.script import BaseScript


class SeersWoodcutter(BaseScript):
    def __init__(self, adb_device: Device, script_name: str, window_name: str, templates_path: str = None, model_path: str = None) -> None:
        super().__init__(adb_device, script_name, window_name, templates_path, model_path)

    def start(self) -> None:
        # self.load_templates()
        self.load_model(model_path='./scripts/local/models/seers_woodcutter.pt')
        self.main_thread.start()
        return True

    def run(self) -> None:
        while self.main_thread.is_running():
            if self.is_script_paused():
                sleep(1)
                continue
            screenshot = self.win_cap.get_screenshot()
            if screenshot is None:
                continue
            self.click_point(1, 1)
            sleep(1)

    def stop(self) -> None:
        self.kill_script_threads()