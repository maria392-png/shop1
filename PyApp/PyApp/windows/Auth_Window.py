from PyQt5.QtWidgets import QMainWindow,QMessageBox
from db import db
from ui import Ui_auth_Win


class AuthWindow(Ui_auth_Win.Ui_MainWindow,QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.login_btn.clicked.connect(self.handle_login)
        self.guest_btn.clicked.connect(self.handle_guest)
    def handle_login(self):
        user = db.getUser(self.login_input.text())
        if user:
            if user.roles.name == 'Авторизованный пользователь':
                from windows.User_Window import UserWindow
                self.user_win = UserWindow(user)
                self.user_win.show()
                self.close()
            if user.roles.name == 'Менеджер':
                from windows.Manager_Window import ManagerWindow
                self.manager_win = ManagerWindow(user)
                self.manager_win.show()
                self.close()
        else:
            QMessageBox.warning(self,'Ошибка','Неверный логин!')
    def handle_guest(self):
        from windows.Guest_Window import GuestWindow
        self.guest_win = GuestWindow()
        self.guest_win.show()
        self.close()