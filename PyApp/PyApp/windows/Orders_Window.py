from PyQt5.QtWidgets import QMainWindow,QMessageBox
from db import db
from PyQt5.QtWidgets import QListWidgetItem
from PyQt5 import QtCore
from ui import Ui_orders_win


class OrdersWindow(Ui_orders_win.Ui_MainWindow,QMainWindow):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        self.load_orders()


    def load_orders(self):
            for o in db.getOrdersGrouped():
                text = (
                    f"№{o['order_id']} | "
                    f"{o['date']} | "
                    f"{o['user']} | "
                    f"{o['positions']} поз. | "
                    f"{o['total']} руб."
                )
                item = QListWidgetItem(text)
                item.setData(QtCore.Qt.UserRole, o['order_id'])
                self.list_orders.addItem(item)