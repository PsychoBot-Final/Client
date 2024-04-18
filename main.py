import sys
import json
import time
import requests
from datetime import datetime
from main_gui import MainGUI
from PyQt5.QtWidgets import QMessageBox
from client.client import connect_to_server
from constants import BOT_VERSION, ACCESS_DENIED
from settings import WEB_SERVER_URL
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from error_pages import RETRY, INVALID_USER, EXPIRED_USER
from user import (
    set_user_id, 
    set_instances,
    set_expiry_date,
    get_authenticated,
)


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
        self.setWindowTitle("PsychoBot - Authenticaion")
        self.setGeometry(100, 100, 400, 650)
        self.centerWindow()
        self.webview = QWebEngineView()
        self.setCentralWidget(self.webview)
        self.verify_bot_version()

    def centerWindow(self):
        frame_geometry = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        frame_geometry.moveCenter(center_point)
        self.move(frame_geometry.topLeft())

    def verify_bot_version(self) -> None:
        url = 'http://' + WEB_SERVER_URL + '/version/'
        request = requests.get(url)
        response = request.json()
        bot_version = float(response.get('bot-version'))
        if BOT_VERSION < bot_version:
            QMessageBox.warning(self, 'Update available!', 'This version of the bot is outdated please visit Discord to download the new version!')
            sys.exit()
        else:
            self.loadAuthPage()

    def loadAuthPage(self):
        print('WEB SERVER URL:', WEB_SERVER_URL)
        self.webview.load(QUrl(f'http://{WEB_SERVER_URL}/?auth_key=1234'))
        self.webview.loadFinished.connect(self.onLoadFinished)

    def onLoadFinished(self):
        current_url = self.webview.url().toString()
        user_verified_url = f'http://{WEB_SERVER_URL}/verified'
        if current_url == user_verified_url:
            self.webview.page().toPlainText(self.processUserDetails)
        elif ACCESS_DENIED in current_url:
            self.webview.setHtml(RETRY)
        else:
            pass

    def processUserDetails(self, raw_data):
        user_data: dict = json.loads(raw_data)
        status = int(user_data.get('status'))
        user_id = int(user_data.get('user_id'))
        username = str(user_data.get('username'))
        expiry_date_str = str(user_data.get('expiry_date'))
        instances = int(user_data.get('instances'))
        #
        expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d %H:%M:%S")
        time_remaining = expiry_date - datetime.now()
        days = time_remaining.days
        hours = time_remaining.seconds // 3600
        minutes = time_remaining.seconds // 60
        #
        if status == 0:
            set_user_id(user_id)
            set_instances(instances)
            set_expiry_date(expiry_date_str)
            connect_to_server()
            self.setVisible(False)
            while get_authenticated() is None:
                time.sleep(1)
            if get_authenticated():
                time_str = f'{days} day(s), {hours} hour(s)' if days > 0 or hours > 0 else f'{minutes} minute(s)'
                QMessageBox.information(self, "PsychoBot", f"Welcome {username}, you have {time_str} left!")
                self.close()
                MainGUI()
            else:
                QMessageBox.warning(self, 'Dupliate ID!', 'It seems you are already connected!')
                self.close()
                self.destroy()
                sys.exit(0)
        else:
            self.webview.setHtml(INVALID_USER if status == 1 else EXPIRED_USER)
    
    def closeEvent(self, event):
        event.accept()

if __name__ == "__main__":
    app = DiscordApp(sys.argv)
    app.run()