import socketio
from user import get_id
from settings import WEB_SERVER_URL
from tkinter import messagebox, ttk
from PyQt5.QtWidgets import QMainWindow
from user import set_user_authenticated


con = socketio.Client()

def connect_to_server() -> None:
    con.connect(f'http://{WEB_SERVER_URL}/?user_id={get_id()}')

@con.event
def authenticated(flag: bool) -> None:
    set_user_authenticated(flag)

@con.event
def connect() -> None:
    print('User', get_id(), 'Connected...')

@con.event
def connect_error(data) -> None:
    print('Error connecting to server...')

@con.event
def disconnect() -> None:
    print('User', get_id(), 'Disconnected...')

def send_message(event: str, data: any) -> None:
    try:
        con.emit(event, data)
    except Exception as e:
        print('Error:', e)