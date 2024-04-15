import os
import re
from constants import (
    FILE_PATH,
    DISPLAY_NAME_PATTERN,
    ADB_PORT_PATTERN
)

def get_bluestacks_windows() -> dict:
    if not os.path.exists(FILE_PATH):
        return {}
    display_names = {}
    adb_ports = {}
    result = {}
    with open(FILE_PATH, 'r') as f:
        lines = f.readlines()
    for line in lines:
        match_display_name = re.search(DISPLAY_NAME_PATTERN, line)
        if match_display_name:
            instance_name, display_name = match_display_name.groups()
            display_names[instance_name] = display_name

        match_adb_port = re.search(ADB_PORT_PATTERN, line)
        if match_adb_port:
            instance_name, adb_port = match_adb_port.groups()
            adb_ports[instance_name] = adb_port

    for instance_name in display_names:
        if instance_name in adb_ports:
            result[display_names[instance_name]] = adb_ports[instance_name]
    
    return result

def get_adb_port_for_instance(
    instance_name: str
) -> int:
    """
    Returns ADB port for bluestacks instance.
    """
    return int(get_bluestacks_windows()[instance_name])
