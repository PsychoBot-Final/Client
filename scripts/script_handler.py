import os
import sys
import json
import types
import tempfile
import requests
import importlib
from base64 import b64decode
from tkinter import messagebox
from error_handler import ADBError
from util import get_resource_path
import customtkinter as ctk
from settings import RUN_LOCAL, WEB_SERVER_URL
from emulators.adb_handler import connect_to_window
from scripts.script import ScriptContainer, BaseScript
from scripts.templates.templates import unzip_templates


script_instances = {}
script_containers = {}
available_scripts = []

def start(id: int, name: str, adb_port: int, window_name: str, parent: ctk.CTkFrame) -> None:
    adb_device = None
    try:
        adb_device = connect_to_window(window_name, adb_port)
    except ADBError as e:
        messagebox.showerror('Connection Error', e)
        return
    if RUN_LOCAL:
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
                module_class = str(scripts[name]['class'])
                exec(source, module.__dict__)
                script_class = getattr(module, module_class)
                script_instance: BaseScript = script_class(adb_device, name, window_name, parent)
                script_instances[id] = script_instance
                # script_instances[id].create_gui(parent)
    else:
        if name in script_containers:
            container: ScriptContainer = script_containers[name]
            file_name = container.file_name
            module_class = container.module_class
            model_path = container.model_path
            print('Model Path:', model_path)
            templates_path = container.templates_path
            source = str(container.source).encode('utf-8')
            script_module = types.ModuleType(file_name)
            exec(source, script_module.__dict__)
            script_class = getattr(script_module, module_class)
            script_instance: BaseScript = script_class(adb_device, name, window_name, parent, templates_path, model_path)
            script_instances[id] = script_instance
            # script_instances[id].create_gui(parent)
        
def stop(id: int) -> None:
    if id in script_instances:
        try:
            instance: BaseScript = script_instances[id]
            instance.close_gui()
            instance.stop()
        except RuntimeError as _:
            ...
        del script_instances[id]

def pause(id: int) -> None:
    if id in script_instances:
        instance: BaseScript = script_instances[id]
        instance.pause_script()

def is_script_paused(id: int) -> bool:
    if id in script_instances:
        instance: BaseScript = script_instances[id]
        return instance.is_script_paused()

def stop_all_scripts() -> None:
    for id, _ in script_instances.items():
        try:
            instance: BaseScript = script_instances[id]
            instance.close_gui()
            instance.stop()
        except RuntimeError as _:
            ...

def remove_all_temp_models() -> None:
    for id, container in script_containers.items():
        os.unlink(container.model_path)

def create_temp_model(model_data: bytes) -> str:
    with tempfile.NamedTemporaryFile(suffix='.pt', delete=False) as model_file:
        model_file.write(model_data)
        temp_model_path = model_file.name
    return temp_model_path

def get_temp_model_path(script_name: str) -> any:
    if script_name in script_containers:
        container = script_containers[script_name]
        return container.model_path

def remove_temp_model(script_name) -> None:
    if script_name in script_containers:
        container: ScriptContainer = script_containers[script_name]
        os.unlink(container.model_path)

def remove_script_container(script_name: str) -> None:
    if script_name in script_containers: 
        del script_containers[script_name]

def recieve_script_names(data) -> None:
    global available_scripts
    available_scripts = data

def receive_script(data) -> None:
    script_name = data['name']
    file_name = data['file_name']
    script_data = str(data['data']).split('|')
    source_data = b64decode(script_data[0]).decode('utf-8')
    model_data = b64decode(script_data[1])
    templates_data = b64decode(script_data[2])
    script_containers[script_name] = ScriptContainer(
        version=float(data['version']),
        file_name=file_name,
        module_class=data['class'],
        source=source_data,
        model_path=create_temp_model(model_data),
        templates_path=unzip_templates(file_name, templates_data)
    )

def script_exists(name: str) -> bool:
    return name in script_containers

def get_script_container(name: str) -> ScriptContainer:
    return script_containers[name] if script_exists(name) else None

def get_script_version(name: str) -> float:
   url = f'http://{WEB_SERVER_URL}/version/{name}'
   request = requests.get(url)
   response = request.json()
   return float(response['version'])


def get_available_scripts() -> list:
    if RUN_LOCAL:
        with open(get_resource_path('scripts/local/scripts.json'), 'r') as f:
            return list(json.load(f).keys())
    else:
        return available_scripts