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
import menu

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
        MainWindow.resize(773, 574)
        MainWindow.setStyleSheet("background-color: white;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(
            QtWidgets.QLayout.SetNoConstraint)
        self.verticalLayout.setContentsMargins(-1, -1, -1, 5)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName("stackedWidget")
        self.verticalLayout.addWidget(self.stackedWidget)
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setEnabled(True)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 2))
        self.frame.setMinimumSize(QtCore.QSize(0, 2))
        self.frame.setStyleSheet("background: black;")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout.setSpacing(4)
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, -1, 10, -1)
        self.horizontalLayout.setSpacing(16)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Status = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.Status.setFont(font)
        self.Status.setAlignment(
            QtCore.Qt.AlignLeading | QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.Status.setObjectName("Status")
        self.horizontalLayout.addWidget(self.Status)
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setEnabled(True)
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
        self.horizontalLayout.addWidget(self.progressBar)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout, 0, 1, 3, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.MainMenu = QtWidgets.QWidget()
        self.Ui_MainMenu = menu.Ui_MainMenu()
        self.Ui_MainMenu.setupUi(self.MainMenu)

        self.stackedWidget.addWidget(self.MainMenu)

        self.progressBar.setVisible(False)
        self.progressChangedSignal.connect(self.changeProgress)
        self.statusChangedSignal.connect(self.changeStatus)

        self.Status.setText("Waiting for uploading")
        self.Ui_MainMenu.Add.clicked.connect(self.getFiles)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.Status.setText(_translate("MainWindow", "Status"))

    def changeProgress(self, progress):
        self.progressBar.setProperty("value", progress)
        if progress == 0 or progress == 100:
            self.progressBar.setVisible(False)
        else:
            self.progressBar.setVisible(True)

    def changeStatus(self, status, color="black"):
        self.Status.setText(status)
        self.Status.setStyleSheet("color: %s;" % color)

    def getFiles(self):
        file = QFileDialog.getOpenFileNames(
            self, 'Add Files', QtCore.QDir.currentPath(), "Image Files (*.png *.jpg)")
        if len(file[0]) == 0:
            self.changeStatus("No files selected", "red")
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
            self.progressChangedSignal.emit(int(progress / maxProgress * 100))

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
            max_index = max([elem[0] for elem in IMAGELIST])
        else:
            max_index = -1

        final = zip(
            range(max_index + 1, max_index + 1 + len(file[0])), file[0], default_scores, subject_sharpness_scores, centering_scores)

        if len(IMAGELIST):
            final = list(final) + IMAGELIST
        final = sorted(final, key=lambda x: x[2], reverse=True)
        print(final)
        IMAGELIST = final
        self.statusChangedSignal.emit("Successfully loaded", "green")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())