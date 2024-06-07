import os
import sys
import json
import types
import tempfile
import requests
import importlib
import logger_configs
from base64 import b64decode
from tkinter import messagebox
from error_handler import ADBError
from util import get_resource_path
from uiautomator2 import Device
import customtkinter as ctk
from settings import RUN_LOCAL, WEB_SERVER_URL
from emulators.adb_handler import connect_to_window
from scripts.script import ScriptContainer, BaseScript
from scripts.templates.templates import unzip_templates


script_instances = {}
script_containers = {}
available_scripts = []
script_modules = {}
logger = logger_configs.get_bot_logger(__name__)

def start(id: int, name: str, adb_port: int, window_name: str, parent) -> None:
    adb_device = None
    try:
        adb_device = connect_to_window(window_name, adb_port)
        logger.info(f'Connected to ADB: {window_name} on port: {adb_port}.')
    except ADBError as e:
        logger.error(f'Error connecting to ADB: {window_name} on port: {adb_port}.')
        messagebox.showerror('Connection Error', e)
        return False
    return (start_local_script if RUN_LOCAL else start_remote_script)(id, name, adb_device, window_name, parent)

def start_local_script(id: int, name: str, adb_device: Device, window_name: str, parent) -> bool:
    try:
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
                script_instance: BaseScript = script_class(id, adb_device, name, window_name, parent)
                script_instances[id] = script_instance
                script_modules[id] = module_name
                return True
    except Exception as e:
        logger.error('Failed to start local script:', e)
        return False

def start_remote_script(id: int, name: str, adb_device: Device, window_name: str, parent) -> bool:
    try:
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
            script_instance: BaseScript = script_class(id, adb_device, name, window_name, parent, templates_path, model_path)
            script_instances[id] = script_instance
            return True
    except Exception as e:
        logger.error('Failed to start remote script:', e)
        return False

def stop(id: int) -> None:
    if id in script_instances:
        try:
            instance: BaseScript = script_instances[id]
            instance.close_gui()
            instance.close_paint()
            instance.stop()
            if id in script_modules:
                module_name = script_modules[id]
                if module_name in sys.modules:
                    del sys.modules[module_name]
                    del script_modules[id]
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
            instance.close_paint()
            instance.stop()
        except RuntimeError as _:
            ...

def show_paint(id: int) -> None:
    if id in script_instances:
        instance: BaseScript = script_instances[id]
        instance.show_paint()

def remove_all_temp_models() -> None:
    logger.info('Removing all temp models.')
    for _, container in script_containers.items():
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

def set_script_names(data: dict) -> None:
    global available_scripts
    available_scripts = data

def receive_script(data) -> None:
    data = data['result']
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
    logger.info(f'Downloaded script: {script_name}.')

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