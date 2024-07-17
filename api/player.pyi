from typing import Union, List, Tuple

def is_point_in_bounds(point: Tuple[int, int], bounds: Union[List[tuple[int, int, int, int]], Tuple[int, int, int, int]]) -> bool:
    """
    The function `is_point_in_bounds` checks if a given point is within the specified bounds.
    
    Args:
      point (Tuple[int, int]): The `point` parameter is a tuple containing the x and y coordinates of a
    point.
      bounds (Union[List[tuple[int, int, int, int]], Tuple[int, int, int, int]]): The `bounds` parameter
    in the `is_point_in_bounds` function can be either a list of tuples or a single tuple. Each tuple in
    the list or the single tuple represents a bounding box in the format (x, y, width, height). The
    function checks if the given `point`
    
    Returns:
      The function `is_point_in_bounds` returns a boolean value, either `True` if the given point is
    within the specified bounds, or `False` if it is not.
    """
    ...

def player_is_moving(screen_shot, min_delay: float) -> bool:
    """ Returns true if flag is detected on minimap.

    Args:
        screen_shot (np.ndarray): Instance of opencv screen shot.
        min_delay (float): Delay before checking for flag on minimap.

    Returns:
        bool: True if flag detected on minimap, else False.
    """
    ...

def get_point_on_screen() -> tuple:
    """
    The function `get_point_on_screen` returns a tuple containing the coordinates (450, 274).
    
    Returns:
      A tuple containing the coordinates (450, 274) is being returned.
    """
    ...

def distance_from(x, y) -> float:
    """
    The function calculates the distance between the coordinates (450, 274) and the input coordinates
    (x, y).
    
    Args:
      x: The `x` parameter represents the x-coordinate of a point in a two-dimensional plane.
      y: The `y` parameter in the `distance_from` function represents the y-coordinate of a point in a
    two-dimensional plane.
    
    Returns:
      The function `distance_from` is returning the distance between the point (450, 274) and the point
    (x, y).
    """
    ...

def get_distance(x1, y1, x2, y2) -> float:
    """
    The function calculates the Euclidean distance between two points in a 2D plane.
    
    Args:
      x1: The parameter `x1` represents the x-coordinate of the first point in a 2D plane.
      y1: The `y1` parameter represents the y-coordinate of the first point in a 2D plane. It is used in
    the `get_distance` function to calculate the distance between two points given their x and y
    coordinates.
      x2: The `x2` parameter represents the x-coordinate of the second point in a 2D plane.
      y2: The `y2` parameter in the `get_distance` function represents the y-coordinate of the second
    point in a two-dimensional Cartesian coordinate system. This function calculates the Euclidean
    distance between two points in this coordinate system using the formula for distance between two
    points: √((x2 - x1
    
    Returns:
      The function `get_distance` returns the Euclidean distance between two points `(x1, y1)` and `(x2,
    y2)` in a 2D plane.
    """
    ...

def in_minimap_bounds(detected_rectangle) -> bool:
    """
    The function `in_minimap_bounds` checks if a point is within the bounds of a rectangle in a minimap.
    
    Args:
      detected_rectangle: The `detected_rectangle` parameter seems to be a list of rectangles, where
    each rectangle is represented by a tuple of four values: x-coordinate, y-coordinate, width, and
    height.
    
    Returns:
      The function is checking if a point (px, py) is inside the bounding rectangle defined by the
    coordinates (x, y, w, h) for each rectangle in the detected_rectangle list. The function returns
    True if the point is inside the rectangle, and False otherwise.
    """
    ...

def coords_in_bounds(detected_rectangle):
    """Detects if player minimap white dot is in openCV rectangle on the minimap."""
    ...

def click_point_in_bounds(script, detected_rectangle, crop_x, crop_y, click_x, click_y):
    """Clicks on a specific coordinate within the detected rectangle on the minimap."""
    ...

def distance_from_label(screen_shot, model, label, coord=(450, 274)) -> float:
    """ calculates a coordinates distance from a Yolov5 label by default player coords """
    ...

def is_run_full(screen_shot):
    ...

def is_run_activated(screen_shot):
    ...

def activate_run(script):
    ...
def get_hp(screen_shot):
    """
    Extracts the player's HP (hit points) from a given screenshot.

    Parameters:
    screen_shot (numpy.ndarray): The screenshot image from which to extract the player's HP.

    Returns:
    int or None: The extracted HP value as an integer if found, otherwise None.
    """
    ...

def find_and_group_characters(screen_shot, templates, threshold=0.95, max_gap=5):
    """
    Finds and groups numeric characters in a given screenshot based on provided templates.

    Parameters:
    screen_shot (numpy.ndarray): The screenshot image in which to find the characters.
    templates (dict): A dictionary where keys are characters and values are their respective template images.
    threshold (float): The matching threshold for template matching. Default is 0.95.
    max_gap (int): The maximum allowable gap between characters to consider them as part of the same number. Default is 5.

    Returns:
    str: The concatenated string of detected numeric characters.
    """
    ...

def is_player_moving_in_area(script, detected_rectangle, interval=0.1):
    """
    Continuously checks if a player is moving within a specified rectangular area.

    Args:
        detected_rectangle (tuple): A tuple containing the coordinates of the rectangle to detect player movement.
        interval (int, optional): Time interval in seconds between movement checks. Default is 1 second.

    Returns:
        bool: True if the player is moving within the specified area, False otherwise.
    """
    ...