from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from db import db
from ui import Ui_product_Widget


class ProductWidget(Ui_product_Widget.Ui_Form,QWidget):
    def __init__(self,product, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.parent = parent
        self.product = product
        self.setAttribute(Qt.WA_StyledBackground,True)
        self.loadData()
        self.mousePressEvent = self.onClick

        if product['totalstock'] < 1:
            self.deleteLater()

    def loadData(self):
        self.name.setText(f"{self.product['name']} | {self.product['manufacture']}")
        self.cat.setText(self.product['category'])
        self.structure.setText(self.product['structure'])
        self.total_stock.setText(f"Кол-во: {str(self.product['totalstock'])}")
        self.price.setText(f"Цена: {str(self.product['price'])}")
        img = QPixmap(f"img/{self.product['img']}")
        if not img.isNull():
            self.img.setPixmap(img)

        if self.product['totalstock'] <= 3:
            self.setStyleSheet(self.styleSheet() + "#Form{"
            "border-color:#FF8080;}")
    def onClick(self,event):
        if event.buttons() == Qt.LeftButton and not self.parent.isGuest:
            from windows.Product_Window import ProductWindow
            self.product_win = ProductWindow(self.product,self.parent)
            self.product_win.show()
