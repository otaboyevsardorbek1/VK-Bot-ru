# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtGui

# GUI
import Main_Window.User_Bot_Menu_Window.User_Command_Widnow.DB_Variable_Window.db_variable_window as db_variable_window
from message_box import MessageBox

# Другое
import methods as Method
import logging

# Окно выбора значения DB
class DBVariableWindow(Method.CreateFormWindow):
	signalReturnDBVariable = QtCore.pyqtSignal(str)

	def __init__(self, bot_name, db_variable_type, parent=None):
		super().__init__(parent)
		self.ui = db_variable_window.Ui_Form()
		self.ui.setupUi(self)

		# Запись в логи программы
		logging.debug(f'{bot_name} - Окно выбора значения DB.')

		# Все нужные переменные
		self.bot_name = bot_name
		self.db_variable_type = db_variable_type
		self.select_button = None

		# Обработчик основной кнопки
		self.ui.UserLevelButton.clicked.connect(self.user_level_button)
		self.ui.UserBalanceButton.clicked.connect(self.user_balance_button)
		self.ui.UserExperienceButton.clicked.connect(self.user_experience_button)
		self.ui.SelectDBVariableButton.clicked.connect(self.select_db_variable_button)

		# Обработчики кнопок с панели
		self.ui.CloseWindowButton.clicked.connect(self.close_window_button)
		self.ui.MinimizeWindowButton.clicked.connect(lambda: self.showMinimized())

	# Логика основной кнопки
	# ==================================================================
	def close_window_button(self):
		logging.debug('Выход из окна выбора значения DB.')
		self.close()

	def user_level_button(self):
		button_value = Method.on_or_off_func(self.select_button == self.ui.UserLevelButton, self.ui.UserLevelButton)
		if button_value == False:
			self.select_button = None
		else:
			self.select_button = self.ui.UserLevelButton

		self.clear_all_buttons()

	def user_balance_button(self):
		button_value = Method.on_or_off_func(self.select_button == self.ui.UserBalanceButton, self.ui.UserBalanceButton)
		if button_value == False:
			self.select_button = None
		else:
			self.select_button = self.ui.UserBalanceButton

		self.clear_all_buttons()

	def user_experience_button(self):
		button_value = Method.on_or_off_func(self.select_button == self.ui.UserExperienceButton, self.ui.UserExperienceButton)
		if button_value == False:
			self.select_button = None
		else:
			self.select_button = self.ui.UserExperienceButton

		self.clear_all_buttons()

	def select_db_variable_button(self):
		text, num = None, 1
		buttons = [
			self.ui.UserLevelButton,
			self.ui.UserBalanceButton,
			self.ui.UserExperienceButton
		]
		for button in buttons:
			if self.select_button == button:
				text = '{' + self.db_variable_type + '[' + str(num) + ']}'
			num += 1
		if text != None:
			logging.debug(f'{self.bot_name} - Пользователь выбрал значения DB {self.db_variable_type}.')
			self.signalReturnDBVariable.emit(text)
			self.close()
		else:
			MessageBox(text = f'Вы не выбрали значение для {{self.db_variable_type}}!', button_1 = 'Щас исправлю...')
	# ==================================================================

	# Обычные функции
	# ==================================================================
	def clear_all_buttons(self):
		buttons = [
			self.ui.UserLevelButton,
			self.ui.UserBalanceButton,
			self.ui.UserExperienceButton
		]
		for button in buttons:
			if self.select_button != button:
				icon = QtGui.QIcon()
				icon.addPixmap(QtGui.QPixmap("../Icons/iconOff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
				button.setIcon(icon)
	# ==================================================================