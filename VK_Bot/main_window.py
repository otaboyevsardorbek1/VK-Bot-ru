# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtGui, QtWidgets

# GUI
from program_info_window import ProgramInfoWindow
import Main_Window.main_window as main_window
from user_bot_menu_window import UserBotMenuWindow
from add_new_user_bot_window import AddNewUserBotWindow
from message_box import MessageBox

# Другие
import global_variables as GlobalVariables
import methods as Method
import server as Server
from bot import Bot
import logging

# Главное окно
class MainWindow(Method.CreateMainWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.ui = main_window.Ui_MainWindow()
		self.ui.setupUi(self)

		# Запись в логи программы
		logging.debug('Главное окно.')

		# Запуск потока
		self.widget_settings_theard = WidgetSettingsTheard()
		self.widget_settings_theard.signalWidgetSettings.connect(self.widget_settings)
		self.widget_settings_theard.start()

		# Обработчики основных кнопок
		self.ui.UserBotMenuButton.clicked.connect(self.user_bot_menu_window_button)
		self.ui.AddUserBotButton.clicked.connect(self.add_new_user_bot_window_button)
		self.ui.DeleteUserBotButton.clicked.connect(self.delete_user_bot_button)

		# Обработчики кнопок с панели
		self.ui.ProgramInfoWindowButton.clicked.connect(lambda: ProgramInfoWindow())
		self.ui.CloseWindowButton.clicked.connect(self.close_window_button)
		self.ui.MinimizeWindowButton.clicked.connect(lambda: self.showMinimized())

	# Декораторы
	# ==================================================================
	def check_selected_user_bot(func):
		def wrapper(self):
			items = self.ui.UserBotListWidget.selectedItems()
			if len(items) == 1:
				bot_name = items[0].text().split(': ')[0]
				func(self, bot_name, items[0])
			else:
				MessageBox(text='Вы не выбрали бота из списка ботов!', button_1='Щас выберу...')
		wrapper.__name__ = func.__name__
		return wrapper
	# ==================================================================

	# Логика основных кнопок
	# ==================================================================
	def close_window_button(self):
		logging.debug('Выход из главного окна.')
		self.close()

	@check_selected_user_bot
	def user_bot_menu_window_button(self, bot_name: str, item: QtWidgets.QListWidgetItem):
		logging.debug('Переход в меню бота.')
		self.user_bot_menu_window = UserBotMenuWindow(bot_name, item)
		self.user_bot_menu_window.signalStartBot.connect(self.start_bot)
		self.user_bot_menu_window.show()

		logging.debug('Добавление бота в глобальную переменную "user_bot_menu_window_online_dict".')
		GlobalVariables.user_bot_menu_window_online_dict.update({bot_name: self.user_bot_menu_window})

	def add_new_user_bot_window_button(self):
		logging.debug('Переход в окно добавления бота.')
		self.add_new_user_bot_window = AddNewUserBotWindow()
		self.add_new_user_bot_window.signalReturnNewUserBot.connect(self.add_user_bot)
		self.add_new_user_bot_window.show()

	@check_selected_user_bot
	def delete_user_bot_button(self, bot_name: str, item: QtWidgets.QListWidgetItem):
		if bot_name not in GlobalVariables.online_bot_dict:
			server_answer_status_code = Server.delete_user_bot(bot_name)
			if server_answer_status_code == 200:
				logging.debug(f'Успешное удаление бота {bot_name}.')
				self.ui.UserBotListWidget.takeItem(self.ui.UserBotListWidget.row(item))
				MessageBox(text='Вы успешно удалили бота.', button_2='Окей')
		else:
			MessageBox(text='Сначала выключите бота!', button_1='Окей')
	# ==================================================================

	# Сигналы QtCore.pyqtSignal
	# ==================================================================
	def widget_settings(self, user_bot_list: list):
		for user_bot in user_bot_list:
			item = QtWidgets.QListWidgetItem()
			item.setTextAlignment(QtCore.Qt.AlignLeft)
			item.setText(f'{user_bot}: выключен')
			self.ui.UserBotListWidget.addItem(item)

	def add_user_bot(self, user_bot: str):
		item = QtWidgets.QListWidgetItem()
		item.setTextAlignment(QtCore.Qt.AlignLeft)
		item.setText(f'{user_bot}: выключен')
		self.ui.UserBotListWidget.addItem(item)

	def start_bot(self, vk_token: str, id_bot: str, bot_name: str):
		logging.debug(f'Включение бота {bot_name}.')
		self.bot = Bot(vk_token, id_bot, bot_name)
		self.bot.signalPrintUserMessage.connect(self.print_user_message)
		self.bot.start()

		logging.debug('Добавление бота в глобальную переменную "online_bot_dict".')
		GlobalVariables.online_bot_dict.update({bot_name: self.bot})

	def print_user_message(self, bot_name: str, user: str, message: str):
		logging.debug(f'{bot_name} - Новое сообщение от пользователя {user}: {message}.')

		def save_log(log, bot_settings):
			if bot_settings['Automati_Save_Log'] == True:
				logging.debug(f'{bot_name} - Сохранения сообщения пользователя {user} в логи бота {bot_name}.')
				log.append(f'{user}: {message}')
				Server.update_log(bot_name, log)
			GlobalVariables.new_user_message = False

		self.return_bot_settings_and_log_theard = ReturnBotSettingsAndLog(bot_name)
		self.return_bot_settings_and_log_theard.signalReturnBotSettingsAndLog.connect(save_log)
		self.return_bot_settings_and_log_theard.start()

		if bot_name in GlobalVariables.user_bot_menu_window_online_dict:
			logging.debug(f'{bot_name} - Отрисовка сообщения пользователя {user} в окне меню бота {bot_name}.')
			item = QtWidgets.QListWidgetItem()
			item.setIcon(QtGui.QIcon('../Icons/user.png'))
			item.setTextAlignment(QtCore.Qt.AlignLeft)
			item.setText(f'{user}:\n{message}')
			GlobalVariables.user_bot_menu_window_online_dict[bot_name].ui.LogListWidget.setIconSize(QtCore.QSize(45, 45))
			GlobalVariables.user_bot_menu_window_online_dict[bot_name].ui.LogListWidget.addItem(item)
	# ==================================================================

# Поток для настрйоки виджетов
class WidgetSettingsTheard(QtCore.QThread):
	signalWidgetSettings = QtCore.pyqtSignal(list)

	def __init__(self):
		QtCore.QThread.__init__(self)

	def run(self):
		user_bot_list = Server.get_user_bot_list()
		self.signalWidgetSettings.emit(user_bot_list)

# Поток для получения настроек бота и логов бота
class ReturnBotSettingsAndLog(QtCore.QThread):
	signalReturnBotSettingsAndLog = QtCore.pyqtSignal(list, dict)

	def __init__(self, bot_name):
		QtCore.QThread.__init__(self)

		self.bot_name = bot_name

	def run(self):
		log = Server.get_log(self.bot_name)
		bot_settings = Server.get_bot_settings(self.bot_name)
		self.signalReturnBotSettingsAndLog.emit(log, bot_settings)