from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap
from db import db
from ui import Ui_product_Window


class ProductWindow(Ui_product_Window.Ui_MainWindow,QMainWindow):
    def __init__(self,product, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.product = product
        self.parent = parent
        self.loadData()
        self.size_box.currentIndexChanged.connect(self.setMaximusSpin)
        self.cancel_btn.clicked.connect(lambda: self.close())
        self.cart_btn.clicked.connect(self.to_cart)

    def loadData(self):
        self.name.setText(self.product['name'])
        self.manufacture.setText(self.product['manufacture'])
        self.cat.setText(self.product['category'])
        self.scat.setText(self.product['subcategory'])
        self.description.setText(self.product['description'])
        self.structure.setText(self.product['structure'])
        self.price.setText(f"Цена: {str(self.product['price'])}")
        self.img.setPixmap(QPixmap(f"img/{self.product['img']}"))
        self.loadSizes()
        self.setMaximusSpin()
    def loadSizes(self):
        for stock in self.product['stocks']:
            if stock['count'] > 0:
                self.size_box.addItem(stock['size'],stock['id_stock'])

    def setMaximusSpin(self):
        for stock in self.product['stocks']:
            if stock['size'] == self.size_box.currentText():
                self.count_spin.setMaximum(stock['count'])

    def group_cart(self):
        grouped = {}
        for c in db.cart:
            id_stock = c['selectedStock']
            if id_stock not in grouped:
                grouped[id_stock] = {
                    **c
                }
            else:
                item = grouped[id_stock]
                item['selectedCount'] += c['selectedCount']
        return list(grouped.values())

    def to_cart(self):
        db.cart.append({
            **self.product,
            'selectedStock':self.size_box.currentData(),
            'selectedSize':self.size_box.currentText(),
            'selectedCount':self.count_spin.value()
        })
        db.cart = self.group_cart()

        for p in db.allProducts:
            for stock in p['stocks']:
                if stock['id_stock'] == self.size_box.currentData():
                    stock['count'] -= self.count_spin.value()
                    p['totalstock'] -= self.count_spin.value()
                    if p['totalstock'] < 1:
                        p['hidden'] = True

        self.parent.window().fillter()
        self.close()
                
                
        
            
        