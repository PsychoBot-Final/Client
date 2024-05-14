def is_inventory_open(screen_shot) -> bool:
    """ Returns True if inventory tab is open. """
    ...

def open_inventory(script, screen_shot) -> None:
    """ Opens the inventory tab. """
    ...

def close_inventory(script, screen_shot) -> None:
    """Closes the inventory tab. """
    ...

def is_inventory_full_or_empty(screen_shot, is_full=True) -> bool:
    ...

def find_filled_slots(screen_shot, exclude_slot=None):
    """Returns a list of slot indices that contain items, excluding a specified slot if provided."""
    ...

def inventory_has_specific_item(screen_shot, item, threshold) -> bool:
    """ Returns true if the inventory has a specified item. """
    ...

def inventory_has_item_in_slot(screen_shot, item, threshold, slot_index) -> bool:
    """Returns True if the specified item is found in the given slot of the inventory."""
    ...

def find_item_slot(screen_shot, item, threshold) -> int:
    """Returns the index of the slot containing the specified item, or -1 if the item is not found."""
    ...

def find_item_slot_filtered_white(screen_shot, item, threshold) -> int:
    """Returns the index of the slot containing the specified item, or -1 if the item is not found."""
    ...

def is_inventory_has_item_except_excluded(screen_shot, exclude_slot_index=None) -> bool:
    ...

def inventory_has_multiple_items(screen_shot, threshold, *image_params) -> bool:
    """Returns True if inventory has at least one of the specified items."""
    """Usage: inventory_has_multiple_items(screen_shot, threshold, picture1, picture2, picture3...)"""
    ...

def click_inventory_item(script, screen_shot, item, threshold) -> None:
    """ Clicks a specified items in the inventory. """
    ...

def get_inventory_count_of_item(screen_shot, item, threshold) -> int:
    """ Returns the amount  """
    ...