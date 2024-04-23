import requests
# from script_container import ScriptContainer
from utils import get_resource_path
from client.client import send_message
from settings import RUN_LOCAL, WEB_SERVER_URL


script_containers = {}

# def request_script(file_name: str) -> None:
#     if file_name in script_containers:
#         script = script_containers[file_name]
#         container = ScriptContainer(
#             version=script['version'],
#             file_name=script['file_name'],
#             class_=script['class_'],
#             source=script['source'],
#             model=script['model'],
#             templates=script['templates']
#         )
#     else:
#         url = f'http://{WEB_SERVER_URL}/version/{file_name}'





def sync(name: str) -> None:
    url = f'http://{WEB_SERVER_URL}/version/{name}'
    request = requests.get(url)
    response = request.json()
    server_version = float(response['version'])
    client_version = float(scripts.get(name, {}).get('version', 0))
    if client_version < server_version:
        send_message('sync_script', {'name': name})

def download(data) -> None:
    global scripts
    scripts[data['name']] = {
        'version': float(data['version']),
        'class': data['class'],
        'module': data['module'],
        'source': data['source']
    }

    model = data['model']
    templates = data['templates']
    
def start(id: int, name: str) -> None:
    sync(name)

def stop(id: int) -> None:
    ...

def pause(id: int) -> None:
    ...