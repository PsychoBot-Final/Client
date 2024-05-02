from tkinter import messagebox
from constants import LOCAL_HOST
from error_handler import ADBError
from uiautomator2 import Device, connect, ConnectError


adb_connections = set()

def is_adb_connected(window_name: str) -> bool:

    return window_name in adb_connections

def connect_to_window(window_name: str, port: int) -> Device:
    if is_adb_connected(window_name):
        raise ADBError(f'Connection already exists for {window_name}...', code=1)
    try:
        device = connect(f'{LOCAL_HOST}:{port}')
        device.app_current()
        new_adb_connection(window_name)
        return device
    except RuntimeError as _:
        raise ADBError(f'Failed to connect to {window_name} on port {port}...', code=2)

def new_adb_connection(window_name: str) -> None:
    adb_connections.add(window_name)

def close_adb_connection(window_name: str) -> None:
    if window_name not in adb_connections:
        raise ADBError(f'No existing connection found for {window_name}...', code=3)
    adb_connections.discard(window_name)