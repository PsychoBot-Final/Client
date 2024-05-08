import os
from dotenv import load_dotenv

load_dotenv()

LOCAL_HOST = os.environ.get('LOCAL_HOST')
LOCAL_SERVER_URL = os.environ.get('LOCAL_SERVER_URL')
PUBLIC_SERVER_URL = os.environ.get('PUBLIC_SERVER_URL')

LOCAL_HOST = '127.0.0.1'
OUTDATED = 'outdated'
VALID, INVALID, EXPIRED = range(3)
FILE_PATH = r'C:\ProgramData\BlueStacks_nxt\bluestacks.conf'
DISPLAY_NAME_PATTERN = r'bst\.instance\.(.+?_\d+)\.display_name="(.+?)"'
ADB_PORT_PATTERN = r'bst\.instance\.(.+?_\d+)\.status\.adb_port="(.+?)"'
ACCESS_DENIED = os.environ.get('ACCESS_DENIED')
HOME_DIR = os.path.expanduser('~')
BOT_DIR_PATH = os.path.join(HOME_DIR, '.psychobot')
TEMPLATES_DIR_PATH = os.path.join(BOT_DIR_PATH, 'templates')
VERSIONS_FILE_PATH = os.path.join(BOT_DIR_PATH, 'versions.json')

VALID_TEMPLATE_EXTENSIONS = ['.jpg', '.png', '.bmp']

BOT_VERSION = 1.0