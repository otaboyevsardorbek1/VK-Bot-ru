# -*- coding: utf-8 -*-

# PyQt5
from PyQt5 import QtCore, QtWidgets

# GUI
import Main_Window.Rank_System_Window.rank_system_window as rank_system_window
from message_box import MessageBox

# Другие
import server as Server

# Окно системы рангов
class RankSystemWindow(QtWidgets.QMainWindow):
	def __init__(self, parent = None):
		QtWidgets.QWidget.__init__(self, parent)
		self.ui = rank_system_window.Ui_Form()
		self.ui.setupUi(self)

		# Отключаем стандартные границы окна программы
		self.setWindowFlag(QtCore.Qt.FramelessWindowHint)
		self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
		self.center()

		# Обработчики основных кнопок
		self.ui.AddNewRankButton.clicked.connect(self.add_new_rank_button)

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
	def add_new_rank_button(self):
		pass
	# ==================================================================

	# Обычные функции
	# ==================================================================
	# ==================================================================

	# Сигналы QtCore.pyqtSignal
	# ==================================================================
    # ==================================================================