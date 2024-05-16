import socketio
import logger_configs
from user import get_id
from api_loader import receive_api
from settings import WEB_SERVER_URL, PORT
from user import set_user_authenticated, set_connection_status
from scripts.script_handler import recieve_script_names, receive_script


logger = logger_configs.get_bot_logger(__name__)
con = socketio.Client()

def connect_to_server() -> None:
    con.on('script_names', handler=recieve_script_names)
    con.on('full_script', handler=receive_script)
    con.on('api_files', handler=receive_api)
    logger.info('Connecting to server.')
    con.connect(f'https://{WEB_SERVER_URL}/?user_id={get_id()}')

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
    logger.info('Connected to server.')
    print('User', get_id(), 'Connected...')
    set_connection_status(True)

@con.event
def connect_error(data) -> None:
    print('Error connecting to server...')
    set_connection_status(False)
    logger.warning('Error connecting to server.')

@con.event
def disconnect() -> None:
    print('User', get_id(), 'Disconnected...')
    set_connection_status(False)
    logger.warning('Disconnected from server.')

def send_message(event: str, data: any) -> None:
    try:
        con.emit(event, data)
        logger.info(f'Successfully emitted event: {event}')
    except Exception as e:
        logger.critical(f'Error emitting event: {event} - Exception: {e}')