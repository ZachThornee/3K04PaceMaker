# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'UF_Login.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Login(object):
    def setupUi(self, Login):
        Login.setObjectName("Login")
        Login.resize(581, 294)
        Login.setStyleSheet("BACKGROUND-COLOR: rgb(255, 255, 255)")
        self.PB_Confirm = QtWidgets.QPushButton(Login)
        self.PB_Confirm.setGeometry(QtCore.QRect(420, 230, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.PB_Confirm.setFont(font)
        self.PB_Confirm.setStyleSheet("BACKGROUND-COLOR: rgb(170, 255, 127);\n"
"BORDER-COLOR: rgb(170, 255, 127);\n"
"BORDER-RADIUS: 10px;\n"
"BORDER-STYLE: outset;\n"
"")
        self.PB_Confirm.setObjectName("PB_Confirm")
        self.PB_UserManager = QtWidgets.QPushButton(Login)
        self.PB_UserManager.setGeometry(QtCore.QRect(20, 230, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.PB_UserManager.setFont(font)
        self.PB_UserManager.setStyleSheet("BACKGROUND-COLOR: rgb(160, 238, 252);\n"
"BORDER-COLOR: rgb(160, 238. 252);\n"
"BORDER-RADIUS: 10px;\n"
"BORDER-STYLE: outset;\n"
"")
        self.PB_UserManager.setObjectName("PB_UserManager")
        self.LAB_Login = QtWidgets.QLabel(Login)
        self.LAB_Login.setGeometry(QtCore.QRect(0, 20, 581, 51))
        self.LAB_Login.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.LAB_Login.setStyleSheet("BACKGROUND-COLOR: rgb(208, 248, 255);\n"
"")
        self.LAB_Login.setAlignment(QtCore.Qt.AlignCenter)
        self.LAB_Login.setObjectName("LAB_Login")
        self.LAB_Username = QtWidgets.QLabel(Login)
        self.LAB_Username.setGeometry(QtCore.QRect(20, 100, 91, 31))
        self.LAB_Username.setObjectName("LAB_Username")
        self.LAB_Password = QtWidgets.QLabel(Login)
        self.LAB_Password.setGeometry(QtCore.QRect(20, 170, 81, 21))
        self.LAB_Password.setObjectName("LAB_Password")
        self.PB_ForgotPassword = QtWidgets.QPushButton(Login)
        self.PB_ForgotPassword.setGeometry(QtCore.QRect(210, 240, 161, 28))
        self.PB_ForgotPassword.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.PB_ForgotPassword.setStyleSheet("BACKGROUND-COLOR: rgb(160, 238, 252);\n"
"BORDER-COLOR: rgb(160, 238. 252);\n"
"BORDER-RADIUS: 10px;\n"
"BORDER-STYLE: outset;\n"
"")
        self.PB_ForgotPassword.setObjectName("PB_ForgotPassword")
        self.textBrowser = QtWidgets.QTextBrowser(Login)
        self.textBrowser.setGeometry(QtCore.QRect(140, 100, 421, 41))
        self.textBrowser.setStyleSheet("BACKGROUND-COLOR: rgb(245, 245, 245);\n"
"BORDER-COLOR: rgb(245, 245, 245);\n"
"BORDER-RADIUS: 7px;\n"
"BORDER-WIDTH: 1px;\n"
"BORDER-STYLE: outset;")
        self.textBrowser.setObjectName("textBrowser")
        self.textBrowser_2 = QtWidgets.QTextBrowser(Login)
        self.textBrowser_2.setGeometry(QtCore.QRect(140, 160, 421, 41))
        self.textBrowser_2.setStyleSheet("BACKGROUND-COLOR: rgb(245, 245, 245);\n"
"BORDER-COLOR: rgb(245, 245, 245);\n"
"BORDER-RADIUS: 7px;\n"
"BORDER-WIDTH: 1px;\n"
"BORDER-STYLE: outset;")
        self.textBrowser_2.setObjectName("textBrowser_2")

        self.retranslateUi(Login)
        QtCore.QMetaObject.connectSlotsByName(Login)

    def retranslateUi(self, Login):
        _translate = QtCore.QCoreApplication.translate
        Login.setWindowTitle(_translate("Login", "Form"))
        self.PB_Confirm.setToolTip(_translate("Login", "<html><head/><body><p>Confirm username and password to log in</p></body></html>"))
        self.PB_Confirm.setText(_translate("Login", "Confirm"))
        self.PB_UserManager.setToolTip(_translate("Login", "<html><head/><body><p>Change your password, create new users, and delete existing users</p></body></html>"))
        self.PB_UserManager.setText(_translate("Login", "User Manager"))
        self.LAB_Login.setText(_translate("Login", "<html><head/><body><p><span style=\" font-size:12pt;\">Login</span></p></body></html>"))
        self.LAB_Username.setText(_translate("Login", "<html><head/><body><p><span style=\" font-size:11pt;\">Username:</span></p></body></html>"))
        self.LAB_Password.setText(_translate("Login", "<html><head/><body><p><span style=\" font-size:11pt;\">Password:</span></p></body></html>"))
        self.PB_ForgotPassword.setText(_translate("Login", "Forgot Password"))
