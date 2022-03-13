# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtWidgets

# GUI
import Main_Window.Program_Info_Window.program_info_window as program_info_window

# Другое
import config as Config
import webbrowser

# Окно настроек бота
class ProgramInfoWindow(QtWidgets.QMainWindow):
	def __init__(self, parent = None):
		super().__init__(parent, QtCore.Qt.Window)
		self.ui = program_info_window.Ui_Form()
		self.ui.setupUi(self)
		self.setWindowModality(2)

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

		# Настройка виджетов
		self.ui.VersionLinkButton.setText(Config.VERSION)

		# Обработчики основных кнопок
		self.ui.VersionLinkButton.clicked.connect(lambda: webbrowser.open(f'https://github.com/EXG1O/VK-Bot/releases/tag/{Config.VERSION}'))
		self.ui.PublicLinkButton.clicked.connect(lambda: webbrowser.open('https://vk.com/software_on_python'))
		self.ui.AuthorLinkButton.clicked.connect(lambda: webbrowser.open('https://vk.com/id599251585'))

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