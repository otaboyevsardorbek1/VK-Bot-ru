# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'registration_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(431, 341)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Window = QtWidgets.QFrame(self.centralwidget)
        self.Window.setGeometry(QtCore.QRect(10, 10, 411, 321))
        self.Window.setStyleSheet("QFrame{\n"
"    border-radius: 7px;\n"
"    background-color: #1B1D23;\n"
"}")
        self.Window.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Window.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Window.setObjectName("Window")
        self.WindowFrame = QtWidgets.QFrame(self.Window)
        self.WindowFrame.setGeometry(QtCore.QRect(0, 0, 411, 31))
        self.WindowFrame.setStyleSheet("QFrame{\n"
"    border-bottom-left-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"    background-color: #2C313C;\n"
"}")
        self.WindowFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.WindowFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.WindowFrame.setObjectName("WindowFrame")
        self.CloseWindowButton = QtWidgets.QPushButton(self.WindowFrame)
        self.CloseWindowButton.setGeometry(QtCore.QRect(371, 0, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.CloseWindowButton.setFont(font)
        self.CloseWindowButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.CloseWindowButton.setStyleSheet("QPushButton{\n"
"    color: white;\n"
"    border: none;\n"
"    border-top-right-radius: 7px;\n"
"    background-color: #2C313C;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: #45494D;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    color: #EA2F4E;\n"
"}")
        self.CloseWindowButton.setObjectName("CloseWindowButton")
        self.MinimizeWindowButton = QtWidgets.QPushButton(self.WindowFrame)
        self.MinimizeWindowButton.setGeometry(QtCore.QRect(330, 0, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.MinimizeWindowButton.setFont(font)
        self.MinimizeWindowButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.MinimizeWindowButton.setStyleSheet("QPushButton{\n"
"    color: white;\n"
"    border: none;\n"
"    background-color: #2C313C;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: #45494D;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    color: #EA2F4E;\n"
"}")
        self.MinimizeWindowButton.setDefault(False)
        self.MinimizeWindowButton.setObjectName("MinimizeWindowButton")
        self.Label = QtWidgets.QLabel(self.Window)
        self.Label.setGeometry(QtCore.QRect(20, 40, 371, 61))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label.sizePolicy().hasHeightForWidth())
        self.Label.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(36)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.Label.setFont(font)
        self.Label.setStyleSheet("QLabel{\n"
"    color: white;\n"
"}")
        self.Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Label.setObjectName("Label")
        self.LoginLineEdit = QtWidgets.QLineEdit(self.Window)
        self.LoginLineEdit.setGeometry(QtCore.QRect(20, 110, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.LoginLineEdit.setFont(font)
        self.LoginLineEdit.setStyleSheet("QLineEdit{\n"
"    border-radius: 12px;\n"
"}")
        self.LoginLineEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.LoginLineEdit.setInputMask("")
        self.LoginLineEdit.setText("")
        self.LoginLineEdit.setFrame(False)
        self.LoginLineEdit.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.LoginLineEdit.setObjectName("LoginLineEdit")
        self.PasswordLineEdit_1 = QtWidgets.QLineEdit(self.Window)
        self.PasswordLineEdit_1.setGeometry(QtCore.QRect(20, 160, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.PasswordLineEdit_1.setFont(font)
        self.PasswordLineEdit_1.setStyleSheet("QLineEdit{\n"
"    border-bottom-right-radius: 0px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-left-radius: 12px;\n"
"    border-top-left-radius: 12px;\n"
"}")
        self.PasswordLineEdit_1.setInputMask("")
        self.PasswordLineEdit_1.setText("")
        self.PasswordLineEdit_1.setFrame(False)
        self.PasswordLineEdit_1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PasswordLineEdit_1.setDragEnabled(False)
        self.PasswordLineEdit_1.setReadOnly(False)
        self.PasswordLineEdit_1.setObjectName("PasswordLineEdit_1")
        self.CreateAccountButton = QtWidgets.QPushButton(self.Window)
        self.CreateAccountButton.setGeometry(QtCore.QRect(220, 260, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.CreateAccountButton.setFont(font)
        self.CreateAccountButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.CreateAccountButton.setStyleSheet("QPushButton{\n"
"    color: white;\n"
"    border-radius: 8px;\n"
"    background-color: #595F76;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: #50566E;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: #434965;\n"
"}")
        self.CreateAccountButton.setObjectName("CreateAccountButton")
        self.AskButton = QtWidgets.QPushButton(self.Window)
        self.AskButton.setGeometry(QtCore.QRect(45, 270, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.AskButton.setFont(font)
        self.AskButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AskButton.setStyleSheet("QPushButton{\n"
"    color: white;\n"
"    border: none;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    color: #ebebeb;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    color: white;\n"
"}")
        self.AskButton.setObjectName("AskButton")
        self.ShowPasswordButton_1 = QtWidgets.QPushButton(self.Window)
        self.ShowPasswordButton_1.setGeometry(QtCore.QRect(350, 160, 41, 41))
        self.ShowPasswordButton_1.setStyleSheet("QPushButton{\n"
"    border: none;\n"
"    border-bottom-right-radius: 12px;\n"
"    border-top-right-radius: 12px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-top-left-radius: 0px;\n"
"    background-color: white;\n"
"}")
        self.ShowPasswordButton_1.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Icons/eyeOn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ShowPasswordButton_1.setIcon(icon)
        self.ShowPasswordButton_1.setIconSize(QtCore.QSize(32, 32))
        self.ShowPasswordButton_1.setObjectName("ShowPasswordButton_1")
        self.PasswordLineEdit_2 = QtWidgets.QLineEdit(self.Window)
        self.PasswordLineEdit_2.setGeometry(QtCore.QRect(20, 210, 331, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.PasswordLineEdit_2.setFont(font)
        self.PasswordLineEdit_2.setStyleSheet("QLineEdit{\n"
"    border-bottom-right-radius: 0px;\n"
"    border-top-right-radius: 0px;\n"
"    border-bottom-left-radius: 12px;\n"
"    border-top-left-radius: 12px;\n"
"}")
        self.PasswordLineEdit_2.setInputMask("")
        self.PasswordLineEdit_2.setText("")
        self.PasswordLineEdit_2.setFrame(False)
        self.PasswordLineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.PasswordLineEdit_2.setDragEnabled(False)
        self.PasswordLineEdit_2.setReadOnly(False)
        self.PasswordLineEdit_2.setObjectName("PasswordLineEdit_2")
        self.ShowPasswordButton_2 = QtWidgets.QPushButton(self.Window)
        self.ShowPasswordButton_2.setGeometry(QtCore.QRect(350, 210, 41, 41))
        self.ShowPasswordButton_2.setStyleSheet("QPushButton{\n"
"    border: none;\n"
"    border-bottom-right-radius: 12px;\n"
"    border-top-right-radius: 12px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-top-left-radius: 0px;\n"
"    background-color: white;\n"
"}")
        self.ShowPasswordButton_2.setText("")
        self.ShowPasswordButton_2.setIcon(icon)
        self.ShowPasswordButton_2.setIconSize(QtCore.QSize(32, 32))
        self.ShowPasswordButton_2.setObjectName("ShowPasswordButton_2")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.CloseWindowButton.setText(_translate("MainWindow", "X"))
        self.MinimizeWindowButton.setText(_translate("MainWindow", "_"))
        self.Label.setText(_translate("MainWindow", "РЕГИСТРАЦИЯ"))
        self.LoginLineEdit.setPlaceholderText(_translate("MainWindow", "Придумайте Login"))
        self.PasswordLineEdit_1.setPlaceholderText(_translate("MainWindow", "Придумайте Password"))
        self.CreateAccountButton.setText(_translate("MainWindow", "Создать аккаунт"))
        self.AskButton.setText(_translate("MainWindow", "Уже есть аккаунт?"))
        self.PasswordLineEdit_2.setPlaceholderText(_translate("MainWindow", "Повторите Password"))
