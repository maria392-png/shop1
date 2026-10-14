from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from db import db
from ui import Ui_product_in_cart_Widget


class ProductInCartWidget(Ui_product_in_cart_Widget.Ui_Form,QWidget):
    def __init__(self,product, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.product = product
        self.parent = parent
        self.setAttribute(Qt.WA_StyledBackground,True)
        self.loadData()
        self.delete_from_cart_btn.clicked.connect(self.delete_from_cart)
    
    def loadData(self):
        self.name.setText(f"{self.product['name']} | {self.product['manufacture']}")
        self.cat.setText(self.product['category'])
        self.structure.setText(f"Выбранный размер: {self.product['selectedSize']}")
        self.total_stock.setText(f"Кол-во: {str(self.product['selectedCount'])}")
        self.price.setText(f"Цена: {str(self.product['price'] * self.product['selectedCount'])}")
        self.img.setPixmap(QPixmap(f"img/{self.product['img']}"))

    def delete_from_cart(self):
        db.cart.remove(self.product)
        for p in db.allProducts:
            for stock in p['stocks']:
                if stock['id_stock'] == self.product['selectedStock']:
                    stock['count'] += self.product['selectedCount']
                    p['totalstock'] += self.product['selectedCount']
                    if p['totalstock'] > 0:
                        p['hidden'] = False


        totalPrice = 0
        for c in db.cart:
            totalPrice += c['price'] * c['selectedCount']
        self.parent.sum.setText(f"Сумма: {str(totalPrice)}")
        self.window().parent.fillter()
        self.deleteLater()
