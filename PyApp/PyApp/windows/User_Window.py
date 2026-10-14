from PyQt5.QtWidgets import QMainWindow
from db import db
from ui import Ui_user_Win
from PyQt5 import QtCore


class UserWindow(Ui_user_Win.Ui_MainWindow,QMainWindow):
    def __init__(self,user, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.isGuest = False
        self.user = user
        self.loadCombos()
        self.name_user.setText(f"{user.name} {user.surname} {user.lastname}")
        self.logout_btn.clicked.connect(self.logout)
        self.fillter()

        self.price_box.currentIndexChanged.connect(self.fillter)
        self.cat_box.currentIndexChanged.connect(self.fillter)
        self.scat_box.currentIndexChanged.connect(self.fillter)
        self.search_edit.textChanged.connect(self.fillter)
        self.cart_btn.clicked.connect(self.open_cart)


    def loadProducts(self,products):
        if products == None:
            products = db.allProducts
        from windows.Product_Widget import ProductWidget
        layout = self.scrollAreaWidgetContents.layout()
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        for product in list(products):
            layout.addWidget(ProductWidget(product,self))

    def loadCombos(self):
        self.price_box.addItem('Все','0')
        self.price_box.addItem('Дешевле','1')
        self.price_box.addItem('Дороже','2')
        self.cat_box.addItem('Все','0')
        self.scat_box.addItem('Все','0')

        for cat in db.getCategories():
            self.cat_box.addItem(cat['name'],cat['id'])
        for scat in db.getSubategories():
            self.scat_box.addItem(scat['name'],scat['id'])

    def fillter(self):
        price = self.price_box.currentText()
        cat = self.cat_box.currentText()
        scat = self.scat_box.currentText()
        search = self.search_edit.text().lower()
        result = list(db.allProducts)

        if cat != 'Все':
            result = [p for p in result if p['category'] == cat]
        if scat != 'Все':
            result = [p for p in result if p['subcategory'] == scat]
        if search != 'Все':
            result = [p for p in result if search in p['name'].lower()]                      
        if price != 'Все':
            if price == 'Дешевле':
                result.sort(key=lambda x: x['price'])
            else:
                result.sort(key=lambda x: x['price'], reverse=True)
        self.loadProducts(result)
    def logout(self):
        from windows.Auth_Window import AuthWindow
        self.auth_win = AuthWindow()
        self.auth_win.show()
        self.close()

    def open_cart(self):
        from windows.Cart_Window import CartWindow
        self.cart_win = CartWindow(self)
        self.cart_win.show()
        


        