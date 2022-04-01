# -*- coding: utf-8 -*-

# GUI
import Main_Window.Program_Info_Window.program_info_window as program_info_window

# Другое
import methods as Method
import config as Config
import webbrowser
import logging

# Окно информации о проекте
class ProgramInfoWindow(Method.CreateFormWindow):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.ui = program_info_window.Ui_Form()
		self.ui.setupUi(self)

		# Запись в логи программы
		logging.debug('Окно информации о проекте.')

		# Настройка виджетов
		self.ui.VersionLinkButton.setText(Config.VERSION)

		# Обработчики основных кнопок
		self.ui.VersionLinkButton.clicked.connect(lambda: webbrowser.open(f'https://github.com/EXG1O/VK-Bot/releases/tag/{Config.VERSION}'))
		self.ui.PublicLinkButton.clicked.connect(lambda: webbrowser.open('https://vk.com/software_on_python'))
		self.ui.AuthorLinkButton.clicked.connect(lambda: webbrowser.open('https://vk.com/id599251585'))

		# Обработчики кнопок с панели
		self.ui.CloseWindowButton.clicked.connect(lambda: self.close())
		self.ui.MinimizeWindowButton.clicked.connect(lambda: self.showMinimized())

		# Запуск окна информации о проекте
		self.show()

	# Логика основной кнопки
	# ==================================================================
	def close_window_button(self):
		logging.debug('Выход из окна информации о проекте.')
		self.close()
	# ==================================================================