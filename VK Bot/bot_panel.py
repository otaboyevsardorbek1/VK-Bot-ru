# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

# GUI
import Bot_Panel.bot_panel as bot_panel
from message_box import MessageBox
from settings_panel import SettingsPanel

# Другие
from mute_time import MuteTime
from methods import *
from bot import Bot
import os

# Окно панель бота
class BotPanel(QtWidgets.QMainWindow):
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
			with open('Logs.txt', 'rb') as file:
				logs = file.read().decode('UTF-8').split('\n')
				for text in logs:
					if text != '':
						text = text.split(': ')
						item = QtWidgets.QListWidgetItem()
						self.ui.LogListWidget.setIconSize(QtCore.QSize(45, 45))
						item.setIcon(QtGui.QIcon('../Icons/user.png'))
						item.setTextAlignment(QtCore.Qt.AlignLeft)
						item.setText(f'{text[0]}:\n{text[1]}')
						self.ui.LogListWidget.addItem(item)

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
		with open('Logs.txt', 'wb') as file:
			file.write(logs.encode('UTF-8'))

	def clear_logs(self):
		items = []
		for num in range(self.ui.LogListWidget.count()):
			items.append(self.ui.LogListWidget.item(num))
		for item in items:
			self.ui.LogListWidget.takeItem(self.ui.LogListWidget.row(item))
		if find_file('Logs.txt') == True:
			os.remove('Logs.txt')

	def bot_settings_panel(self):
		bot_settings_panel = SettingsPanel(self.login, self.password)
		bot_settings_panel.show()

	def start_bot(self):
		bot_settings = get_bot_settings()
		if bot_settings['VK_Token'] != '' or bot_settings['Group_ID'] != '':
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
				self.bot = Bot(bot_settings['VK_Token'], bot_settings['Group_ID'])
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

	# Сигналы QtCore.pyqtSignal
	# ==================================================================
	def print_user_messgae(self, user, message):
		item = QtWidgets.QListWidgetItem()
		self.ui.LogListWidget.setIconSize(QtCore.QSize(45, 45))
		item.setIcon(QtGui.QIcon('../Icons/user.png'))
		item.setTextAlignment(QtCore.Qt.AlignLeft)
		item.setText(f'{user}:\n{message}')
		self.ui.LogListWidget.addItem(item)

		bot_settings = get_bot_settings()
		if bot_settings['Automati_Save_Log'] == True:
			self.save_logs()
    # ==================================================================