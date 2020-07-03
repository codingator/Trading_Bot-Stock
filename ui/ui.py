from kiwoom.kiwoom import *

import sys
from PyQt5.QtWidgets import *

class Ui_class():
    def __init__(self):
        print("Ui_Class called")

        self.app = QApplication(sys.argv)

        # 변수에 담지않고 Kiwoom()만 했을 때 오류발생. 할당을 안하면 휘발되나?
        self.kiwoom = Kiwoom()

        self.app.exec_()
