# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'user_bot_menu_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(811, 651)
        self.Window = QtWidgets.QFrame(Form)
        self.Window.setGeometry(QtCore.QRect(10, 10, 791, 631))
        self.Window.setStyleSheet("QFrame{\n"
"    border-radius: 7px;\n"
"    background-color: #1B1D23;\n"
"}\n"
"\n"
"QLabel{\n"
"    color: white;\n"
"}\n"
"\n"
"QScrollBar:vertical{\n"
"    border: none;\n"
"    background: #595F76;\n"
"    width: 15px;\n"
"    margin: 15px 0 15px 0;\n"
"    border-radius: 0px;\n"
" }\n"
"\n"
"QScrollBar::handle:vertical{    \n"
"    background-color: #494E61;\n"
"    min-height: 30px;\n"
"}\n"
"QScrollBar::handle:vertical:hover{    \n"
"    background-color: #D5006A;\n"
"}\n"
"QScrollBar::handle:vertical:pressed{    \n"
"    background-color: #B9005C;\n"
"}\n"
"\n"
"QScrollBar::sub-line:vertical{\n"
"    border: none;\n"
"    background-color: #3A3F50;\n"
"    height: 15px;\n"
"    border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"    subcontrol-position: top;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:vertical:hover{    \n"
"    background-color: #D5006A;\n"
"}\n"
"QScrollBar::sub-line:vertical:pressed{    \n"
"    background-color: #B9005C;\n"
"}\n"
"\n"
"QScrollBar::add-line:vertical{\n"
"    border: none;\n"
"    background-color: #3A3F50;\n"
"    height: 15px;\n"
"    border-bottom-left-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"    subcontrol-position: bottom;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::add-line:vertical:hover{    \n"
"    background-color: #D5006A;\n"
"}\n"
"QScrollBar::add-line:vertical:pressed{    \n"
"    background-color: #B9005C;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical{\n"
"    background: none;\n"
"}\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical{\n"
"    background: none;\n"
"}\n"
"\n"
"QScrollBar:horizontal{\n"
"    border: none;\n"
"    background: #595F76;\n"
"    height: 15px;\n"
"    margin: 0px 15 0px 15;\n"
"    border-radius: opx;\n"
" }\n"
"\n"
"QScrollBar::handle:horizontal{    \n"
"    background-color: #494E61;\n"
"    min-width: 30px;\n"
"}\n"
"QScrollBar::handle:horizontal:hover{    \n"
"    background-color: #D5006A;\n"
"}\n"
"QScrollBar::handle:horizontal:pressed{    \n"
"    background-color: #B9005C;\n"
"}\n"
"\n"
"QScrollBar::sub-line:horizontal{\n"
"    border: none;\n"
"    background-color: #3A3F50;\n"
"    width: 15px;\n"
"    border-top-left-radius: 7px;\n"
"    border-bottom-left-radius: 7px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal:hover{    \n"
"    background-color:#D5006A;\n"
"}\n"
"QScrollBar::sub-line:horizontal:pressed{    \n"
"    background-color: #B9005C;\n"
"}\n"
"\n"
"QScrollBar::add-line:horizontal{\n"
"    border: none;\n"
"    background-color: #3A3F50;\n"
"    width: 15px;\n"
"    border-top-right-radius: 7px;\n"
"    border-bottom-right-radius: 7px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::add-line:horizontal:hover{    \n"
"    background-color: #D5006A;\n"
"}\n"
"QScrollBar::add-line:horizontal:pressed{    \n"
"    background-color: #B9005C;\n"
"}\n"
"\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal{\n"
"    background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal{\n"
"    background: none;\n"
"}")
        self.Window.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Window.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Window.setObjectName("Window")
        self.WindowFrame = QtWidgets.QFrame(self.Window)
        self.WindowFrame.setGeometry(QtCore.QRect(0, 0, 791, 31))
        self.WindowFrame.setStyleSheet("QFrame{\n"
"    border-bottom-left-radius: 0px;\n"
"    border-bottom-right-radius: 0px;\n"
"    background-color: #2C313C;\n"
"}")
        self.WindowFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.WindowFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.WindowFrame.setObjectName("WindowFrame")
        self.CloseWindowButton = QtWidgets.QPushButton(self.WindowFrame)
        self.CloseWindowButton.setGeometry(QtCore.QRect(750, 0, 41, 31))
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
        self.MinimizeWindowButton.setGeometry(QtCore.QRect(709, 0, 41, 31))
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
        self.SaveBotSettingsButton = QtWidgets.QPushButton(self.WindowFrame)
        self.SaveBotSettingsButton.setGeometry(QtCore.QRect(678, 0, 31, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.SaveBotSettingsButton.setFont(font)
        self.SaveBotSettingsButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SaveBotSettingsButton.setStyleSheet("QPushButton{\n"
"    border: none;\n"
"    background-color: #2C313C;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: #45494D;\n"
"}")
        self.SaveBotSettingsButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../Icons/SaveOff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.SaveBotSettingsButton.setIcon(icon)
        self.SaveBotSettingsButton.setIconSize(QtCore.QSize(25, 25))
        self.SaveBotSettingsButton.setObjectName("SaveBotSettingsButton")
        self.ProgramInfoWindowButton = QtWidgets.QPushButton(self.WindowFrame)
        self.ProgramInfoWindowButton.setGeometry(QtCore.QRect(0, 0, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.ProgramInfoWindowButton.setFont(font)
        self.ProgramInfoWindowButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ProgramInfoWindowButton.setStyleSheet("QPushButton{\n"
"    color: white;\n"
"    border: none;\n"
"    border-top-left-radius: 7px;\n"
"    background-color: #2C313C;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"    background-color: #45494D;\n"
"}\n"
"\n"
"QPushButton:pressed{\n"
"    background-color: #1B1D23;\n"
"}")
        self.ProgramInfoWindowButton.setObjectName("ProgramInfoWindowButton")
        self.VKTokenLineEdit = QtWidgets.QLineEdit(self.Window)
        self.VKTokenLineEdit.setGeometry(QtCore.QRect(20, 130, 331, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.VKTokenLineEdit.setFont(font)
        self.VKTokenLineEdit.setStyleSheet("QLineEdit{\n"
"    border-bottom-left-radius: 12px;\n"
"    border-top-left-radius: 12px;\n"
"    background-color: white;\n"
"}")
        self.VKTokenLineEdit.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.VKTokenLineEdit.setInputMask("")
        self.VKTokenLineEdit.setText("")
        self.VKTokenLineEdit.setFrame(False)
        self.VKTokenLineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.VKTokenLineEdit.setCursorMoveStyle(QtCore.Qt.LogicalMoveStyle)
        self.VKTokenLineEdit.setObjectName("VKTokenLineEdit")
        self.IDBotLineEdit = QtWidgets.QLineEdit(self.Window)
        self.IDBotLineEdit.setGeometry(QtCore.QRect(20, 170, 371, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.IDBotLineEdit.setFont(font)
        self.IDBotLineEdit.setStyleSheet("QLineEdit{\n"
"    border-radius: 12px;\n"
"    background-color: white;\n"
"}")
        self.IDBotLineEdit.setInputMask("")
        self.IDBotLineEdit.setText("")
        self.IDBotLineEdit.setFrame(False)
        self.IDBotLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.IDBotLineEdit.setDragEnabled(False)
        self.IDBotLineEdit.setReadOnly(False)
        self.IDBotLineEdit.setObjectName("IDBotLineEdit")
        self.label_3 = QtWidgets.QLabel(self.Window)
        self.label_3.setGeometry(QtCore.QRect(400, 494, 281, 20))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("")
        self.label_3.setObjectName("label_3")
        self.AutomatiSaveLogButton = QtWidgets.QPushButton(self.Window)
        self.AutomatiSaveLogButton.setGeometry(QtCore.QRect(678, 497, 20, 21))
        self.AutomatiSaveLogButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AutomatiSaveLogButton.setStyleSheet("QPushButton{\n"
"    border: none;\n"
"}")
        self.AutomatiSaveLogButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../Icons/iconOff.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.AutomatiSaveLogButton.setIcon(icon1)
        self.AutomatiSaveLogButton.setIconSize(QtCore.QSize(16, 16))
        self.AutomatiSaveLogButton.setObjectName("AutomatiSaveLogButton")
        self.UserBotNameLineEdit = QtWidgets.QLineEdit(self.Window)
        self.UserBotNameLineEdit.setGeometry(QtCore.QRect(20, 90, 371, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(False)
        font.setWeight(50)
        self.UserBotNameLineEdit.setFont(font)
        self.UserBotNameLineEdit.setStyleSheet("QLineEdit{\n"
"    border-radius: 12px;\n"
"    background-color: white;\n"
"}")
        self.UserBotNameLineEdit.setInputMask("")
        self.UserBotNameLineEdit.setText("")
        self.UserBotNameLineEdit.setFrame(False)
        self.UserBotNameLineEdit.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.UserBotNameLineEdit.setDragEnabled(False)
        self.UserBotNameLineEdit.setReadOnly(False)
        self.UserBotNameLineEdit.setObjectName("UserBotNameLineEdit")
        self.Label_1 = QtWidgets.QLabel(self.Window)
        self.Label_1.setGeometry(QtCore.QRect(20, 34, 371, 51))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_1.sizePolicy().hasHeightForWidth())
        self.Label_1.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.Label_1.setFont(font)
        self.Label_1.setStyleSheet("QLabel{\n"
"    color: white;\n"
"}")
        self.Label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.Label_1.setObjectName("Label_1")
        self.UserBotButton = QtWidgets.QPushButton(self.Window)
        self.UserBotButton.setGeometry(QtCore.QRect(20, 210, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.UserBotButton.setFont(font)
        self.UserBotButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.UserBotButton.setStyleSheet("QPushButton{\n"
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
        self.UserBotButton.setText("")
        self.UserBotButton.setObjectName("UserBotButton")
        self.ClearLogButton = QtWidgets.QPushButton(self.Window)
        self.ClearLogButton.setGeometry(QtCore.QRect(400, 570, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.ClearLogButton.setFont(font)
        self.ClearLogButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.ClearLogButton.setStyleSheet("QPushButton{\n"
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
        self.ClearLogButton.setObjectName("ClearLogButton")
        self.SaveLogButton = QtWidgets.QPushButton(self.Window)
        self.SaveLogButton.setGeometry(QtCore.QRect(400, 520, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.SaveLogButton.setFont(font)
        self.SaveLogButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.SaveLogButton.setStyleSheet("QPushButton{\n"
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
        self.SaveLogButton.setObjectName("SaveLogButton")
        self.Label_2 = QtWidgets.QLabel(self.Window)
        self.Label_2.setGeometry(QtCore.QRect(400, 34, 371, 51))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_2.sizePolicy().hasHeightForWidth())
        self.Label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.Label_2.setFont(font)
        self.Label_2.setStyleSheet("QLabel{\n"
"    color: white;\n"
"}")
        self.Label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.Label_2.setObjectName("Label_2")
        self.LogListWidget = QtWidgets.QListWidget(self.Window)
        self.LogListWidget.setGeometry(QtCore.QRect(400, 90, 371, 401))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.LogListWidget.setFont(font)
        self.LogListWidget.setTabletTracking(False)
        self.LogListWidget.setAutoFillBackground(False)
        self.LogListWidget.setStyleSheet("QListWidget{\n"
"    color: white;\n"
"    border-radius: 7px;\n"
"    background-color: #2C313C;\n"
"}\n"
"")
        self.LogListWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.LogListWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.LogListWidget.setLineWidth(1)
        self.LogListWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.LogListWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.LogListWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.LogListWidget.setAutoScroll(True)
        self.LogListWidget.setTabKeyNavigation(False)
        self.LogListWidget.setProperty("showDropIndicator", True)
        self.LogListWidget.setDragDropOverwriteMode(False)
        self.LogListWidget.setAlternatingRowColors(False)
        self.LogListWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.LogListWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.LogListWidget.setMovement(QtWidgets.QListView.Static)
        self.LogListWidget.setFlow(QtWidgets.QListView.TopToBottom)
        self.LogListWidget.setProperty("isWrapping", False)
        self.LogListWidget.setResizeMode(QtWidgets.QListView.Fixed)
        self.LogListWidget.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.LogListWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.LogListWidget.setUniformItemSizes(False)
        self.LogListWidget.setWordWrap(False)
        self.LogListWidget.setSelectionRectVisible(False)
        self.LogListWidget.setObjectName("LogListWidget")
        self.DeleteUserCommandButton = QtWidgets.QPushButton(self.Window)
        self.DeleteUserCommandButton.setGeometry(QtCore.QRect(20, 570, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.DeleteUserCommandButton.setFont(font)
        self.DeleteUserCommandButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.DeleteUserCommandButton.setStyleSheet("QPushButton{\n"
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
        self.DeleteUserCommandButton.setObjectName("DeleteUserCommandButton")
        self.UserCommandsListWidget = QtWidgets.QListWidget(self.Window)
        self.UserCommandsListWidget.setGeometry(QtCore.QRect(20, 310, 371, 151))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.UserCommandsListWidget.setFont(font)
        self.UserCommandsListWidget.setTabletTracking(False)
        self.UserCommandsListWidget.setAutoFillBackground(False)
        self.UserCommandsListWidget.setStyleSheet("color: white;\n"
"border-radius: 7px;\n"
"background-color: #2C313C;\n"
"")
        self.UserCommandsListWidget.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.UserCommandsListWidget.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.UserCommandsListWidget.setLineWidth(1)
        self.UserCommandsListWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.UserCommandsListWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.UserCommandsListWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.UserCommandsListWidget.setAutoScroll(True)
        self.UserCommandsListWidget.setTabKeyNavigation(False)
        self.UserCommandsListWidget.setProperty("showDropIndicator", True)
        self.UserCommandsListWidget.setDragDropOverwriteMode(False)
        self.UserCommandsListWidget.setAlternatingRowColors(False)
        self.UserCommandsListWidget.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.UserCommandsListWidget.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerItem)
        self.UserCommandsListWidget.setMovement(QtWidgets.QListView.Static)
        self.UserCommandsListWidget.setFlow(QtWidgets.QListView.TopToBottom)
        self.UserCommandsListWidget.setProperty("isWrapping", False)
        self.UserCommandsListWidget.setResizeMode(QtWidgets.QListView.Fixed)
        self.UserCommandsListWidget.setLayoutMode(QtWidgets.QListView.SinglePass)
        self.UserCommandsListWidget.setViewMode(QtWidgets.QListView.ListMode)
        self.UserCommandsListWidget.setUniformItemSizes(False)
        self.UserCommandsListWidget.setWordWrap(False)
        self.UserCommandsListWidget.setSelectionRectVisible(False)
        self.UserCommandsListWidget.setObjectName("UserCommandsListWidget")
        self.Label_3 = QtWidgets.QLabel(self.Window)
        self.Label_3.setGeometry(QtCore.QRect(20, 254, 371, 51))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Label_3.sizePolicy().hasHeightForWidth())
        self.Label_3.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(30)
        font.setBold(True)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(75)
        font.setStrikeOut(False)
        font.setKerning(True)
        self.Label_3.setFont(font)
        self.Label_3.setStyleSheet("QLabel{\n"
"    color: white;\n"
"}")
        self.Label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.Label_3.setObjectName("Label_3")
        self.EditUserCommandButton = QtWidgets.QPushButton(self.Window)
        self.EditUserCommandButton.setGeometry(QtCore.QRect(20, 520, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.EditUserCommandButton.setFont(font)
        self.EditUserCommandButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.EditUserCommandButton.setStyleSheet("QPushButton{\n"
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
        self.EditUserCommandButton.setObjectName("EditUserCommandButton")
        self.AddUserCommandButton = QtWidgets.QPushButton(self.Window)
        self.AddUserCommandButton.setGeometry(QtCore.QRect(20, 470, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.AddUserCommandButton.setFont(font)
        self.AddUserCommandButton.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.AddUserCommandButton.setStyleSheet("QPushButton{\n"
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
        self.AddUserCommandButton.setObjectName("AddUserCommandButton")
        self.ShowVKTokenButton = QtWidgets.QPushButton(self.Window)
        self.ShowVKTokenButton.setGeometry(QtCore.QRect(350, 130, 41, 31))
        self.ShowVKTokenButton.setStyleSheet("QPushButton{\n"
"    border: none;\n"
"    border-bottom-right-radius: 12px;\n"
"    border-top-right-radius: 12px;\n"
"    border-bottom-left-radius: 0px;\n"
"    border-top-left-radius: 0px;\n"
"    background-color: white;\n"
"}")
        self.ShowVKTokenButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("../Icons/eyeOn.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.ShowVKTokenButton.setIcon(icon2)
        self.ShowVKTokenButton.setIconSize(QtCore.QSize(32, 32))
        self.ShowVKTokenButton.setObjectName("ShowVKTokenButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.CloseWindowButton.setText(_translate("Form", "X"))
        self.MinimizeWindowButton.setText(_translate("Form", "_"))
        self.ProgramInfoWindowButton.setText(_translate("Form", "О программе"))
        self.VKTokenLineEdit.setPlaceholderText(_translate("Form", "Введите VK Token бота"))
        self.IDBotLineEdit.setPlaceholderText(_translate("Form", "Введите ID бота"))
        self.label_3.setText(_translate("Form", "Автомат. сохранение логов:"))
        self.UserBotNameLineEdit.setPlaceholderText(_translate("Form", "Придумайте имя боту"))
        self.Label_1.setText(_translate("Form", "Инфо. о боте"))
        self.ClearLogButton.setText(_translate("Form", "Очистить логи"))
        self.SaveLogButton.setText(_translate("Form", "Сохранить логи"))
        self.Label_2.setText(_translate("Form", "Логи"))
        self.LogListWidget.setSortingEnabled(False)
        self.DeleteUserCommandButton.setText(_translate("Form", "Удалить команду"))
        self.UserCommandsListWidget.setSortingEnabled(False)
        self.Label_3.setText(_translate("Form", "Команды бота"))
        self.EditUserCommandButton.setText(_translate("Form", "Редактировать команду"))
        self.AddUserCommandButton.setText(_translate("Form", "Добавить команду"))
