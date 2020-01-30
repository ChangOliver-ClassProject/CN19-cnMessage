import sys
import os
import threading
import time
import signal
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtNetwork import *
from app import *
from tmp_LogIn import Ui_MainWindow

class noticeMessageThread:
	def __init__(self):
		self.isRunning = True
		
	def run(self):
		distance = 0
		while self.isRunning:
			print("Noticing msg now...")
			distance = distance + 1
			w.msgUpdate(distance)
			# update 各個log的資料是否與現在的有所不同，差了n行內容
			# TODO: 顯示有n則通知
			time.sleep(1)

	def stop(self):
		print("Stop noticing")
		self.isRunning = False

class showMessageThread:
	def __init__(self, _username, _recipient):
		self.isRunning = True
		self.username = _username
		self.recipient = _recipient

	def run(self):
		while self.isRunning:
			print("thread is running")
			# s.sendall(pickle.dumps(packet(302, [username, self.recipient])))
			#收訊息並更新history
			time.sleep(1)

	def stop(self):
		self.isRunning = False
		LogWindow.stop(self)

class LogoutMsg(QWidget):
	def __init__(self):
		super().__init__()

		self.initUI()

	def initUI(self):
		self.setGeometry(300, 300, 250, 150)
		self.question = QLabel("請問您確定要登出嗎？")
		self.question.setAlignment(Qt.AlignCenter)
		self.yesbtn = QPushButton("是", self)
		self.nobtn = QPushButton("否", self)
		self.vLayout = QVBoxLayout()
		self.hLayout = QHBoxLayout()
		self.hLayout.addWidget(self.yesbtn)
		self.hLayout.addWidget(self.nobtn)
		self.vLayout.addWidget(self.question)
		self.vLayout.addLayout(self.hLayout)
		self.yesbtn.clicked.connect(self.logout)
		self.nobtn.clicked.connect(self.cancel)
		self.setLayout(self.vLayout)

	def logout(self):
		w.logout()
		self.hide()

	def cancel(self):
		print("I don't want to logout.")
		self.hide()

class LogWindow(QMainWindow):
	def __init__(self, parent = None, username = ""):
		super().__init__()
		self.ui = Ui_MainWindow()
		self.ui.setupUi(self)
		self.show()
		self.username = username
		self._title = self.username + "的聊天室"
		self.setWindowTitle(self._title)
		self.cwd = os.getcwd()	#獲取當前文件位置
		self.ui.fileInput.clicked.connect(self.chooseFile)
		self.ui.textInput.clicked.connect(self.textTransfer)
		self.ui.stopbtn.clicked.connect(showMessageThread.stop)
		# self.ui.changebtn.clicked.connect(self.changeRecipient)
		self.ui.person_1.clicked.connect(self.start)
		self.ui.person_2.clicked.connect(self.start)
		self.ui.person_3.clicked.connect(self.start)
		self.ui.person_4.clicked.connect(self.start)
		global ntc_t
		ntc_t = noticeMessageThread()
		global t_check
		t_check = threading.Thread(target = ntc_t.run)
		t_check.start()
		if (ntc_t.isRunning == False):
			t_check.join()

	def start(self):
		print("now showing msg")
		global msg_t
		msg_t = showMessageThread(self.username, self.username)
		print("start thread")
		t = threading.Thread(target = msg_t.run)
		t.start()
		if ():
			print("join thread")
			t.join()

	# def changeRecipient(self):
		

	def stop(self, t):
		# msg_t.stop()
		t.join()

	def msgUpdate(self, i):
		self.ui.msgcnt_4.setText(str(i))

	def chooseFile(self):
		files, filetype = QFileDialog.getOpenFileNames(self, "多文件選擇", self.cwd, "All Files (*);; mp3 Files (*.mp3);; jpg Files (*.jpg);; PDF Files (*.pdf);; Text Files (*.txt)")  

		if len(files) == 0:
			return

		for file in files:
			self.ui.history.append(self.username + "已傳送檔案給您")
			print(file)
			# 傳送檔案, file為各檔案的絕對路徑

		self.ui.lineEdit.clear()

	def textTransfer(self):
		text = self.ui.lineEdit.text()
		if len(text) == 0:
			return
		#傳送訊息
		self.ui.history.append("[" + self.username + "]:" + text)
		
		self.ui.lineEdit.clear()

	def logout(self):
		widget = QWidget()
		a = AppWindow()
		a.__init__(widget)
		self.hide()

		# MainWindow = QMainWindow()
		# l = LogWindow()
  #           l.__init__(MainWindow)
  #           self.ui.signIn_button.clicked.connect(MainWindow.__init__)
  #           self.hide()

	def closeEvent(self,event):
		result = QMessageBox.question(self, "Confirm Exit...", "請問您確定要登出並離開嗎？", QMessageBox.Yes| QMessageBox.No)
		
		event.ignore()

		if result == QMessageBox.Yes:
			ntc_t.isRunning = False # TODO: CANNOT join the thread correctly
			msg_t.isRunning = False
			# tt.join()
			event.accept()

if __name__ == "__main__":
	app = QApplication(sys.argv)
	w = LogWindow()
	l = LogoutMsg()
	w.show()
	w.ui.logoutbtn.clicked.connect(l.__init__)
	sys.exit(app.exec_())