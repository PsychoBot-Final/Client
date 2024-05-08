import numpy as np
import win32con
import win32gui
import win32ui
import threading


class WinCap:

    """ Capture screenshot of specified window. """

    # Thread lock
    lock = threading.Lock()

    # Top left positon of window.
    x, y = 0, 0

    # Cropped position of window.
    cropped_x, cropped_y = 0, 0

    # Width & Height of window from position.
    w, h = 0, 0

    def __init__(self, window_name=None) -> None:
        # Check if window_name exists, if not raise Exception.
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception(f'Window not found: {window_name}')
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]
        border_pixels = 0
        titlebar_pixels = 34
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

    def get_screenshot(self):
        self.lock.acquire()
        try:
            wDC = win32gui.GetWindowDC(self.hwnd)
            dcObj = win32ui.CreateDCFromHandle(wDC)
            cDC = dcObj.CreateCompatibleDC()
            dataBitMap = win32ui.CreateBitmap()
            dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
            cDC.SelectObject(dataBitMap)
            cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)
            signedIntsArray = dataBitMap.GetBitmapBits(True)
            img = np.frombuffer(signedIntsArray, dtype='uint8')
            img.shape = (self.h, self.w, 4)
            dcObj.DeleteDC()
            cDC.DeleteDC()
            win32gui.ReleaseDC(self.hwnd, wDC)
            win32gui.DeleteObject(dataBitMap.GetHandle())
            img = img[...,:3]
            return np.ascontiguousarray(img)
        finally:
            self.lock.release()

def list_window_names():
    """ List's all open window names. """
    all_windows = []
    def winEnumHandler(hwnd, ctx):
        if win32gui.IsWindowVisible(hwnd):
            name = str(win32gui.GetWindowText(hwnd))
            all_windows.append(name)
            # if name.startswith('OSRS #'):
            #     all_windows.append(win32gui.GetWindowText(hwnd))
            # print(hex(hwnd), win32gui.GetWindowText(hwnd))
    win32gui.EnumWindows(winEnumHandler, None)
    return all_windows