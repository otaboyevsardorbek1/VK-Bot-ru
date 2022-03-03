# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets
from flask import Config

# GUI
import Main_Window.main_window as main_window
from message_box import MessageBox
from settings_widnow import SettingsWindow

# Другие
import server as Server
import config as Config
from bot import Bot, MuteTime

# Окно панель бота
class MainWindow(QtWidgets.QMainWindow):
	def __init__(self, parent = None):
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = main_window.Ui_MainWindow()
		self.ui.setupUi(self)

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

		# Вывод логов в "self.ui.LogListWidget"
		log = Server.get_log()
		if log != []:
			for text in log:
				if text != '':
					text = text.split(': ')
					item = QtWidgets.QListWidgetItem()
					self.ui.LogListWidget.setIconSize(QtCore.QSize(45, 45))
					item.setIcon(QtGui.QIcon('../Icons/user.png'))
					item.setTextAlignment(QtCore.Qt.AlignLeft)
					item.setText(f'{text[0]}:\n{text[1]}')
					self.ui.LogListWidget.addItem(item)

		# Обработчики основных кнопок
		self.ui.SaveLogButton.clicked.connect(lambda: self.save_log())
		self.ui.ClearLogButton.clicked.connect(self.clear_log_button)
		self.ui.SettingsWindowButton.clicked.connect(self.settings_window_button)
		self.ui.OnOrOffBotButton.clicked.connect(self.on_or_off_bot_button)

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
	def clear_log_button(self):
		items = []
		for num in range(self.ui.LogListWidget.count()):
			items.append(self.ui.LogListWidget.item(num))

		for item in items:
			self.ui.LogListWidget.takeItem(self.ui.LogListWidget.row(item))
		Server.update_log([])

	def settings_window_button(self):
		settings_window = SettingsWindow()
		settings_window.show()

	def on_or_off_bot_button(self):
		bot_settings = Server.get_bot_settings()
		if bot_settings['VK_Token'] != '' or bot_settings['Group_ID'] != '':
			if self.ui.OnOrOffBotButton.text() == 'Запустить бота':
				self.ui.OnOrOffBotButton.setText('Выключить бота')
				self.ui.OnOrOffBotButton.setStyleSheet(Config.ON_BUTTON)

				self.mute_time = MuteTime()
				self.mute_time.start()

				self.bot = Bot(bot_settings['VK_Token'], bot_settings['Group_ID'])
				self.bot.signalPrintUserMessage.connect(self.print_user_message)
				self.bot.start()
			else:
				self.ui.OnOrOffBotButton.setText('Запустить бота')
				self.ui.OnOrOffBotButton.setStyleSheet(Config.OFF_BUTTON)

				self.mute_time.mute_time_theard_run = False
				self.bot.longpoll.bot_theard_run = False
		else:
			MessageBox(text = 'Отсутствует "VK Token" или "ID Group" в настройках!', button_2 = 'Окей')
	# ==================================================================

	# Обычные функции
	# ==================================================================
	def save_log(self):
		items = []
		for num in range(self.ui.LogListWidget.count()):
			items.append(self.ui.LogListWidget.item(num))

		log = []
		for item in items:
			text = ' '.join(item.text().split('\n'))
			log.append(text)
		Server.update_log(log)
	# ==================================================================

	# Сигналы QtCore.pyqtSignal
	# ==================================================================
	def print_user_message(self, user, message):
		item = QtWidgets.QListWidgetItem()
		self.ui.LogListWidget.setIconSize(QtCore.QSize(45, 45))
		item.setIcon(QtGui.QIcon('../Icons/user.png'))
		item.setTextAlignment(QtCore.Qt.AlignLeft)
		item.setText(f'{user}:\n{message}')
		self.ui.LogListWidget.addItem(item)

		bot_settings = Server.get_bot_settings()
		if bot_settings['Automati_Save_Log'] == True:
			self.save_log()
    # ==================================================================