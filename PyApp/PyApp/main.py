from PyQt5.QtWidgets import QApplication
from windows.Auth_Window import AuthWindow
if __name__ == '__main__':
    app = QApplication([])
    auth_win = AuthWindow()
    auth_win.show()

    app.exec()