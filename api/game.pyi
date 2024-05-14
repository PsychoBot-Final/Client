import numpy as np

def is_compass_set(screen_shot, direction: str) -> bool:
    """ Checks what direction the compass is sest to """
    ...

def set_compass_direction(script, direction: str) -> None:
    """ sets compass direction to specified direction """
    ...

def move_camera_up(script) -> None:
    """ Moves the camera up. """
    ...

def is_setting_tab_open(screen_shot) -> bool:
    """ Returns true is setting tab is open. """
    ...

def open_setting_tab(script, screen_shot) -> None:
    """ Opens the setting tab. """
    ...

def is_setting_menu_open(screen_shot) -> bool:
    """ Returns true if the setting menu is open """
    ...

def open_setting_menu(script, screen_shot) -> None:
    """ Click the all setting button and opens the setting menu. """
    ...

def search_setting(script, search_text) -> None:
    """ Search for a specific setting in the setting menu search bar. """
    ...

def is_zoom_text_visible(screen_shot) -> bool:
    """ Returns true if the text 'zoom' is visible in the search bar. """
    ...

def is_bright_text_visible(screen_shot) -> bool:
    ...


def is_ground_text_visible(screen_shot) -> bool:
    ...


def is_roof_text_visible(screen_shot) -> bool:
    ...


def is_function_text_visible(screen_shot) -> bool:
    ...


def is_search_bar_empty(screen_shot) -> bool:
    ...


def is_screen_brightness_3(screen_shot) -> bool:
    ...


def is_camera_zoom_2(screen_shot) -> bool:
    """ Returns true if the camera zoom is set to the second notch """
    ...


def is_minimap_zoom_1(screen_shot) -> bool:
    """ Returns true if the minimap zoom is set to the first notch """
    ...


def is_minimap_zoom_3(screen_shot) -> bool:
    """ Returns true if the minimap zoom is set to the third notch """
    ...


def is_minimap_zoom_button_visible(screen_shot) -> bool:
    """ Returns true if the minimap zoom button is visible """
    ...


def is_drop_activated(screen_shot) -> int:
    """ Returns True if the drop settings is activated. """
    ...


def is_drop_deactivated(screen_shot) -> int:
    """ Returns True if the drop settings is activated. """
    ...


def activate_drop(script, screen_shot) -> None:
    """ Click to activate drop setting. """
    ...


def deactivate_drop(script, screen_shot) -> None:
    """ Click to deactivate the drop setting. """
    ...


def is_function_mode_tap_to_drop(screen_shot) -> bool:
    """ Returns true if the function mode set to tap to drop """
    ...


def is_function_drop_down_visible(screen_shot) -> bool:
    """ Returns true if function mode dropdown is visible """
    ...


def is_show_function_button_disabled(screen_shot) -> bool:
    ...


def is_show_function_button_enabled(screen_shot) -> bool:
    ...


def is_ground_item_enabled(screen_shot) -> bool:
    ...


def is_ground_item_disabled(screen_shot) -> bool:
    ...


def is_hide_roof_enabled(screen_shot) -> bool:
    ...


def is_hide_roof_disabled(screen_shot) -> bool:
    ...

def get_minimap_image(screen_shot) -> np.ndarray:
    """ Returns cropped circle of minimap.

    Args:
        screen_shot (np.ndarray): Instance of screenshot.

    Returns:
        np.ndarray: Cropped minimap image.
    """
    ...

def is_app_open(script) -> bool:  # sourcery skip: raise-specific-error
    """ Checks the running package on bluestacks using ADB and checks if it is OSRS.

    Args:
        script (Script): Instance of script running.

    Raises:
        Exception: If ADB is not connected.

    Returns:
        bool: Returns True if OSRS is running, else False.
    """
    ...