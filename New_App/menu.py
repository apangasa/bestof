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
        self.add_files_button = QtWidgets.QPushButton(MainMenu)
        self.add_files_button.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.add_files_button.sizePolicy().hasHeightForWidth())
        self.add_files_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.add_files_button.setFont(font)
        self.add_files_button.setAutoFillBackground(False)
        self.add_files_button.setStyleSheet("border: bold")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            ":/img/kisspng-computer-icons-download-button-symbol-plus-5abd9e3ed95b29.3600526615223762548903-removebg-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_files_button.setIcon(icon)
        self.add_files_button.setIconSize(QtCore.QSize(50, 50))
        self.add_files_button.setAutoDefault(True)
        self.add_files_button.setDefault(True)
        self.add_files_button.setObjectName("Add")
        self.verticalLayout.addWidget(
            self.add_files_button, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.run_analysis_button = QtWidgets.QPushButton(MainMenu)
        self.run_analysis_button.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.run_analysis_button.sizePolicy().hasHeightForWidth())
        self.run_analysis_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.run_analysis_button.setFont(font)
        self.run_analysis_button.setStyleSheet("border: bold\n"
                                               "")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(
            ":/img/run-removebg-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.run_analysis_button.setIcon(icon1)
        self.run_analysis_button.setIconSize(QtCore.QSize(50, 50))
        self.run_analysis_button.setAutoDefault(True)
        self.run_analysis_button.setDefault(True)
        self.run_analysis_button.setObjectName("Run")
        self.verticalLayout.addWidget(
            self.run_analysis_button, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.settings_button = QtWidgets.QPushButton(MainMenu)
        self.settings_button.setCursor(
            QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.settings_button.sizePolicy().hasHeightForWidth())
        self.settings_button.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.settings_button.setFont(font)
        self.settings_button.setStyleSheet("border: bold")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(
            ":/img/download__3_-removebg-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.settings_button.setIcon(icon2)
        self.settings_button.setIconSize(QtCore.QSize(50, 50))
        self.settings_button.setObjectName("Settings")
        self.verticalLayout.addWidget(
            self.settings_button, 0, QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        spacerItem1 = QtWidgets.QSpacerItem(
            20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.gridLayout_2.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(MainMenu)
        QtCore.QMetaObject.connectSlotsByName(MainMenu)

    def retranslateUi(self, MainMenu):
        _translate = QtCore.QCoreApplication.translate
        MainMenu.setWindowTitle(_translate("MainMenu", "Form"))
        self.add_files_button.setText(_translate(
            "MainMenu", "Add Files"))
        self.run_analysis_button.setText(_translate(
            "MainMenu", "Run Analysis"))
        self.settings_button.setText(
            _translate("MainMenu", "Settings"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainMenu = QtWidgets.QWidget()
    ui = Ui_MainMenu()
    ui.setupUi(MainMenu)
    MainMenu.show()
    sys.exit(app.exec_())
