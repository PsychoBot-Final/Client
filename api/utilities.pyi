def load_templates(dir_name: str) -> dict:
    """
    The function `load_templates` loads image templates from a specified directory and returns them as a
    dictionary.

    Args:
      dir_name (str): The `dir_name` parameter in the `load_templates` function is a string that
    represents the name of the directory where the templates are located. This function loads image
    templates from the specified directory and returns a dictionary where the keys are the template
    names (without file extensions) and the values are the corresponding

    Returns:
      A dictionary containing template names as keys and corresponding image data loaded using OpenCV as
    values.
    """
    ...
    
def get_center_point(rect) -> tuple:
    """ Gets the center point of a OpenCV rectangle. """
    ...


def get_random_point(rect) -> tuple:
    """ gets a random point within the opencv rectangle. """
    ...

def crop_image_rect(image, x, y, x1, y1):
    """ Crops an OpenCV image using Pillow.

    Args:
        image (_type_): OpenCV image to crop.
        x1 (_type_): X-coordinate of the leftmost point.
        y1 (_type_): Y-coordinate of the topmost point.
        x2 (_type_): X-coordinate of the rightmost point.
        y2 (_type_): Y-coordinate of the bottommost point.

    Returns:
        _type_: OpenCV cropped image.
    """
    ...


def crop_image_circle(image, x, y, x1, y1):
    """ Crops a circle from an image using OpenCV.

    Args:
        image (_type_): Image to crop.
        left (_type_): X-coordinate of the leftmost point.
        top (_type_): Y-coordinate of the topmost point.
        right (_type_): X-coordinate of the rightmost point.
        bottom (_type_):Y-coordinate of the bottommost point.

    Returns:
        _type_: np.ndarray (OpenCV)
    """
    ...