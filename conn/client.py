import socketio
import logger_configs

from settings import WEB_SERVER_URL
from socketio.exceptions import ConnectionError
from user import (
    get_id,
    get_uuid,
    set_status,
    set_connection_status
)
from scripts.script_handler import (
    receive_script,
    set_script_names
)
from api_loader import (
    receive_api_files, 
    receive_api_templates
)


client = socketio.Client()
logging = logger_configs.get_bot_logger(__name__)


def connect_to_server() -> bool:
    logging.info(f'Connecting to server: {WEB_SERVER_URL}.')
    try:
        client.connect(f'https://{WEB_SERVER_URL}/?uuid={get_uuid()}')
    except ConnectionError as e:
        logging.error(f'Error connecting to server: {e}.')
    except Exception as e:
        logging.error(f'Unexpected error while connecting to server: {e}.')


@client.event
def connect() -> None:
    set_connection_status(True)
    logging.info(f'User {get_id()} connected to server successfully.')


@client.event
def connect_error(data) -> None:
    set_connection_status(False)
    logging.warning(f'Error connecting to server: {data}')


@client.event
def disconnect() -> None:
    set_connection_status(False)
    logging.info(f'User {get_id()} disconnected from server.')


#

@client.on('user_status')
def on_user_status(data: dict) -> None:
    status_id = data.get('id')
    set_status(status_id)
#


def request_script_names() -> None:
    data = {'uuid': get_uuid()}
    send_message(event='request_script_names', data=data, callback=set_script_names)

def request_api_templates() -> None:
    data = {'uuid': get_uuid()}
    send_message(event='request_api_templates', data=data, callback=receive_api_templates)

def request_api_files() -> None:
    data = {'uuid': get_uuid()}
    send_message(event='request_api_files', data=data, callback=receive_api_files)

def request_script(script_name: str) -> None:
    data = {'uuid': get_uuid(), 'script_name': script_name}
    send_message(event='request_script', data=data, callback=receive_script)

#

def disconnect_from_server() -> None:
    client.handlers.clear()
    client.disconnect()
    set_connection_status(False)

def is_connected() -> bool:
    return client.connected

def send_message(event: str, data: any, namespace=None, callback=None) -> None:
    try:
        if callback:
            client.emit(event=event, data=data, namespace=namespace, callback=callback)
        else:
            client.emit(event=event, data=data, namespace=namespace)
        logging.info(f'Client successfully emitted event: {event}.')
    except Exception as e:
        logging.critical(f'Error emitting event {event} - Exception: {e}.')