# import sys
# from typing import List
# from PyQt5.QtWidgets import QApplication, QSplashScreen, QMainWindow, QWidget
# from PyQt5.QtCore import Qt, QTimer
# from PyQt5.QtGui import QPixmap


# def after_splash():
#     print("Splash screen completed. Initialization done.")
#     # You can also add more code here to perform other actions.
#     sys.exit(0)

# def main():
#     app = QApplication(sys.argv)
    
#     # Load the splash screen image
#     pixmap = QPixmap("./quality.png")
#     splash = QSplashScreen(pixmap, Qt.WindowStaysOnTopHint)
#     splash.setMask(pixmap.mask())  # This ensures non-rectangular splash screens
#     splash.show()

#     # Main window code
#     main_window = QMainWindow()
#     main_window.setWindowTitle("My Application")
#     main_window.setGeometry(300, 300, 600, 400)  # Set position and size of the window

#     def on_splash_finished():
#         after_splash()  # Call a function after showing the main window

#     # Schedule the splash to close and main window to show
#     QTimer.singleShot(3000, lambda: splash.close())
#     QTimer.singleShot(3000, on_splash_finished)  # Ensure this runs after splash is closed
    
#     # Finish initialization and run the application
#     splash.finish(main_window)
#     sys.exit(app.exec_())

# if __name__ == "__main__":
#     main()


import sys
from PyQt5.QtWidgets import QApplication, QSplashScreen, QMainWindow
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from main_gui import MainGUI

class SplashScreen(QSplashScreen):
    def __init__(self, image_path):
        pixmap = QPixmap(image_path)
        super().__init__(pixmap, Qt.WindowStaysOnTopHint)
        self.setMask(pixmap.mask())

    def show_splash(self, timeout_ms, callback):
        self.show()
        QTimer.singleShot(timeout_ms, self.close)
        QTimer.singleShot(timeout_ms, callback)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("My Application")
        self.setGeometry(300, 300, 600, 400)

class SplashApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.main_window = MainWindow()
        self.splash_screen = SplashScreen("./quality.png")
        self.run()

    def run(self):
        self.splash_screen.show_splash(3000, self.after_splash)
        sys.exit(self.app.exec_())

    def after_splash(self):
        print("Splash screen completed. Initialization done.")
        MainGUI()
        sys.exit(0)

if __name__ == "__main__":
    app = SplashApp()
    app.run()
