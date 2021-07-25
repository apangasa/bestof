# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app1.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.
from PyQt5.QtGui import *
import sys
import numpy as np
import res
from PyQt5.QtWidgets import QWidget, QFileDialog
from PyQt5 import QtCore, QtGui, QtWidgets
from threading import Thread
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

import bestOf.backend.similarity as similarity
import bestOf.backend.blinkDetector as blinkDetector
import bestOf.backend.cropDetector as cropDetector
import bestOf.backend.evaluateSharpness as evaluateSharpness
import bestOf.backend.identifyPeople as identifyPeople
import bestOf.backend.evaluateCentering as evaluateCentering


def loadImages(filenames):
    for filename in filenames:
        image = identifyPeople.read_img(filename)
        yield (image * 255).astype(np.uint8)[:, :, :3] if 'png' in filename else image


IMAGELIST = []
GROUPS = []


class Ui_MainWindow(QWidget):
    progressChangedSignal = pyqtSignal(int)
    statusChangedSignal = pyqtSignal(str, str)

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(831, 610)
        MainWindow.setMaximumSize(QtCore.QSize(831, 610))
        MainWindow.setStyleSheet("background-color: white;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Add = QtWidgets.QPushButton(self.centralwidget)
        self.Add.setGeometry(QtCore.QRect(20, 150, 271, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.Add.setFont(font)
        self.Add.setAutoFillBackground(False)
        self.Add.setStyleSheet("border: bold")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(
            ":/img/kisspng-computer-icons-download-button-symbol-plus-5abd9e3ed95b29.3600526615223762548903-removebg-preview.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.Add.setIcon(icon)
        self.Add.setIconSize(QtCore.QSize(45, 45))
        self.Add.setAutoDefault(True)
        self.Add.setDefault(True)
        self.Add.setObjectName("Add")
        self.Run = QtWidgets.QPushButton(self.centralwidget)
        self.Run.setGeometry(QtCore.QRect(40, 240, 271, 61))
        font = QtGui.QFont()
        font.setPointSize(16)
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
        self.Settings = QtWidgets.QPushButton(self.centralwidget)
        self.Settings.setGeometry(QtCore.QRect(20, 340, 261, 61))
        self.Settings.setMaximumSize(QtCore.QSize(271, 16777215))
        font = QtGui.QFont()
        font.setPointSize(16)
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
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setEnabled(True)
        self.frame.setGeometry(QtCore.QRect(0, 570, 831, 2))
        self.frame.setStyleSheet("background: black;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
        self.progressBar.setGeometry(QtCore.QRect(180, 580, 641, 23))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.progressBar.setFont(font)
        self.progressBar.setStyleSheet("QProgressBar {\n"
                                       "    border: 2px solid black;\n"
                                       "   text-align: center;\n"
                                       "}\n"
                                       "\n"
                                       "QProgressBar::chunk {\n"
                                       "    background-color: #1976D3;\n"
                                       "    width: 20px;\n"
                                       "}")
        self.progressBar.setProperty("value", 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.Status = QtWidgets.QLabel(self.centralwidget)
        self.Status.setGeometry(QtCore.QRect(10, 576, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.Status.setFont(font)
        self.Status.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.Status.setObjectName("Status")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.progressChangedSignal.connect(self.changeProgress)
        self.statusChangedSignal.connect(self.changeStatus)

        self.Status.setText("Waiting")
        self.Add.clicked.connect(self.getFiles)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Add.setText(_translate("MainWindow", "  Add Files"))
        self.Run.setText(_translate("MainWindow", "  Run Analysis"))
        self.Settings.setText(_translate("MainWindow", "  Settings"))
        self.Status.setText(_translate("MainWindow", "Status"))

    def changeProgress(self, progress):
        self.progressBar.setProperty("value", progress)

    def changeStatus(self, status, color="black"):
        self.Status.setText(status)
        self.Status.setStyleSheet("color: %s;" % color)

    def getFiles(self):
        file = QFileDialog.getOpenFileNames(
            self, 'Add Files', QtCore.QDir.rootPath(), "Image Files (*.png *.jpg)")
        if len(file[0]) == 0:
            self.changeStatus("No files selected", "red")
            self.changeProgress(0)
            return
        self.changeStatus("Loading...")
        thread = Thread(target=self.loadFiles, args=(file,))
        thread.start()

    def loadFiles(self, file):
        global IMAGELIST
        global GROUPS

        maxProgress = len(file[0]) * 2
        progress = 0

        image_generator = loadImages(list(file[0]))
        vectors = []
        for image in image_generator:
            v = similarity.generate_feature_vector(image)
            vectors.append(v)
            progress += 1
            self.progressChangedSignal.emit(progress / maxProgress * 100)

        threshold = 0.8  # this should be grabbed from whatever the user set it to in the settings
        groups = similarity.group(vectors, threshold=threshold)
        # print(groups)
        GROUPS = groups

        image_generator = loadImages(list(file[0]))

        default_scores = []
        subject_sharpness_scores = []
        centering_scores = []

        for image in image_generator:
            # print('Scanning Image...')
            subjects, bounds_list = identifyPeople.crop_subjects(image)
            # print("len of subjects", len(subjects))
            blinks = 0
            crops = 0

            subject_sharpness_scores.append([])

            centering_scores.append(
                evaluateCentering.evaluate_centering(bounds_list, image))

            for sub in subjects:
                # identifyPeople.show_img(sub)
                # print('Scanning Subject...')
                if blinkDetector.test(sub):
                    blinks += 1
                if cropDetector.test(sub):
                    crops += 1

                subject_sharpness_scores[-1].append(
                    evaluateSharpness.evaluate_sharpness(sub))

            if len(subjects) == 0:
                default_scores.append(0)
                progress += 1
                self.progressChangedSignal.emit(progress / maxProgress * 100)
                continue

            blink_score = (len(subjects) - blinks) / len(subjects)
            crop_score = (len(subjects) - crops) / len(subjects)

            default_score = blink_score + crop_score
            default_scores.append(default_score)

            progress += 1
            self.progressChangedSignal.emit(progress / maxProgress * 100)

        if len(IMAGELIST):
            max_index = max([ind for ind in IMAGELIST[0]])
        else:
            max_index = -1

        final = zip(
            range(max_index + 1, max_index + 1 + len(file[0])), file[0], default_scores, subject_sharpness_scores, centering_scores)

        if len(IMAGELIST):
            final = final + IMAGELIST
        final = sorted(final, key=lambda x: x[2], reverse=True)
        print(final)
        IMAGELIST = final
        self.statusChangedSignal.emit("Files loaded", "green")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
