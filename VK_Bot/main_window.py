# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

# GUI
import Main_Window.main_window as main_window
from user_command_window import UserCommandWindow
from settings_widnow import SettingsWindow
from program_info_window import ProgramInfoWindow
from message_box import MessageBox

# Другие
import server as Server
import config as Config
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

		# Запуск потоков
		self.widget_settings_theard = WidgetSettingsTheard()
		self.widget_settings_theard.signalWidgetSettings.connect(self.widget_settings)
		self.widget_settings_theard.start()

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
	def settings_window_button(self):
		self.settings_window = SettingsWindow()
		self.settings_window.show()

	def program_info_window_button(self):
		self.program_info_window = ProgramInfoWindow()
		self.program_info_window.show()

	def clear_log_button(self):
		items = []
		for num in range(self.ui.LogListWidget.count()):
			items.append(self.ui.LogListWidget.item(num))

		for item in items:
			self.ui.LogListWidget.takeItem(self.ui.LogListWidget.row(item))
		Server.update_log([])

	def on_or_off_bot_button(self):
		bot_settings = Server.get_bot_settings()
		if bot_settings['VK_Token'] != '' or bot_settings['Group_ID'] != '':
			if self.ui.OnOrOffBotButton.text() == 'Запустить бота':
				self.ui.OnOrOffBotButton.setText('Выключить бота')
				self.ui.OnOrOffBotButton.setStyleSheet(Config.ON_BUTTON)

				self.bot = Bot(bot_settings['VK_Token'], bot_settings['Group_ID'])
				self.bot.signalPrintUserMessage.connect(self.print_user_message)
				self.bot.start()
			else:
				self.ui.OnOrOffBotButton.setText('Запустить бота')
				self.ui.OnOrOffBotButton.setStyleSheet(Config.OFF_BUTTON)

				self.bot.longpoll.bot_theard_run = False
		else:
			MessageBox(text = 'Отсутствует "VK Token" или "ID Group" в настройках!', button_2 = 'Окей')

	def add_new_user_command_window_button(self):
		self.add_new_user_command_window = UserCommandWindow(button_text = 'Создать команду')
		self.add_new_user_command_window.signalAddNewUserCommand.connect(self.add_new_user_command)
		self.add_new_user_command_window.show()

	def edit_user_command_window_button(self):
		item = self.ui.UserCommandsListWidget.selectedItems()
		if len(item) == 0:
			MessageBox(text = 'Вы не выбрали команду, которую хотите изменить!', button_1 = 'Щас исправлю...')
		elif len(item) == 1:
			item = item[0]
			self.edit_user_command_window = UserCommandWindow(button_text = 'Редактировать команду', item = item)
			self.edit_user_command_window.show()

	def remove_user_command_button(self):
		item = self.ui.UserCommandsListWidget.selectedItems()
		if len(item) == 0:
			MessageBox(text = 'Вы не выбрали команду, которую хотите удалить!', button_1 = 'Щас исправлю...')
		elif len(item) == 1:
			item = item[0]

			old_user_command = item.text().replace('Команда: ', '').strip()
			user_commands = Server.get_user_commands()

			user_command_value = 0
			for user_command in user_commands:
				if user_command['Command_Name'] == old_user_command: 
					break
				user_command_value += 1
			del user_commands[user_command_value]

			Server.update_user_commands(user_commands)

			self.ui.UserCommandsListWidget.takeItem(self.ui.UserCommandsListWidget.row(item))

			MessageBox(text = 'Вы успешно удалили пользоватскую команду.', button_1 = 'Окей')
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
	def widget_settings(self, log, user_commands):
		# Настройка виджетов
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

		for user_command in user_commands:
			item = QtWidgets.QListWidgetItem()
			item.setTextAlignment(QtCore.Qt.AlignLeft)
			item.setText(user_command['Command_Name'])
			self.ui.UserCommandsListWidget.addItem(item)

		# Обработчики основных кнопок
		self.ui.SettingsWindowButton.clicked.connect(self.settings_window_button)
		self.ui.ProgramInfoWindowButton.clicked.connect(self.program_info_window_button)
		self.ui.SaveLogButton.clicked.connect(lambda: self.save_log())
		self.ui.ClearLogButton.clicked.connect(self.clear_log_button)
		self.ui.OnOrOffBotButton.clicked.connect(self.on_or_off_bot_button)
		self.ui.AddUserCommandButton.clicked.connect(self.add_new_user_command_window_button)
		self.ui.EditUserCommandButton.clicked.connect(self.edit_user_command_window_button)
		self.ui.DeleteUserCommandButton.clicked.connect(self.remove_user_command_button)

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
	
	def add_new_user_command(self, new_command):
		item = QtWidgets.QListWidgetItem()
		item.setTextAlignment(QtCore.Qt.AlignLeft)
		item.setText(new_command['Command_Name'])
		self.ui.UserCommandsListWidget.addItem(item)
    # ==================================================================

# Поток для настрйоки виджетов
class WidgetSettingsTheard(QtCore.QThread):
	signalWidgetSettings = QtCore.pyqtSignal(list, list)

	def __init__(self):
		QtCore.QThread.__init__(self)

	def run(self):
		log = Server.get_log()
		user_commands = Server.get_user_commands()
		self.signalWidgetSettings.emit(log, user_commands)