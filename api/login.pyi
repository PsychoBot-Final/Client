from uiautomator2 import Device


def is_osrs_open(device: Device) -> bool:
    """
    This Python function checks if the current activity on a device is the Old School RuneScape app.
    
    Args:
      device (Device): Device is an object representing a device on which an application is running.
    
    Returns:
      The function `is_osrs_open` is returning a boolean value based on whether the current activity of
    the provided `device` is 'com.jagex.android.MainActivity'.
    """
    ...

def start_osrs_app(device: Device) -> None:
    """
    The function `start_osrs_app` is used to start the Old School RuneScape app on a specified device.
    
    Args:
      device (Device): A device object representing the mobile device on which the Old School RuneScape
    (OSRS) app will be started.
    """
    ...

def is_osrs_app_installed(device: Device) -> bool:
    """
    The function `is_osrs_app_installed` checks if the Old School RuneScape app is installed on a given
    device.
    
    Args:
      device (Device): Device is an object representing a device (e.g., smartphone, tablet, etc.) on
    which apps can be installed and run.
    
    Returns:
      The function `is_osrs_app_installed` takes a `Device` object as input and returns a boolean value
    indicating whether the Old School RuneScape app is installed on the device. It checks the app list
    on the device for the package name 'com.jagex.oldscape.android' and returns True if the app is
    installed, and False if it is not installed.
    """
    ...

def click_play_now_btn(script, screen_shot) -> None:
    """ click Login on the first login page of the game """
    ...


def click_tap_here_btn(script, screen_shot) -> None:
    """ click Login on the second login page of the game """
    ...


def click_ok_btn(script, screen_shot) -> None:
    """ click ok btn on the first login page of the game """
    ...


def close_osrs_app(script) -> None:
    ...


def is_logged_in(screen_shot) -> bool:
    ...


def login(script, screen_shot) -> None:
    """ detects if logged out and logs in to the game. """
    ...


def logout(script, screen_shot) -> None:
    """logs out of game"""
    ...