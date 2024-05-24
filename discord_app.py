import os
import sys
import json
import time
import logger_configs

from main_gui import MainGUI
from datetime import datetime
from PyQt5.QtCore import QUrl
from settings import WEB_SERVER_URL
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from constants import (
    BOT_VERSION, 
    ACCESS_DENIED,
    VALID,
    INVALID,
    EXPIRED,
    IN_USE
)
from error_pages import (
    RETRY, 
    INVALID_USER, 
    EXPIRED_USER, 
    ERROR
)
from PyQt5.QtWidgets import (
    QApplication, 
    QMainWindow, 
    QDesktopWidget
)
from conn.client import (
    request_api_files,
    request_script_names,
    request_api_templates,
    connect_to_server,
    is_connected,
    disconnect_from_server
)
from user import (
    set_uuid,
    get_status_id,
    set_user_id, 
    set_instances,
    set_expiry_date,
    get_authenticated,
)


logger = logger_configs.get_bot_logger(__name__)

class DiscordApp(QApplication):
    def __init__(self, argv):
        super().__init__(argv)
        self.discord_window = DiscordWindow()

    def run(self) -> None:
        self.discord_window.show()
        sys.exit(self.exec_())


class DiscordWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PsychoBot - Authentication")
        self.setGeometry(100, 100, 400, 650)
        self.centerWindow()
        self.webview = QWebEngineView()
        self.setCentralWidget(self.webview)
        self.loadAuthPage()

    def centerWindow(self):
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    # def verify_bot_version(self) -> None:
    #     url = 'https://' + WEB_SERVER_URL + '/version/'
    #     request = requests.get(url)
    #     response = request.json()
    #     bot_version = float(response.get('bot-version'))
    #     if BOT_VERSION < bot_version:
    #         QMessageBox.warning(self, 'Update available!', 'This version of the bot is outdated please visit Discord to download the new version!')
    #         sys.exit()
    #     else:
    #         self.loadAuthPage()

    def loadAuthPage(self):
        self.webview.load(QUrl(f'https://{WEB_SERVER_URL}?auth_key=12345'))
        self.webview.loadFinished.connect(self.onLoadFinished)

    def onLoadFinished(self):
        current_url = self.webview.url().toString()
        user_verified_url = f'https://{WEB_SERVER_URL}/verified'
        if current_url == user_verified_url:
            self.webview.page().toPlainText(self.processUserDetails)
        elif ACCESS_DENIED in current_url:
            logger.warning(msg='Access denied.')
            self.webview.setHtml(RETRY)
        else:
            pass

    def processUserDetails(self, raw_data):
        
        try:
            user_data: dict = json.loads(raw_data)
            # print(user_data)
        except json.JSONDecodeError as e:
            logger.error(msg=f'Failed to retrieve user data - Exception: {e}')
            QMessageBox.critical(self, 'Error', 'Failed to retrieve user data, please restart...')
            self.webview.setHtml(ERROR)
            return

        try:
            uuid = str(user_data.get('uuid'))    
            status = int(user_data.get('status'))
            user_id = int(user_data.get('discord_id'))
            username = str(user_data.get('discord_username'))
            expiry_date_str = str(user_data.get('expiry_date'))
            instances = int(user_data.get('instances'))
            expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d %H:%M:%S")
        except (ValueError, TypeError) as e:
            logger.critical(msg=f'Failed to unpack user data - Exception: {e}')
            QMessageBox.critical(self, 'Error', 'Failed to retrieve user data, please restart...')
            self.webview.setHtml(ERROR)
            return

        time_remaining = expiry_date - datetime.now()
        days = time_remaining.days
        hours = time_remaining.seconds // 3600
        minutes = time_remaining.seconds // 60

        if status == 0:
            set_uuid(uuid)
            set_user_id(user_id)
            set_instances(instances)
            set_expiry_date(expiry_date_str)
            
            connect_to_server()
            self.setVisible(False)

            while status_id:= get_status_id() is None:
                logger.info('waiting...')
                time.sleep(1)

            if status_id == INVALID:
                logger.warning(msg=f'User {username} (ID: {user_id}) is not a valid member.')
                QMessageBox.warning(self, 'Membership Invalid', 'You are not an active member of Psychobot, please visit the official discord to purchase membership.')
                if is_connected():
                    disconnect_from_server()
                self.close()
                self.destroy()
                os._exit(1)

            elif status_id == EXPIRED:
                logger.warning(msg=f'User {username} (ID: {user_id}) membership has expired.')
                QMessageBox.warning(self, 'Membership Expired', 'Your membership has expired, please visit the official discord to renew.')
                if is_connected():
                    disconnect_from_server()
                self.close()
                self.destroy()
                os._exit(1)

            elif status_id == IN_USE:
                logger.warning(msg=f'User {username} (ID: {user_id}) already connected to server.')
                QMessageBox.warning(self, 'Already Connected', 'It seems you are already connected!')
                if is_connected():
                    disconnect_from_server()
                self.close()
                self.destroy()
                os._exit(1)

            elif status_id == VALID:
                request_script_names()
                request_api_templates()
                request_api_files()
                logger.info(msg=f'User {username} (ID: {user_id}) successfully authenticated with the server.')
                time_str = f'{days} day(s), {hours} hour(s)' if days > 0 or hours > 0 else f'{minutes} minute(s)'
                QMessageBox.information(self, "PsychoBot", f"Welcome {username}, you have {time_str} left!")
                self.close()
                MainGUI()
        else:
            logger.info(msg=f'User {username} (ID: {user_id}) failed to authenticated, status: {status}.')
            self.webview.setHtml(INVALID_USER if status == 1 else EXPIRED_USER)
    
    def closeEvent(self, event):
        event.accept()