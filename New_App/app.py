# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\app1.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.


from PyQt5 import QtCore, QtGui, QtWidgets,uic
import res
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication,QWidget, QVBoxLayout, QPushButton, QFileDialog , QLabel, QTextEdit
import sys
from PyQt5.QtGui import QPixmap


class Ui_MainWindow(QWidget):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(831, 610)
        MainWindow.setMaximumSize(QtCore.QSize(831, 610))
        MainWindow.setStyleSheet("background:url(:/img/background.png) ;\n"
"\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(0, 520, 791, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(130, 140, 131, 16))
        self.label.setText("")
        self.label.setObjectName("label")
        self.Add = QtWidgets.QPushButton(self.centralwidget)
        self.Add.setGeometry(QtCore.QRect(70, 100, 271, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Add.setFont(font)
        self.Add.setAutoFillBackground(False)
        self.Add.setStyleSheet("border: bold")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/img/kisspng-computer-icons-download-button-symbol-plus-5abd9e3ed95b29.3600526615223762548903-removebg-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Add.setIcon(icon)
        self.Add.setIconSize(QtCore.QSize(45, 45))
        self.Add.setAutoDefault(True)
        self.Add.setDefault(True)
        self.Add.setObjectName("Add")
        self.Run = QtWidgets.QPushButton(self.centralwidget)
        self.Run.setGeometry(QtCore.QRect(90, 190, 281, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Run.setFont(font)
        self.Run.setStyleSheet("border: bold\n"
"")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/img/run-removebg-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Run.setIcon(icon1)
        self.Run.setIconSize(QtCore.QSize(50, 50))
        self.Run.setAutoDefault(True)
        self.Run.setDefault(True)
        self.Run.setObjectName("Run")
        self.Settings = QtWidgets.QPushButton(self.centralwidget)
        self.Settings.setGeometry(QtCore.QRect(70, 290, 261, 61))
        self.Settings.setMaximumSize(QtCore.QSize(271, 16777215))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Settings.setFont(font)
        self.Settings.setStyleSheet("border: bold")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/img/download__3_-removebg-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Settings.setIcon(icon2)
        self.Settings.setIconSize(QtCore.QSize(50, 50))
        self.Settings.setObjectName("Settings")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.Add.clicked.connect(self.getImage)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Add.setText(_translate("MainWindow", "  Add Files"))
        self.Run.setText(_translate("MainWindow", "  Run Analysis"))
        self.Settings.setText(_translate("MainWindow", "  Settings"))
    
    def getImage(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file','C:', "Image files (*.jpg *.gif)")

        imagePath = fname[0]
        pixmap = QPixmap(imagePath)
        self.label.setPixmap(QPixmap(pixmap))
        self.resize(pixmap.width(), pixmap.height())    


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
