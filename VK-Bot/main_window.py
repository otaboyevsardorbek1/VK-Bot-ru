# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

# GUI
import Main_Window.main_window as main_window
from message_box import MessageBox
from settings_panel_widnow import SettingsPanelWindow

# Другие
from mute_time import MuteTime
import server as Server
from bot import Bot

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
		self.ui.SaveLogButton.clicked.connect(self.save_log)
		self.ui.ClearLogButton.clicked.connect(self.clear_log)
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
	def save_log(self):
		items = []
		for num in range(self.ui.LogListWidget.count()):
			items.append(self.ui.LogListWidget.item(num))
		log = []
		for item in items:
			text = ' '.join(item.text().split('\n'))
			log.append(text)

		Server.update_log(log)

	def clear_log(self):
		items = []
		for num in range(self.ui.LogListWidget.count()):
			items.append(self.ui.LogListWidget.item(num))
		for item in items:
			self.ui.LogListWidget.takeItem(self.ui.LogListWidget.row(item))
		Server.update_log([])

	def bot_settings_panel(self):
		bot_settings_panel = SettingsPanelWindow()
		bot_settings_panel.show()

	def start_bot(self):
		bot_settings = Server.get_bot_settings()
		if bot_settings['VK_Token'] != '' or bot_settings['Group_ID'] != '':
			if self.ui.StartBotButton.text() == 'Запустить бота':
				self.ui.StartBotButton.setText('Выключить бота')
				self.ui.StartBotButton.setStyleSheet("""\
					QPushButton{
						border-radius: 8px;
						background-color: #EA4100;
					}

					QPushButton:hover{
						background-color: #DF3E00;
					}

					QPushButton:pressed{
						background-color: #CA3700;
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
						background-color: #92E604;
					}

					QPushButton:hover{
						background-color: #8BDC03;
					}

					QPushButton:pressed{
						background-color: #7DC802;
					}
				""")
				self.bot.longpoll.bot_run = False
		else:
			MessageBox(text = 'Отсутствует "VK Token" или "ID Group" в настройках!', button_2 = 'Окей')
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

		bot_settings = Server.get_bot_settings()
		if bot_settings['Automati_Save_Log'] == True:
			self.save_log()
    # ==================================================================