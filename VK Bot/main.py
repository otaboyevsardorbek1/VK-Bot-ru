# -*- coding: utf-8 -*-

# VK_API
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

# GUI
import MessageBox.message_box as message_box
import Bot_Panel.Settings_Panel.settings_panel as settings_panel
import Bot_Panel.bot_panel as bot_panel
import Authorization.auth as auth
import Registration.reg as reg

# Другие
import datetime
import requests
import json
import time
import sys
import os

# Обычные функции для глобального применения
# ==================================================================
def get_bot_settings(): # Функция возврата настроек бота
	with open('Bot-Settings.json') as file:
		bot_settings = json.loads(file.read())
	return bot_settings

def find_file(find_name, path = None): # Функция для поиска файлов
	file_find = False
	if path == None:
		listdir = os.listdir()
	else:
		listdir = os.listdir(path)
	for file in listdir:
		if file == find_name:
			file_find = True
	return file_find
# ==================================================================

# Создание файла "Bot-Settings.json" для работы бота
if find_file('Bot-Settings.json') == False:
	with open('Bot-Settings.json', 'a') as file:
		data = {
			'Automati_Authorizaton': False,
			'User_Commands': False,
			'VK_Token': '',
			'Group_ID': ''
		}
		file.write(json.dumps(data, ensure_ascii = False))

# Настройки бота
class Config:
	SERVER = 'http://exg1o.pythonanywhere.com'
	# SERVER = 'http://127.0.0.1:5000/'
	UNIQUE_KEY = None

	RANKS = {
		1: 'Посвящённый',
		4: 'Junior',
		12: 'Middle',
		16: 'Senior',
		20: 'Бог программирования'
	}

# Графический интерфейс программы
# ==================================================================
class MessageBox(QtWidgets.QMainWindow): # Всплывающее окно
	signalButton = QtCore.pyqtSignal(str)

	def __init__(self, parent = None, font_size = 10, text = '', button_1 = '', button_2 = ''):
		super().__init__(parent, QtCore.Qt.Window)
		_translate = QtCore.QCoreApplication.translate
		self.ui = message_box.Ui_Form()
		self.ui.setupUi(self)
		self.setWindowModality(2)

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

		self.ui.Label.setText(text)

		font = QtGui.QFont()
		font.setPointSize(11)
		font.setBold(True)
		font.setWeight(75)
		style = """
QPushButton{
	color: white;
	border-radius: 8px;
	background-color: #595F76;
}

QPushButton:hover{
	background-color: #50566E;
}

QPushButton:pressed{
	background-color: #434965;
}
"""
		if button_1 != '' and button_2 != '':
			self.Button_1 = QtWidgets.QPushButton(self.ui.Window)
			self.Button_1.setGeometry(QtCore.QRect(20, 70, 171, 41))
			self.Button_1.setFont(font)
			self.Button_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
			self.Button_1.setStyleSheet(style)

			self.Button_2 = QtWidgets.QPushButton(self.ui.Window)
			self.Button_2.setGeometry(QtCore.QRect(210, 70, 171, 41))
			self.Button_2.setFont(font)
			self.Button_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
			self.Button_2.setStyleSheet(style)

			self.Button_1.setText(_translate('Form', button_1))
			self.Button_2.setText(_translate('Form', button_2))

			self.Button_1.clicked.connect(lambda: self.signalButton.emit(button_1))
			self.Button_2.clicked.connect(lambda: self.signalButton.emit(button_2))
		elif button_1 != '':
			self.Button_1 = QtWidgets.QPushButton(self.ui.Window)
			self.Button_1.setGeometry(QtCore.QRect(120, 70, 161, 41))
			self.Button_1.setFont(font)
			self.Button_1.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
			self.Button_1.setStyleSheet(style)
			self.Button_1.setText(_translate('Form', button_1))
			self.Button_1.clicked.connect(lambda: self.signalButton.emit(button_1))
		elif button_2 != '':
			self.Button_2 = QtWidgets.QPushButton(self.ui.Window)
			self.Button_2.setGeometry(QtCore.QRect(120, 70, 161, 41))
			self.Button_2.setFont(font)
			self.Button_2.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
			self.Button_2.setStyleSheet(style)
			self.Button_2.setText(_translate('Form', button_2))
			self.Button_2.clicked.connect(lambda: self.signalButton.emit(button_2))

		font.setPointSize(font_size)
		self.ui.Label.setFont(font)

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

class SettingsPanel(QtWidgets.QMainWindow): # Окно настроек бота
	signalUpdateBotSettings = QtCore.pyqtSignal()

	def __init__(self, login, password, parent = None):
		super().__init__(parent, QtCore.Qt.Window)
		self.ui = settings_panel.Ui_Form()
		self.ui.setupUi(self)
		self.setWindowModality(2)

		self.login = login
		self.password = password

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

		self.bot_settings = get_bot_settings()
		self.user_commands_button_status = False
		self.automati_authorizaton_button_status = False
		self.ui.VKTokenLineEdit.setText(self.bot_settings['VK_Token'])
		self.ui.IDBotLineEdit.setText(self.bot_settings['Group_ID'])
		if self.bot_settings['User_Commands'] == True:
			self.user_commands_button_status = True
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/On.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.UserCommandsButton.setIcon(icon)
		if self.bot_settings['Automati_Authorizaton'] == True:
			self.automati_authorizaton_button_status = True
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/On.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.AutomatiAuthorizatonButton.setIcon(icon)

		# Обработчики основных кнопок
		self.ui.AutomatiAuthorizatonButton.clicked.connect(self.automati_authorizaton_button)
		self.ui.UserCommandsButton.clicked.connect(self.user_commands_button)
		self.ui.ShowVKTokenButton.clicked.connect(self.show_vk_token)
		self.ui.SaveBotSettingsButton.clicked.connect(self.save_bot_settings)

		# Обработчики кнопок с панели
		self.ui.CloseWindowButton.clicked.connect(self.close_window)
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

	def automati_authorizaton_button(self):
		if self.automati_authorizaton_button_status == True:
			self.automati_authorizaton_button_status = False
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/Off.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.AutomatiAuthorizatonButton.setIcon(icon)
		else:
			self.automati_authorizaton_button_status = True
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/On.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.AutomatiAuthorizatonButton.setIcon(icon)

	def user_commands_button(self):
		if self.user_commands_button_status == True:
			self.user_commands_button_status = False
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/Off.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.UserCommandsButton.setIcon(icon)
		else:
			self.user_commands_button_status = True
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/On.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.UserCommandsButton.setIcon(icon)

	def signalButton(self, button):
		if button == 'Да':
			self.save_bot_settings()
		self.message_box.close()

	def close_window(self):
		different_settings = False
		if self.bot_settings['Automati_Authorizaton'] != self.automati_authorizaton_button_status:
			different_settings = True
		elif self.bot_settings['User_Commands'] != self.user_commands_button_status:
			different_settings = True
		elif self.bot_settings['VK_Token'] != self.ui.VKTokenLineEdit.text():
			different_settings = True
		elif self.bot_settings['Group_ID'] != self.ui.IDBotLineEdit.text():
			different_settings = True

		if different_settings == True:
			self.message_box = MessageBox(text = 'Вы изменили настройки, хотите их сохранить?', button_1 = 'Да', button_2 = 'нет')
			self.message_box.signalButton.connect(self.signalButton)
			self.message_box.show()

		self.close()

	def show_vk_token(self):
		if self.ui.VKTokenLineEdit.echoMode() == 2:
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/eyeOff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.ShowVKTokenButton.setIcon(icon)
			self.ui.VKTokenLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
		else:
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/eyeOn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.ShowVKTokenButton.setIcon(icon)
			self.ui.VKTokenLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)

	def save_bot_settings(self):
		with open('Bot-Settings.json', 'w') as file:
			data = {
				'Automati_Authorizaton': self.automati_authorizaton_button_status,
				'User_Commands': self.user_commands_button_status,
				'VK_Token': self.ui.VKTokenLineEdit.text(),
				'Group_ID': self.ui.IDBotLineEdit.text()
			}
			if self.automati_authorizaton_button_status == True:
				data.update(
					{
						'Login': self.login,
						'Password': self.password
					}
				)
			file.write(json.dumps(data, ensure_ascii = False))
		message_box = MessageBox(text = 'Успешное сохранение настроек бота', button_2 = 'Окей')
		message_box.signalButton.connect(lambda: message_box.close())
		message_box.show()

class BotPanel(QtWidgets.QMainWindow): # Окно панель бота
	def __init__(self, login, password, parent = None):
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = bot_panel.Ui_MainWindow()
		self.ui.setupUi(self)

		self.login = login
		self.password = password

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

		if find_file('Logs.txt') == True:
			with open('Logs.txt', 'r') as file:
				logs = file.read().split('\n')
				for text in logs:
					if text != '':
						text = text.split(': ')
						item = QtWidgets.QListWidgetItem()
						self.ui.LogListWidget.setIconSize(QtCore.QSize(45, 45))
						item.setIcon(QtGui.QIcon('../Icons/user.png'))
						item.setTextAlignment(QtCore.Qt.AlignLeft)
						item.setText(f'{text[0]}:\n{text[1]}')
						self.ui.LogListWidget.addItem(item)

		self.bot_settings = get_bot_settings()

		# Обработчики основных кнопок
		self.ui.SaveLogButton.clicked.connect(self.save_logs)
		self.ui.ClearLogButton.clicked.connect(self.clear_logs)
		self.ui.BotSettingsButton.clicked.connect(self.bot_settings_panel)
		self.ui.StartBotButton.clicked.connect(self.start_bot)

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
	def save_logs(self):
		items = []
		for num in range(self.ui.LogListWidget.count()):
			items.append(self.ui.LogListWidget.item(num))
		logs = ''
		for item in items:
			text = ' '.join(item.text().split('\n'))
			logs += f'{text}\n'
		with open('Logs.txt', 'w') as file:
			file.write(logs)

	def clear_logs(self):
		items = []
		for num in range(self.ui.LogListWidget.count()):
			items.append(self.ui.LogListWidget.item(num))
		for item in items:
			self.ui.LogListWidget.takeItem(self.ui.LogListWidget.row(item))
		if find_file('Logs.txt') == True:
			os.remove('Logs.txt')

	def bot_settings_panel(self):
		settings_panel = SettingsPanel(self.login, self.password)
		settings_panel.signalUpdateBotSettings.connect(self.update_bot_settings)
		settings_panel.show()

	def start_bot(self):
		if self.bot_settings['VK_Token'] != '' or self.bot_settings['Group_ID'] != '':
			if self.ui.StartBotButton.text() == 'Запустить бота':
				self.ui.StartBotButton.setText('Выключить бота')
				self.ui.StartBotButton.setStyleSheet("""\
					QPushButton{
						border-radius: 8px;
						background-color: #ed3a2d;
					}

					QPushButton:hover{
						background-color: #c7382e;
					}

					QPushButton:pressed{
						background-color: #b5382f;
					}
				""")
				self.muteTime = MuteTime()
				self.bot = Bot(self.bot_settings['VK_Token'], self.bot_settings['Group_ID'])
				self.bot.signalMuteTime.connect(self.muteTime.start)
				self.bot.signalPrintUserMessage.connect(self.print_user_messgae)
				self.bot.start()
			else:
				self.ui.StartBotButton.setText('Запустить бота')
				self.ui.StartBotButton.setStyleSheet("""\
					QPushButton{
						border-radius: 8px;
						background-color: #75ea00;
					}

					QPushButton:hover{
						background-color: #6fdd00;
					}

					QPushButton:pressed{
						background-color: #62c400;
					}
				""")
				self.bot.longpoll.bot_run = False
		else:
			message_box = MessageBox(text = 'Отсутствует "VK Token" или "ID Group" в настройках!', button_2 = 'Окей')
			message_box.signalButton.connect(lambda: message_box.close())
			message_box.show()
	# ==================================================================

	# Обычные функции
	# ==================================================================
	def update_bot_settings(self):
		self.bot_settings = get_bot_settings()
	# ==================================================================

	# Сигналы QtCore.pyqtSignal
	# ==================================================================
	def print_user_messgae(self, user, message):
		item = QtWidgets.QListWidgetItem()
		self.ui.LogListWidget.setIconSize(QtCore.QSize(45, 45))
		item.setIcon(QtGui.QIcon('../Icons/user.png'))
		item.setTextAlignment(QtCore.Qt.AlignLeft)
		item.setText(f'{user}:\n{message}')
		self.ui.LogListWidget.addItem(item)

# ==================================================================

# VK Бот
# ==================================================================
class Sender:
	def __init__(self, vk_session):
		self.vk_session = vk_session

	def send_message(self, peer_id, message, keyboard = None):
		if keyboard != None:
			self.vk_session.method(
				'messages.send',
				{
					'peer_id': peer_id,
					'message': message,
					'keyboard': keyboard.encode('UTF-8'),
					'random_id': 0
				}
			)
		else:
			self.vk_session.method(
				'messages.send',
				{
					'peer_id': peer_id,
					'message': message,
					'random_id': 0
				}
			)

class Server:
	@staticmethod
	def find(sqlite3_command):
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/database/find', json = {
				'SQLite3_Command': sqlite3_command,
				'Unique_Key': Config.UNIQUE_KEY
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			return server_answer_text['Result']
		else:
			if 'Details' in server_answer_text:
				message_box = MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
				message_box.signalButton.connect(lambda: message_box.close())
				message_box.show()
			else:
				message_box = MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
				message_box.signalButton.connect(lambda: message_box.close())
				message_box.show()

	@staticmethod
	def find_all(sqlite3_command):
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/database/find_all', json = {
				'SQLite3_Command': sqlite3_command,
				'Unique_Key': Config.UNIQUE_KEY
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 200:
			return server_answer_text['Result']
		else:
			if 'Details' in server_answer_text:
				message_box = MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
				message_box.signalButton.connect(lambda: message_box.close())
				message_box.show()
			else:
				message_box = MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
				message_box.signalButton.connect(lambda: message_box.close())
				message_box.show()

	@staticmethod
	def edit_database(sqlite3_command, values = ()):
		server_answer = requests.post(f'{Config.SERVER}/vk_bot/database/edit_database', json = {
				'SQLite3_Command': sqlite3_command,
				'Unique_Key': Config.UNIQUE_KEY,
				'Values': values
			} if values != () else {
				'SQLite3_Command': sqlite3_command,
				'Unique_Key': Config.UNIQUE_KEY
			}
		)
		server_answer_text = json.loads(server_answer.text)
		if server_answer.status_code == 400:
			if 'Details' in server_answer_text:
				message_box = MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
				message_box.signalButton.connect(lambda: message_box.close())
				message_box.show()
			else:
				message_box = MessageBox(text = server_answer_text['Answer'], button_2 = 'Окей')
				message_box.signalButton.connect(lambda: message_box.close())
				message_box.show()

class MyBotLongPool(VkBotLongPoll):
	def listen(self):
		self.bot_run = True
		while self.bot_run:
			try:
				for event in self.check():
					if self.bot_run == True:
						yield event
			except:
				pass

class MuteTime(QtCore.QThread):
	def __init__(self):
		QtCore.QThread.__init__(self)

	def run(self):
		while True:
			for user in Server.find_all("SELECT * FROM Users"):
				mute = json.loads(user[5])
				if mute['Value'] == True:
					now = datetime.datetime.now()
					now = f'{now.day - 1}:{now.hour}:{now.minute}:{now.second}'
					now_time = datetime.datetime.strptime(now, '%d:%H:%M:%S')
					mute_time = datetime.datetime.strptime(mute['Time'], '%d:%H:%M:%S')
					result_time = now_time - mute_time
					result = result_time.days * 24 + result_time.seconds / 3600
					if result >= 2.0:
						Server.edit_database(f"UPDATE Users SET mute = '{json.dumps({'Value': False, 'Time': None, 'Time Left': None})}' WHERE id = '{user[0]}'")
					else:
						Server.edit_database(f"UPDATE Users SET mute = '{json.dumps({'Value': True, 'Time': mute['Time'], 'Time Left': mute['Time Left'] - 1})}' WHERE id = '{user[0]}'")
			time.sleep(60)

class Bot(QtCore.QThread):
	signalMuteTime = QtCore.pyqtSignal()
	signalPrintUserMessage = QtCore.pyqtSignal(str, str)

	def __init__(self, token, group_id):
		QtCore.QThread.__init__(self)

		self.dict_for_warning_func = {}
		self.warning = 0

		self.vk_session = vk_api.VkApi(token = token)
		self.longpoll = MyBotLongPool(self.vk_session, int(group_id))

		self._sender = Sender(self.vk_session)

		Server.edit_database("""
			CREATE TABLE IF NOT EXISTS Users(
				id BIGINT,
				level BIGINT,
				cash BIGINT,
				exp BIGINT,
				rank TEXT,
				mute TEXT
			)
		""")

		self.signalMuteTime.emit()

	def send_command_list(self, peer_id):
		self._sender.send_message(peer_id,  """\
Команды для беседы:
•  !Cписок команд
•  !Статистика [ID пользователя (По умолчанию ваш ID)]
•  !Пожать руку пользователю [ID пользователя]

Команды для личных сообщений:
•  !Мут-чата

PS: Для того, чтобы использовать "Команды для личных сообщений", напишите боту в личные сообщения команду, которую вы хотите использовать.
""")

	def send_statistic(self, id, peer_id, message):
		user_data = self.vk_session.method('users.get',{'user_ids': id, 'fields': 'verified'})[0]
		if len(message.split()) > 1:
			other_id = int(message.split()[1].split('|')[0].replace('[', '').replace('id', '').strip())
			chat_members = self.vk_session.method('messages.getConversationMembers', {'peer_id': peer_id, 'fields': 'verified'})
			other_user_find_in_chat_members = False
			for chat_member in chat_members['items']:
				if other_id == chat_member['member_id']:
					other_user_find_in_chat_members = True
			other_user_data = self.vk_session.method('users.get',{'user_ids': other_id, 'fields': 'verified'})[0]
			other_user = Server.find(f"SELECT * FROM Users WHERE id = '{other_id}'")
			if other_user != None:
				if other_user_find_in_chat_members == True:
					self._sender.send_message(peer_id, f"""\
Имя пользователя: @id{id} ({other_user_data['first_name']} {other_user_data['last_name']})
Ранг пользователя: {other_user[4]}
Балланс пользователя: {other_user[2]}
Уровень пользователя: {other_user[1]}
Опыт пользователя: {other_user[3]}/{other_user[1] * 20}
""")
				else:
					self._sender.send_message(peer_id, f"@id{id} ({user_data['first_name']} {user_data['last_name']}), вы не можете получить статистику пользователя @id{other_id} ({other_user_data['first_name']} {other_user_data['last_name']}), потому-что он не является участником данной беседы!")
			else:
				self._sender.send_message(peer_id, f"@id{id} ({user_data['first_name']} {user_data['last_name']}), пользователя @id{other_id} ({other_user_data['first_name']} {other_user_data['last_name']}) нету в базе данных бота, попробуйте в другой раз!")
		else:
			user = Server.find(f"SELECT * FROM Users WHERE id = '{id}'")
			self._sender.send_message(peer_id, f"""\
Вас зовут: @id{id} ({user_data['first_name']} {user_data['last_name']})
Ваш ранг: {user[4]}
Ваш балланс: {user[2]}
Ваш уровень: {user[1]}
Ваш опыт: {user[3]}/{user[1] * 20}
""")

	def send_mute_chat_time(self, id):
		user_data = self.vk_session.method('users.get',{'user_ids': id, 'fields': 'verified'})[0]
		user = Server.find(f"SELECT * FROM Users WHERE id = '{id}'")
		mute = json.loads(user[5])
		if mute['Value'] == True:
			self._sender.send_message(id, f"@id{id} ({user_data['first_name']} {user_data['last_name']}), вам осталось подождать {mute['Time Left']} мин.")
		else:
			self._sender.send_message(id, f"@id{id} ({user_data['first_name']} {user_data['last_name']}), у вас нету чат-мута!")

	def shake_hands_with_the_user(self, id, peer_id, message):
		if len(message.split()) > 4:
			self._sender.send_message(peer_id, 'Вы неверно ввели команд "!Пожать руку пользователю [ID пользователя]"!\nВот пример: !Пожать руку пользователю 599251585')
		else:
			other_id = int(message.split()[3].split('|')[0].replace('[', '').replace('id', '').strip())
			other_user_data = self.vk_session.method('users.get',{'user_ids': other_id, 'fields': 'verified'})[0]
			user_data = self.vk_session.method('users.get',{'user_ids': id, 'fields': 'verified'})[0]
			chat_members = self.vk_session.method('messages.getConversationMembers', {'peer_id': peer_id, 'fields': 'verified'})
			other_user_find_in_chat_members = False
			for chat_member in chat_members['items']:
				if other_id == chat_member['member_id']:
					other_user_find_in_chat_members = True
			if other_user_find_in_chat_members == True:
				self._sender.send_message(peer_id, f"@id{id} ({user_data['first_name']} {user_data['last_name']}) пожал руку пользователю @id{other_id} ({other_user_data['first_name']} {other_user_data['last_name']})")
			else:
				self._sender.send_message(peer_id, f"@id{id} ({user_data['first_name']} {user_data['last_name']}), вы не можете пожать руку пользователю @id{other_id} ({other_user_data['first_name']} {other_user_data['last_name']}), потому-что он не является участником данной беседы!")

	def new_message(self, event):
		id, peer_id, message = event.obj.from_id, event.obj.peer_id, event.obj.text

		user_data = self.vk_session.method('users.get', {'user_ids': id, 'fields': 'verified'})[0]
		self.signalPrintUserMessage.emit(f"{user_data['first_name']} {user_data['last_name']}", message)

		user = Server.find(f"SELECT * FROM Users WHERE id = '{id}'")
		if user == None:
			user_data = self.vk_session.method('users.get', {'user_ids': id, 'fields': 'verified'})[0]
			self._sender.send_message(peer_id, f"""\
Добро пожаловать @id{id} ({user_data['first_name']} {user_data['last_name']})!
Так как я тебя раньше не видел, попрошу тебя ознакомится с списком команд через команду "!Список команд".
""")
			Server.edit_database("INSERT INTO Users VALUES (?, ?, ?, ?, ?, ?)", values = (id, 1, 0, 0, 'Посвящённый', json.dumps({'Value': False, 'Time': None, 'Time Left': None}, ensure_ascii = False)))
		user = Server.find(f"SELECT * FROM Users WHERE id = '{id}'")

		mute = json.loads(user[5])
		if mute['Value'] == True:
			self.vk_session.method('messages.delete', {'peer_id': peer_id, 'message_ids': event.obj.conversation_message_id, 'spam': 1,})
		elif mute['Value'] == False:
			if peer_id - 2000000000 > 0:
				Server.edit_database(f"UPDATE Users SET exp = '{user[3] + 1}' WHERE id = '{id}'")
				user_data = self.vk_session.method('users.get', {'user_ids': id, 'fields': 'verified'})[0]
				if user[3] + 1 >= user[1] * 20:
					Server.edit_database(f"UPDATE Users SET level = '{user[1] + 1}' WHERE id = '{id}'")
					self._sender.send_message(peer_id, f"Пользователь @id{id} ({user_data['first_name']} {user_data['last_name']}) получил новый уровень!")
					user = Server.find(f"SELECT * FROM Users WHERE id = '{id}'")
				if user[1] in Config.RANKS and Config.RANKS[user[1]] != user[4]:
					Server.edit_database(f"UPDATE Users SET rank = '{Config.RANKS[user[1]]}' WHERE id = '{id}'")
					self._sender.send_message(peer_id, f"Пользователь @id{id} ({user_data['first_name']} {user_data['last_name']}) получает новый ранг \"{Config.RANKS[user[1]]}\"!")

			if len(list(message.strip())) > 1:
				if list(message.strip())[0] == '!':
					try:
						message = ''.join(list(message)[1:len(list(message)) + 1])
						if peer_id - 2000000000 > 0:
							if message.lower() == 'список команд':
								self.send_command_list(peer_id)
							elif message.split()[0].lower() == 'статистика':
								self.send_statistic(id, peer_id, message)
							elif ' '.join(message.split()[:3]).lower() == 'пожать руку пользователю':
								self.shake_hands_with_the_user(id, peer_id, message)
						else:
							if message.lower() == 'мут-чата':
								self.send_mute_chat_time(id)
					except:
						self._sender.send_message(peer_id, f"@id{id} ({user_data['first_name']} {user_data['last_name']}), вы неправильно ввели команду!")

	def run(self):
		for event in self.longpoll.listen():
			if event.type == VkBotEventType.MESSAGE_NEW:
				id, peer_id, message = event.obj.from_id, event.obj.peer_id, event.obj.text
				if peer_id - 2000000000 > 0:
					if peer_id in self.dict_for_warning_func:
						if self.dict_for_warning_func[peer_id][0] == message:
							self.dict_for_warning_func.update({peer_id: [message, self.dict_for_warning_func[peer_id][1] + 1]})
							if self.dict_for_warning_func[peer_id][1] == 3:
								self.dict_for_warning_func.update({peer_id: [message, 1]})
								self.warning += 1
								user_data = self.vk_session.method('users.get',{'user_ids': id, 'fields': 'verified'})[0]
								self._sender.send_message(peer_id, f"""\
@id{id} ({user_data['first_name']} {user_data['last_name']}), хватит флудить!
Вам выдано предупреждение {self.warning}/3.
При достижении 3/3 предупреждений, вы получите мут-чата!
""")
								if self.warning == 3:
									self.warning = 0
									now_time = datetime.datetime.now()
									Server.update_record(f"UPDATE Users SET mute = '{json.dumps({'Value': True, 'Time': f'{now_time.day}:{now_time.hour}:{now_time.minute}:{now_time.second}', 'Time Left': 120}, ensure_ascii = False)}' WHERE id = '{id}'")
									self._sender.send_message(peer_id, f"""\
@id{id} ({user_data['first_name']} {user_data['last_name']}), вы получаете мут-чата на 2 часа за флуд!
Время мута вы можете отслеживать в личных сообщениях у бота, через команду \"!Мут-чата\".
""")
						else:
							self.dict_for_warning_func.update({peer_id: [message, 1]})
					else:
						self.dict_for_warning_func.update({peer_id: [message, 1]})
				self.new_message(event)
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
			with open('Bot-Settings.json', 'w') as file: 
				file.write(json.dumps(bot_settings, ensure_ascii = False))
			myapp = Authorization()
	else:
		myapp = Authorization()
	myapp.show()
	sys.exit(app.exec_())