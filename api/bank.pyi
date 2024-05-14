def get_pin_number_bounds(screen_shot, pin_number: str) -> tuple:
  """
  The function `get_pin_number_bounds` finds the center point of a specified PIN number template
  within a given screen shot image.

  Args:
    screen_shot: The `screen_shot` parameter is likely a screenshot image of the screen where the PIN
  number is displayed. The function `get_pin_number_bounds` seems to be designed to find the bounding
  box or location of a specific PIN number within the screenshot image. The `pin_number` parameter is
  the specific PIN
    pin_number (str): The `pin_number` parameter in the `get_pin_number_bounds` function is a string
  that represents the PIN number for a bank account. This function is designed to find the bounding
  box of the specified PIN number on a given `screen_shot` image using a template matching technique.
  If a bounding box

  Returns:
    The function `get_pin_number_bounds` is returning a tuple containing the center point coordinates
  of the pin number rectangle found in the `screen_shot` image using the specified pin number
  template. If no matching rectangle is found, it returns `None`.
  """
  ...

def get_pin_stage(screen_shot) -> int:
  """
  The function `get_pin_stage` determines the stage of entering a PIN based on the appearance of
  specific templates in a screenshot.

  Args:
    screen_shot: The function `get_pin_stage(screen_shot)` is designed to determine which stage of
  entering a PIN code the user is currently at based on the provided `screen_shot`. The function uses
  template matching to identify specific elements on the screen that correspond to each stage of
  entering the PIN.

  Returns:
    The function `get_pin_stage` returns an integer value representing the stage of entering a PIN on
  a banking screen. The function checks for the presence of specific templates corresponding to each
  stage of entering the PIN (first, second, third, fourth) in the provided `screen_shot` image. If a
  template is found, the function returns the corresponding stage number (0 for first, 1 for second
  """
  ...

def get_bank_region(screen_shot):
  """
  This Python function extracts a specific region from a given screen shot based on the provided
  coordinates.

  Args:
    screen_shot: The `screen_shot` parameter is likely an image or a screenshot of a banking
  application interface. The `get_bank_region` function takes this screenshot as input and extracts a
  specific region from it based on the provided coordinates. The region extracted is a rectangular
  area starting from pixel coordinates (175, 100

  Returns:
    The function `get_bank_region` is returning a specific region of the `screen_shot` image. The
  region starts at coordinates (175, 100) and has a width of 333 pixels and a height of 494 pixels.
  """
  ...

def is_bank_open(screen_shot) -> bool:
  """
  The function `is_bank_open` checks if the bank is open based on the provided screen shot by
  identifying specific text elements.

  Args:
    screen_shot: The `screen_shot` parameter is likely a screenshot or image of a screen display,
  possibly from a banking application or website. This function `is_bank_open` seems to be checking if
  a bank is open based on the presence of certain text elements (like 'the_bank' and 'tab') in

  Returns:
    a boolean value indicating whether the bank is open or not. It checks for the presence of specific
  text elements related to the bank in the given screen shot and returns True if any of these elements
  are found, indicating that the bank is open.
  """
  ...

def deposit_all(script) -> None:
  ...

def exit_bank(script) -> None:
  ...

def is_quantity_set(screen_shot, amount: str) -> bool:
  """ Use amount as '1, 5, 10, all'. """

def is_quantity_x(screen_shot) -> bool:
  """ Returns True if the qunatity 'x' is selected. """

def is_bank_mode_set_to(screen_shot, mode: str) -> bool:
  """ Use mode as 'item' or 'note'. """

def set_quantity_to(script, screen_shot, amount: str) -> None:
  """ Sets the bank quanitity to "1, 5, 10, all".

  Args:
      script (script.Script): Instance of script invoking function.
      screen_shot (_type_): An instance of the script.
      amount (str): "1, 5, 10, all".
  """
  ...

def set_bank_mode_to(script, screen_shot, mode: str) -> None:
  """ Set banking mode to 'item' or 'note'. """
  ...

def withdraw_item(script, screen_shot, item, threshold) -> None:
  """ Withdraw a specified items from the bank. """
  ...