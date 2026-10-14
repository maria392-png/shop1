from datetime import date

from sqlalchemy import select
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

from PyQt5.QtWidgets import QMessageBox

class Database:
    def __init__(self):
        self.STOCKS_FIELDS = {'count','size','id_stock'}

        self.engine = create_engine('postgresql://postgres:12345@localhost/Practica')
        self.session = Session(self.engine)
        Base = automap_base()
        Base.prepare(self.engine)

        self.users = Base.classes.users
        self.stocks = Base.classes.stocks
        self.manufactures = Base.classes.manufactures
        self.categories = Base.classes.categories
        self.subcategories = Base.classes.subcategories
        self.products = Base.classes.products
        self.sizes = Base.classes.sizes

        self.orders = Base.classes.orders
        self.orderitems = Base.classes.orderitems

        self.allProducts = self.toGroup()
        self.cart = []


    def getUser(self,loginVal):
        stmt = (
            select(self.users)
            .where(self.users.login == loginVal)
        )
        result = self.session.execute(stmt).first()

        return [] if not result else result[0]

    def getCategories(self):
        stmt = (
            select(self.categories.id,self.categories.name)
        )
        result = self.session.execute(stmt).all()
    
        return [dict(row._mapping) for row in result]
    def getSubategories(self):
        stmt = (
            select(self.subcategories.id,self.subcategories.name)
        )
        result = self.session.execute(stmt).all()
        
        return [dict(row._mapping) for row in result]
    def getProducts(self):
        stmt =(
            select(
                self.products.id.label('id_product'),
                self.categories.name.label('category'),
                self.subcategories.name.label('subcategory'),
                self.products.img,
                self.products.name,
                self.manufactures.name.label('manufacture'),
                self.products.description,
                self.products.structure,
                self.products.price,
                self.stocks.id.label('id_stock'),
                self.sizes.name.label('size'),
                self.stocks.count.label('count')
            )
            .join(self.stocks, self.stocks.id_product == self.products.id)
            .join(self.manufactures, self.manufactures.id == self.products.id_manufacture)
            .join(self.categories, self.categories.id == self.products.id_category)
            .join(self.subcategories, self.subcategories.id == self.products.id_subcategory)
            .join(self.sizes, self.stocks.id_size == self.sizes.id)
            .order_by(self.products.id)
        )
        result = self.session.execute(stmt).all()
        return [dict(row._mapping) for row in result]
    def toGroup(self):
        grouped = {}

        for product in list(self.getProducts()):
            product_id = product['id_product']

            if product_id not in grouped:
                grouped[product_id] = {
                    **product,
                    'hidden':False,
                    'totalstock':0,
                    'stocks':[]
                }

            item = grouped[product_id]
            item['totalstock'] += product['count']
            item['stocks'].append({
                'size':product['size'],
                'count':product['count'],
                'id_stock':product['id_stock']
            })

            for key in self.STOCKS_FIELDS:
                grouped[product_id].pop(key,None)
        return list(grouped.values())
    def create_order(self,user_id):
        if len(self.cart):
            try:
                order = self.orders(
                    id_user = user_id,
                    dateoforder = date.today() 
                )
                self.session.add(order)
                self.session.flush()

                for c in self.cart:
                    id_stock = c['selectedStock']
                    count = c['selectedCount']

                    stock = self.session.get(self.stocks,id_stock)

                    if stock is None:
                        raise ValueError(f"stock_id={id_stock} не найден")
                    if stock.count < count:
                        raise ValueError(f"Недостаточно товара (stock_id={id_stock})")

                    stock.count -= count

                    self.session.add(
                        self.orderitems(
                            id_order=order.id,
                            id_stock=id_stock,
                            count = count
                        )
                    )
                self.session.commit()
                QMessageBox.information(None,'Успех','Заказ создан!')
                self.cart.clear()
            except Exception as e:
                self.session.rollback()
                QMessageBox.warning(None,'Ошибка',str(e))
                raise
        else:
            QMessageBox.warning(None,'Ошибка','Корзина пуста!')
    def getOrders(self):
        stmt = (
            select(
                self.orderitems.id.label('order_id'),
                self.orders.dateoforder,
                self.users.surname,
                self.users.name.label('user_name'),
                self.orders.id.label('id_position'),
                self.products.name.label('product'),
                self.sizes.name.label('size'),
                self.orderitems.count,
                self.products.price,
            )
            .join(self.orders, self.orders.id == self.orderitems.id_order)
            .join(self.users, self.users.id == self.orders.id_user)
            .join(self.stocks, self.stocks.id == self.orderitems.id_stock)
            .join(self.products, self.products.id == self.stocks.id_product)
            .join(self.sizes, self.sizes.id == self.stocks.id_size)
            .order_by(self.orderitems.id.desc())
        )
        result = self.session.execute(stmt).all()
        return [dict(row._mapping) for row in result]
    def getOrdersGrouped(self):
        rows = self.getOrders()  
        grouped = {}
        for r in rows:
            oid = r['order_id']
            if oid not in grouped:
                grouped[oid] = {
                    'order_id': oid,
                    'date': r['dateoforder'],
                    'user': f"{r['surname']} {r['user_name']}",
                    'positions': 0,
                    'total': 0,
                    'items': [],
                }
            g = grouped[oid]
            g['positions'] += 1
            g['total'] += r['count'] * r['price']
            g['items'].append(r)
        return list(grouped.values())
db = Database()