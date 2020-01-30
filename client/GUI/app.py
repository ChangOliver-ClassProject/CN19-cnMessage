import sys
import os
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from tmp_app import Ui_Form
from LogIn import *

import socket
import hashlib
import pickle

sys.path.append(os.getcwd() + '/..')
from client import *
from util import *

class AppWindow(QWidget):
    def __init__(self, parent = None):
        super(AppWindow, self).__init__(parent)
        
        global s, user
        s = socket.socket()
        s.connect((SERVER_IP, PORT)) 
        print(str(s.recv(RECV_SIZE))[2:-1]) # welcome message

        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self._title = "登入介面"
        self.setWindowTitle(self._title)
        self.ui.signIn_button.clicked.connect(self.signIn)
        self.ui.signUp_button.clicked.connect(self.signUp)
        self.show()
        self.ui.lineEdit.setPlaceholderText("20個字符以內，只可使用字母or數字")
        self.ui.lineEdit_2.setEchoMode(QLineEdit.Password)

        regx = QRegExp("[0-9A-Za-z]{29}$")
        validator_1 = QRegExpValidator(regx, self.ui.lineEdit)
        validator_2 = QRegExpValidator(regx, self.ui.lineEdit_2)
        self.ui.lineEdit.setValidator(validator_1)
        self.ui.lineEdit_2.setValidator(validator_2)
        print("connected")

    def signIn(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text() 

        success, message = sign_in(s, username, password)

        if (success):
            QMessageBox.information(self, "Congratulation", message, QMessageBox.Ok)
            MainWindow = QMainWindow()
            l = LogWindow(None, username)
            l.__init__(MainWindow)
            self.ui.signIn_button.clicked.connect(MainWindow.__init__)
            self.hide()
        else:
            QMessageBox.warning(self, "Critical", message, QMessageBox.Ok)
            self.ui.lineEdit_2.clear()

    def signUp(self):
        username = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()

        # 檢查帳號是否存在database裡
        success, message = sign_up(s, username, password)

        if (success):
            QMessageBox.information(self, "Congratulation", message, QMessageBox.Ok)
            MainWindow = QMainWindow()
            l = LogWindow()
            l.__init__(MainWindow)
            self.ui.signIn_button.clicked.connect(MainWindow.__init__)
            self.hide()
        else:
            QMessageBox.warning(self, "Critical", message, QMessageBox.Ok)
            self.ui.lineEdit.clear()
            self.ui.lineEdit_2.clear() 

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = AppWindow()
    w.show()
    sys.exit(app.exec_())
    print("shut down")