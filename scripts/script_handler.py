import os
import sys
import json
import types
import requests
import importlib
import uiautomator2 as u2
from base64 import b64decode
from tkinter import messagebox
from constants import LOCAL_HOST
from utils import get_resource_path
from scripts.base_scipt import BaseScript
from settings import RUN_LOCAL, WEB_SERVER_URL
from scripts.script_container import ScriptContainer


running_scripts = {}
script_containers = {}
available_scripts = []
open_adb_connections = {}

def remove_script_container(name: str) -> None:
    global script_containers
    del script_containers[name]

def recieve_script_names(data) -> None:
    global available_scripts
    available_scripts = data

def receive_script(data) -> None:
    global script_containers
    name = data['name']
    script_data = data['data']
    script_data = str(script_data).split('|')
    source = b64decode(script_data[0]).decode('utf-8')
    model = b64decode(script_data[1])
    templates = b64decode(script_data[2])
    script_containers[name] = ScriptContainer(
        version=float(data['version']),
        file_name=data['file_name'],
        class_=data['class'],
        source=source,
        model=model,
        templates=templates
    )

def script_exists(name: str) -> bool:
    return name in script_containers

def get_script_container(name: str) -> ScriptContainer:
    return script_containers[name]

def get_script_version(name: str) -> float:
   url = f'http://{WEB_SERVER_URL}/version/{name}'
   request = requests.get(url)
   response = request.json()
   return float(response['version'])

def new_adb_connection(window_name: str) -> None:
    global open_adb_connections
    open_adb_connections[window_name] = True

def close_adb_connection(window_name: str) -> None:
    global open_adb_connections
    if window_name in open_adb_connections:
        del open_adb_connections[window_name]

def is_adb_connected(window_name: str) -> bool:
    return window_name in open_adb_connections\

def start_from_server(id: int, name: str, adb_port: int, window_name: str) -> bool:
    global running_scripts
    adb_device = None
    if not RUN_LOCAL:
        if not window_name in open_adb_connections:
            try:
                adb_device = u2.connect(f'{LOCAL_HOST}:{adb_port}')
                adb_device.app_current()
            except Exception as e:
                messagebox.showerror('Error', f'Error connecting to {window_name}!')
                return False
            new_adb_connection(window_name)
        else:
            messagebox.showerror('Error', 'Another script is already connected to this window!')
            return False
        container: ScriptContainer = script_containers[name]
        module_ = container.file_name
        class_ = container.class_
        source = str(container.source).encode('utf-8')
        model = container.model
        templates = container.templates

        script_module = types.ModuleType(module_)
        exec(source, script_module.__dict__)
        script_class = getattr(script_module, class_)

        script_instance: BaseScript = script_class(
            adb_device,
            name,
            window_name
        )

        running_scripts[id] = script_instance
        running_scripts[id].start()
        return True


def start_from_local(id: int, name: str, adb_port: int, window_name: str) -> bool:
    global running_scripts
    adb_device = None
    if RUN_LOCAL:
        if not window_name in open_adb_connections:
            try:
                adb_device = u2.connect(f'{LOCAL_HOST}:{adb_port}')
                adb_device.app_current()
            except Exception as e:
                messagebox.showerror('Error', f'Error connecting to {window_name}!')
                print('ADB Error:', e)
                return False
            new_adb_connection(window_name)
        else:
            messagebox.showerror('Error', 'Another script is already connected to this window!')
            return False
        print('Connected to', window_name, '...')

        with open(get_resource_path('scripts/local/scripts.json'), 'r') as f:
            scripts = json.load(f)
            module_name = scripts[name]['module']   
            module_directory = os.path.dirname(get_resource_path(f'scripts/local/'))
            if module_directory not in sys.path:
                sys.path.insert(0, module_directory)

            module = importlib.import_module(module_name)
            with open(get_resource_path(f'scripts/local/{module_name}.py'), 'rb') as file:
                source_bytes = file.read()
                source = str(source_bytes).encode('utf-8')
                class_name = str(scripts[name]['class'])
                exec(source, module.__dict__)
                script_class = getattr(module, class_name)
                script_instance: BaseScript = script_class(
                    adb_device, 
                    name, 
                    window_name, 
                )
                running_scripts[id] = script_instance
                running_scripts[id].start()
                return True

def stop(id: int) -> None:
    if id in running_scripts:
        instance: BaseScript = running_scripts[id]
        instance.stop()
        del running_scripts[id]

def pause(id: int) -> None:
    ...

def get_available_scripts() -> list:
    if RUN_LOCAL:
        with open(get_resource_path('scripts/local/scripts.json'), 'r') as f:
            return list(json.load(f).keys())
    else:
        return available_scripts