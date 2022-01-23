# -*- coding: utf-8 -*-

# PyQt5
from marshal import dumps
from PyQt5 import QtCore, QtGui, QtWidgets

# GUI
from message_box import MessageBox
from bot_panel import BotPanel
import Authorization.auth as auth
import Registration.reg as reg

# Другие
from methods import *
import requests
import Config
import json
import sys

# Создание файла "User-Commands.json" для работы бота
if find_file('User-Commands.json') == False:
	with open('User-Commands.json', 'ab') as file:
		file.write(json.dumps([], ensure_ascii = False, indent = 2).encode('UTF-8'))

# Создание файла "Bot-Settings.json" для работы бота
if find_file('Bot-Settings.json') == False:
	with open('Bot-Settings.json', 'a') as file:
		data = {
			'Automati_Authorizaton': False,
			'Automati_Save_Log': False,
			'User_Commands': False,
			'VK_Token': '',
			'Group_ID': ''
		}
		file.write(json.dumps(data, ensure_ascii = False, indent = 2).encode('UTF-8'))

# Графический интерфейс программы
# ==================================================================
class Registration(QtWidgets.QMainWindow): # Окно регистрации
	def __init__(self, parent = None):
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = reg.Ui_MainWindow()
		self.ui.setupUi(self)

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

		# Обработчики основных кнопок
		self.ui.ShowPasswordButton.clicked.connect(self.show_password)
		self.ui.CreateAccountButton.clicked.connect(self.create_account)
		self.ui.LoginLineEdit.returnPressed.connect(self.create_account)
		self.ui.PasswordLineEdit.returnPressed.connect(self.create_account)
		self.ui.AskButton.clicked.connect(self.authorization_window)

		# Обработчики кнопок с панели
		self.ui.CloseWindowButton.clicked.connect(lambda: self.close())
		self.ui.MinimizeWindowButton.clicked.connect(lambda: self.showMinimized())

	# Перетаскивание безрамочного окна
	# ==================================================================
	def center(self):
		qr = self.frameGeometry()
		cp = QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def mousePressEvent(self, event):
		self.oldPos = event.globalPos()

	def mouseMoveEvent(self, event):
		try:
			delta = QtCore.QPoint(event.globalPos() - self.oldPos)
			self.move(self.x() + delta.x(), self.y() + delta.y())
			self.oldPos = event.globalPos()
		except AttributeError:
			pass
	# ==================================================================

	# Логика основных кнопок
	# ==================================================================
	def show_password(self):
		if self.ui.PasswordLineEdit.echoMode() == 2:
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/eyeOff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.ShowPasswordButton.setIcon(icon)
			self.ui.PasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
		else:
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/eyeOn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.ShowPasswordButton.setIcon(icon)
			self.ui.PasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

	def create_account(self):
		data = {
			'Login': self.ui.LoginLineEdit.text(),
			'Password': self.ui.PasswordLineEdit.text()
		}
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/registration', json = data)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			message_box = MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
			message_box.signalButton.connect(lambda: message_box.close())
			message_box.show()
			auth = Authorization()
			self.close()
			auth.show()
		else:
			message_box = MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
			message_box.signalButton.connect(lambda: message_box.close())
			message_box.show()

	def authorization_window(self):
		auth = Authorization()
		self.close()
		auth.show()

class Authorization(QtWidgets.QMainWindow): # Окно авторизации
	def __init__(self, parent = None):
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = auth.Ui_MainWindow()
		self.ui.setupUi(self)
		self.setWindowModality(2)

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

		# Обработчики основных кнопок
		self.ui.ShowPasswordButton.clicked.connect(self.show_password)
		self.ui.AuthorizationButton.clicked.connect(self.authorization)
		self.ui.LoginLineEdit.returnPressed.connect(self.authorization)
		self.ui.PasswordLineEdit.returnPressed.connect(self.authorization)
		self.ui.AskButton.clicked.connect(self.registration_window)

		# Обработчики кнопок с панели
		self.ui.CloseWindowButton.clicked.connect(lambda: self.close())
		self.ui.MinimizeWindowButton.clicked.connect(lambda: self.showMinimized())

	# Перетаскивание безрамочного окна
	# ==================================================================
	def center(self):
		qr = self.frameGeometry()
		cp = QtWidgets.QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def mousePressEvent(self, event):
		self.oldPos = event.globalPos()

	def mouseMoveEvent(self, event):
		try:
			delta = QtCore.QPoint(event.globalPos() - self.oldPos)
			self.move(self.x() + delta.x(), self.y() + delta.y())
			self.oldPos = event.globalPos()
		except AttributeError:
			pass
	# ==================================================================

	# Логика основных кнопок
	# ==================================================================
	def show_password(self):
		if self.ui.PasswordLineEdit.echoMode() == 2:
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/eyeOff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.ShowPasswordButton.setIcon(icon)
			self.ui.PasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
		else:
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/eyeOn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.ShowPasswordButton.setIcon(icon)
			self.ui.PasswordLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

	def authorization(self):
		data = {
			'Login': self.ui.LoginLineEdit.text(),
			'Password': self.ui.PasswordLineEdit.text()
		}
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/authorization', json = data)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			message_box = MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
			message_box.signalButton.connect(lambda: message_box.close())
			message_box.show()
			Config.UNIQUE_KEY = server_answer_text['Unique_Key']
			bot_panel = BotPanel(self.ui.LoginLineEdit.text(), self.ui.PasswordLineEdit.text())
			self.close()
			bot_panel.show()
		else:
			message_box = MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
			message_box.signalButton.connect(lambda: message_box.close())
			message_box.show()

	def registration_window(self):
		reg = Registration()
		self.close()
		reg.show()
# ==================================================================

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	bot_settings = get_bot_settings()
	if bot_settings['Automati_Authorizaton'] == True:
		data = {
			'Login': bot_settings['Login'],
			'Password': bot_settings['Password']
		}
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/authorization', json = data)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			Config.UNIQUE_KEY = server_answer_text['Unique_Key']
			myapp = BotPanel(bot_settings['Login'], bot_settings['Password'])
		else:
			bot_settings.update(
				{
					'Automati_Authorizaton': False
				}
			)
			for item in ['Login', 'Password']:
				bot_settings.pop(item)
			with open('Bot-Settings.json', 'wb') as file: 
				file.write(json.dumps(bot_settings, ensure_ascii = False, indent = 2).encode('UTF-8'))
			myapp = Authorization()
	else:
		myapp = Authorization()
	myapp.show()
	sys.exit(app.exec_())