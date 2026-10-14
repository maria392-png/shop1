from PyQt5.QtWidgets import QMainWindow
from db import db
from ui import Ui_cart_Win


class CartWindow(Ui_cart_Win.Ui_MainWindow,QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.parent = parent
        self.setupUi(self)
        self.loadCart()
        self.cancel_btn.clicked.connect(lambda: self.close())
        self.to_order_btn.clicked.connect(self.create_order)

    def loadCart(self):
        from windows.Product_In_Cart_Widget import ProductInCartWidget
        layout = self.scrollAreaWidgetContents.layout()

        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        totalPrice = 0
        for cart in db.cart:
            totalPrice += cart['price'] * cart['selectedCount']
            layout.addWidget(ProductInCartWidget(cart,self))
        self.sum.setText(f"Сумма: {totalPrice}")
    def create_order(self):
        db.create_order(self.parent.user.id)
        self.close()
        