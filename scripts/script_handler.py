import json
from utils import get_resource_path
from settings import RUN_LOCAL, WEB_SERVER_URL


scripts = {}

def fetch_script(name: str, module: str, _class: str, version: float) -> None:
    global scripts
    if name in scripts:
        version = float(scripts[name]['version'])
    else:
        ...


available_scripts = []

def get_script_names() -> list:
    if RUN_LOCAL:
        with open(get_resource_path('scripts/local/scripts.json'), 'r') as f:
            return list(json.load(f).keys())
    else:
        return get_available_scripts()

def set_available_scripts(data: list) -> None:
    global available_scripts
    available_scripts = data

def get_available_scripts() -> list:
    return available_scripts