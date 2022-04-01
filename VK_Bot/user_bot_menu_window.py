# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

# GUI
import Main_Window.User_Bot_Menu_Window.user_bot_menu_window as user_bot_menu_window
from program_info_window import ProgramInfoWindow
from user_command_window import UserCommandWindow
from message_box import MessageBox

# Другое
import global_variables as GlobalVariables
import methods as Method
import server as Server
import config as Config
import logging

# Окно меню бота
class UserBotMenuWindow(Method.CreateFormWindow):
	signalStartBot = QtCore.pyqtSignal(str, str, str)

	def __init__(self, bot_name, item, parent=None):
		super().__init__(parent)
		self.ui = user_bot_menu_window.Ui_Form()
		self.ui.setupUi(self)

		# Запись в логи программы
		logging.debug(f'{bot_name} - Окно меню бота {bot_name}.')

		# Все нужные переменные
		self.bot_name = bot_name
		self.item = item
		self.automati_save_log_button_status = False

		# Настройка основной кнопки
		if self.bot_name in GlobalVariables.online_bot_dict:
			self.ui.UserBotButton.setText('Выключить бота')
			self.ui.UserBotButton.setStyleSheet(Config.ON_BUTTON)
		else:
			self.ui.UserBotButton.setText('Включить бота')
			self.ui.UserBotButton.setStyleSheet(Config.OFF_BUTTON)

		# Запуск потока
		self.widget_settings_theard = WidgetSettingsTheard(self.bot_name)
		self.widget_settings_theard.signalWidgetSettings.connect(self.widget_settings)
		self.widget_settings_theard.start()

		# Обработчики основных кнопок
		self.ui.ProgramInfoWindowButton.clicked.connect(lambda: ProgramInfoWindow())
		self.ui.SaveBotSettingsButton.clicked.connect(self.save_bot_settings_button)
		self.ui.ShowVKTokenButton.clicked.connect(lambda: Method.show_or_hide_text(self, self.ui.VKTokenLineEdit, self.ui.ShowVKTokenButton))
		self.ui.UserBotButton.clicked.connect(self.start_or_stop_bot_button)
		self.ui.AutomatiSaveLogButton.clicked.connect(self.automati_save_log_button)
		self.ui.SaveLogButton.clicked.connect(self.save_log)
		self.ui.ClearLogButton.clicked.connect(self.clear_log_button)
		self.ui.AddUserCommandButton.clicked.connect(self.add_new_user_command_button)
		self.ui.EditUserCommandButton.clicked.connect(self.edit_user_command_button)
		self.ui.DeleteUserCommandButton.clicked.connect(self.remove_user_command_button)

		# Обработчики кнопок с панели
		self.ui.CloseWindowButton.clicked.connect(self.close_window_button)
		self.ui.MinimizeWindowButton.clicked.connect(lambda: self.showMinimized())

	# Декораторы
	# ==================================================================
	def check_selected_user_command(func):
		def wrapper(self):
			items = self.ui.UserCommandsListWidget.selectedItems()
			if len(items) == 1:
				item = items[0]
				func(self, item)
			else:
				MessageBox(text='Вы не выбрали команду из списка команд!', button_1='Щас исправлю...')
		wrapper.__name__ = func.__name__
		return wrapper
	# ==================================================================

	# Логика основных кнопок
	# ==================================================================
	def close_window_button(self):
		def save_bot_settings_button_signal(self, message_box, text):
			message_box.close()
			if text == 'Да':
				self.save_bot_settings_button()
			del GlobalVariables.user_bot_menu_window_online_dict[self.bot_name]
			logging.debug(f'{self.bot_name} - Выход из окна меню бота {self.bot_name}.')
			self.close()

		if self.check_different_settings() == True:
			message_box = MessageBox(text='Вы изменили настройки бота, сохранить их?', button_1='Да', button_2='Нет')
			message_box.message_box.signalButton.connect(lambda text: save_bot_settings_button_signal(self, message_box.message_box, text))
		else:
			logging.debug(f'{self.bot_name} - Удаление бота {self.bot_name} из глобальной переменной "user_bot_menu_window_online_dict".')
			del GlobalVariables.user_bot_menu_window_online_dict[self.bot_name]
			logging.debug(f'{self.bot_name} - Выход из окна меню бота {self.bot_name}.')
			self.close()

	def save_bot_settings_button(self):
		bot_name = self.ui.UserBotNameLineEdit.text()
		if bot_name != '':
			logging.debug(f'{self.bot_name} - Успешное сохранение настроек бота {self.bot_name}.')
			self.bot_settings = {
				'Automati_Save_Log': self.automati_save_log_button_status,
				'Bot_Name': bot_name,
				'VK_Token': self.ui.VKTokenLineEdit.text(),
				'Group_ID': self.ui.IDBotLineEdit.text()
			}
			Server.update_bot_settings(self.bot_name, self.bot_settings)
			MessageBox(text='Успешное сохранение настроек бота', button_2='Окей')
		else:
			MessageBox(text='Придумайте сначала имя боту!', button_1='Окей')

	def start_or_stop_bot_button(self):
		def start_or_stop_bot(self):
			vk_token = self.ui.VKTokenLineEdit.text()
			id_bot = self.ui.IDBotLineEdit.text()
			if vk_token != '' or id_bot != '':
				if self.ui.UserBotButton.text() == 'Включить бота':
					logging.debug(f'{self.bot_name} - Бот {self.bot_name} включен.')
					self.ui.UserBotButton.setText('Выключить бота')
					self.ui.UserBotButton.setStyleSheet(Config.ON_BUTTON)
					self.item.setText(f'{self.bot_name}: включен')

					self.signalStartBot.emit(vk_token, id_bot, self.bot_name)
				else:
					logging.debug(f'{self.bot_name} - Бот {self.bot_name} выключен.')
					self.ui.UserBotButton.setText('Включить бота')
					self.ui.UserBotButton.setStyleSheet(Config.OFF_BUTTON)
					self.item.setText(f'{self.bot_name}: выключен')

					GlobalVariables.online_bot_dict[self.bot_name].longpoll.bot_theard_run = False
					logging.debug(f'{self.bot_name} - Удаление бота {self.bot_name} из глобальной переменной "online_bot_dict".')
					del GlobalVariables.online_bot_dict[self.bot_name]
			else:
				MessageBox(text='Отсутствует значение полей "VK Token" или "ID Group"!', button_2='Окей')

		def save_bot_settings_button_signal(self, message_box, text):
			message_box.close()
			if text == 'Да':
				self.save_bot_settings_button()
			start_or_stop_bot(self)

		if self.check_different_settings() == True and self.ui.UserBotButton.text() == 'Включить бота':
			message_box = MessageBox(text='Вы изменили настройки бота, сохранить их?', button_1='Да', button_2='Нет')
			message_box.message_box.signalButton.connect(lambda text: save_bot_settings_button_signal(self, message_box.message_box, text))
		else:
			start_or_stop_bot(self)

	def automati_save_log_button(self):
		icon = QtGui.QIcon()
		if self.automati_save_log_button_status == True:
			self.automati_save_log_button_status = False
			icon.addPixmap(QtGui.QPixmap("../Icons/iconOff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.AutomatiSaveLogButton.setIcon(icon)
		else:
			self.automati_save_log_button_status = True
			icon.addPixmap(QtGui.QPixmap("../Icons/iconOn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.AutomatiSaveLogButton.setIcon(icon)

	def save_log(self):
		items = []
		for num in range(self.ui.LogListWidget.count()):
			items.append(self.ui.LogListWidget.item(num))
		log = []
		for item in items:
			text = ' '.join(item.text().split('\n'))
			log.append(text)
		Server.update_log(self.bot_name, log)
		logging.debug(f'{self.bot_name} - Успешное сохранения логов бота {self.bot_name}.')
		MessageBox(text='Успешное сохранение логов бота.', button_1='Окей')

	def clear_log_button(self):
		items = []
		for num in range(self.ui.LogListWidget.count()):
			items.append(self.ui.LogListWidget.item(num))
		for item in items:
			self.ui.LogListWidget.takeItem(self.ui.LogListWidget.row(item))
		Server.update_log(self.bot_name, [])
		logging.debug(f'{self.bot_name} - Успешная очистка логов бота {self.bot_name}.')
		MessageBox(text='Успешная очистка логов бота.', button_1='Окей')

	def add_new_user_command_button(self):
		logging.debug(f'{self.bot_name} - Переход в окно создания новой пользоватской команды.')
		self.add_new_user_command_window = UserCommandWindow('Создать команду', self.bot_name)
		self.add_new_user_command_window.signalAddNewUserCommand.connect(self.add_new_user_command)
		self.add_new_user_command_window.show()

	@check_selected_user_command
	def edit_user_command_button(self, item: QtWidgets.QListWidgetItem):
		logging.debug(f'{self.bot_name} - Переход в окно редактирования пользоватской команды.')
		self.edit_user_command_window = UserCommandWindow('Редактировать команду', self.bot_name, item=item)
		self.edit_user_command_window.show()

	@check_selected_user_command
	def remove_user_command_button(self, item: QtWidgets.QListWidgetItem):
		user_commands = Server.get_user_commands(self.bot_name)
		old_user_command = item.text().replace('Команда: ', '').strip()

		user_command_value = 0
		for user_command in user_commands:
			if user_command['Command_Name'] == old_user_command: 
				break
			user_command_value += 1
		del user_commands[user_command_value]
		Server.update_user_commands(self.bot_name, user_commands)

		logging.debug(f'{self.bot_name} - Успешное удаление пользоватской команды.')
		self.ui.UserCommandsListWidget.takeItem(self.ui.UserCommandsListWidget.row(item))
		MessageBox(text='Вы успешно удалили пользоватскую команду.', button_1='Окей')
	# ==================================================================

	# Обычные функции
	# ==================================================================
	def check_different_settings(self):
		different_settings = False
		if self.bot_settings['Automati_Save_Log'] != self.automati_save_log_button_status:
			different_settings = True
		elif self.bot_settings['VK_Token'] != self.ui.VKTokenLineEdit.text():
			different_settings = True
		elif self.bot_settings['Group_ID'] != self.ui.IDBotLineEdit.text():
			different_settings = True
		return different_settings
	# ==================================================================

	# Сигналы QtCore.pyqtSignal
	# ==================================================================
	def widget_settings(self, log: list, user_commands: list, bot_settings: dict):
		self.bot_settings = bot_settings
		self.ui.UserBotNameLineEdit.setText(self.bot_name)
		self.ui.UserBotNameLineEdit.setDisabled(True)
		self.ui.VKTokenLineEdit.setText(self.bot_settings['VK_Token'])
		self.ui.IDBotLineEdit.setText(self.bot_settings['Group_ID'])

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

		if self.bot_settings['Automati_Save_Log'] == True:
			self.automati_save_log_button_status = True
			icon = QtGui.QIcon()
			icon.addPixmap(QtGui.QPixmap("../Icons/iconOn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
			self.ui.AutomatiSaveLogButton.setIcon(icon)
		else:
			self.automati_save_log_button_status = False

	def add_new_user_command(self, new_command: dict):
		item = QtWidgets.QListWidgetItem()
		item.setTextAlignment(QtCore.Qt.AlignLeft)
		item.setText(new_command['Command_Name'])
		self.ui.UserCommandsListWidget.addItem(item)
	# ==================================================================

# Поток для настрйоки виджетов
class WidgetSettingsTheard(QtCore.QThread):
	signalWidgetSettings = QtCore.pyqtSignal(list, list, dict)

	def __init__(self, bot_name):
		QtCore.QThread.__init__(self)

		self.bot_name = bot_name

	def run(self):
		log = Server.get_log(self.bot_name)
		user_commands = Server.get_user_commands(self.bot_name)
		bot_settings = Server.get_bot_settings(self.bot_name)
		self.signalWidgetSettings.emit(log, user_commands, bot_settings)