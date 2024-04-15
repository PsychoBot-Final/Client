import socketio
from settings import WEB_SERVER_URL
from tkinter import messagebox, ttk
from user import get_id, get_expiry
from client.event_handler import id_in_use

con = socketio.Client()

def init() -> None:
    con.on('id_in_use', handler=id_in_use)
    con.connect(WEB_SERVER_URL)

def send_message(event: str, data: any) -> None:
    con.emit(event, data)

@con.event
def connect() -> None:
    con.emit('new_connection', {'user_id': get_id(), 'expiry_date': get_expiry()})

@con.event
def connect_error(data) -> None:
    ...

@con.event
def disconnect() -> None:
    ...