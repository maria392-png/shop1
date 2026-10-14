from PyQt5.QtWidgets import QMainWindow
from db import db
from ui import Ui_guest_Win


class GuestWindow(Ui_guest_Win.Ui_MainWindow,QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.isGuest = True
        self.loadProducts()
        self.login_btn.clicked.connect(self.handle_login)

    def loadProducts(self):
        from windows.Product_Widget import ProductWidget
        layout = self.scrollAreaWidgetContents.layout()

        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for product in list(db.allProducts):
            layout.addWidget(ProductWidget(product,self))
    def handle_login(self):
        from windows.Auth_Window import AuthWindow
        self.auth_win = AuthWindow()
        self.auth_win.show()
        self.close()