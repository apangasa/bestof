# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainMenu(object):
    def setupUi(self, MainMenu):
        MainMenu.setObjectName("MainMenu")
        MainMenu.resize(816, 605)
        self.gridLayout_2 = QtWidgets.QGridLayout(MainMenu)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(100, -1, -1, -1)
        self.verticalLayout.setSpacing(40)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.Add = QtWidgets.QPushButton(MainMenu)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Add.sizePolicy().hasHeightForWidth())
        self.Add.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Add.setFont(font)
        self.Add.setAutoFillBackground(False)
        self.Add.setStyleSheet("border: bold")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            ":/img/kisspng-computer-icons-download-button-symbol-plus-5abd9e3ed95b29.3600526615223762548903-removebg-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Add.setIcon(icon)
        self.Add.setIconSize(QtCore.QSize(50, 50))
        self.Add.setAutoDefault(True)
        self.Add.setDefault(True)
        self.Add.setObjectName("Add")
        self.verticalLayout.addWidget(
            self.Add, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.Run = QtWidgets.QPushButton(MainMenu)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Run.sizePolicy().hasHeightForWidth())
        self.Run.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Run.setFont(font)
        self.Run.setStyleSheet("border: bold\n"
                               "")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(
            ":/img/run-removebg-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Run.setIcon(icon1)
        self.Run.setIconSize(QtCore.QSize(50, 50))
        self.Run.setAutoDefault(True)
        self.Run.setDefault(True)
        self.Run.setObjectName("Run")
        self.verticalLayout.addWidget(
            self.Run, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.Settings = QtWidgets.QPushButton(MainMenu)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.Settings.sizePolicy().hasHeightForWidth())
        self.Settings.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.Settings.setFont(font)
        self.Settings.setStyleSheet("border: bold")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(
            ":/img/download__3_-removebg-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Settings.setIcon(icon2)
        self.Settings.setIconSize(QtCore.QSize(50, 50))
        self.Settings.setObjectName("Settings")
        self.verticalLayout.addWidget(
            self.Settings, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(MainMenu)
        QtCore.QMetaObject.connectSlotsByName(MainMenu)

    def retranslateUi(self, MainMenu):
        _translate = QtCore.QCoreApplication.translate
        MainMenu.setWindowTitle(_translate("MainMenu", "Form"))
        self.Add.setText(_translate("MainMenu", "  Add Files"))
        self.Run.setText(_translate("MainMenu", "  Run Analysis"))
        self.Settings.setText(_translate("MainMenu", "  Settings"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainMenu = QtWidgets.QWidget()
    ui = Ui_MainMenu()
    ui.setupUi(MainMenu)
    MainMenu.show()
    sys.exit(app.exec_())
