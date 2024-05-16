import os
import sys
from constants import (
    BOT_DIR_PATH, 
    TEMPLATES_DIR_PATH
)

def init() -> None:
    try:
        os.makedirs(BOT_DIR_PATH, exist_ok=True)
    except OSError:
        print(f'Error while creating directory {BOT_DIR_PATH}...')

    try:
        os.makedirs(TEMPLATES_DIR_PATH, exist_ok=True)
    except OSError:
        print(f'Error while creating directory {TEMPLATES_DIR_PATH}...')

def get_resource_path(relative_path: str) -> str:
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)