import socketio
from user import get_id
from settings import WEB_SERVER_URL
from tkinter import messagebox, ttk
from PyQt5.QtWidgets import QMainWindow
from user import set_user_authenticated, set_connection_status
from api_loader import receive_api
from scripts.script_handler import recieve_script_names, receive_script
from util import get_resource_path


con = socketio.Client()

def connect_to_server() -> None:
    con.on('script_names', handler=recieve_script_names)
    con.on('full_script', handler=receive_script)
    con.on('api_files', handler=receive_api)
    con.connect(f'http://{WEB_SERVER_URL}/?user_id={get_id()}')

def verify_integrity() -> None:
    ...

def request_script(type: str, name: str) -> None:
    send_message('request_script', {'type': type, 'name': name})

def request_api() -> None:
    send_message('request_api', {})

@con.event
def authenticated(flag: bool) -> None:
    set_user_authenticated(flag)

@con.event
def connect() -> None:
    print('User', get_id(), 'Connected...')
    set_connection_status(True)

@con.event
def connect_error(data) -> None:
    print('Error connecting to server...')
    set_connection_status(False)

@con.event
def disconnect() -> None:
    print('User', get_id(), 'Disconnected...')
    set_connection_status(False)

def send_message(event: str, data: any) -> None:
    try:
        con.emit(event, data)
    except Exception as e:
        print('Error:', e)