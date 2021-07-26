
from PyQt5.QtGui import *
import sys
import numpy as np

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
import res
from main import Ui_MainWindow
from menu import Ui_MainMenu
from settings import Ui_Settings
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5 import QtCore
from threading import Thread

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


class BestOfApp(QObject):
    progressChangedSignal = pyqtSignal(int)
    statusChangedSignal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.MainWindow = QMainWindow()
        self.Ui_MainWindow = Ui_MainWindow()
        self.Ui_MainWindow.setupUi(self.MainWindow)
        self.MainMenu = QWidget()
        self.Ui_MainMenu = Ui_MainMenu()
        self.Ui_MainMenu.setupUi(self.MainMenu)
        self.Settings = QWidget()
        self.Ui_Settings = Ui_Settings()
        self.Ui_Settings.setupUi(self.Settings)

        self.Ui_MainWindow.stackedWidget.addWidget(self.MainMenu)
        self.Ui_MainWindow.stackedWidget.addWidget(self.Settings)

        self.Ui_MainWindow.progressBar.setVisible(False)

        self.Ui_MainMenu.Add.clicked.connect(self.getFiles)
        self.Ui_MainMenu.Settings.clicked.connect(
            lambda: self.Ui_MainWindow.stackedWidget.setCurrentIndex(1))
        self.Ui_Settings.Back.clicked.connect(
            lambda: self.Ui_MainWindow.stackedWidget.setCurrentIndex(0))
        self.progressChangedSignal.connect(self.Ui_MainWindow.changeProgress)
        self.statusChangedSignal.connect(self.Ui_MainWindow.changeStatus)

        self.imageList = []
        self.groups = []

        self.MainWindow.show()

    def getFiles(self):
        file = QFileDialog.getOpenFileNames(
            self.MainWindow, 'Add Files', QtCore.QDir.currentPath(), "Image Files (*.png *.jpg)")
        if len(file[0]) == 0:
            self.Ui_MainWindow.changeStatus("No files selected", "red")
            return
        self.Ui_MainWindow.changeStatus("Reading images...")
        thread = Thread(target=self.loadFiles, args=(file,))
        thread.start()

    def loadFiles(self, file):
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
        self.groups = groups

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

        if len(self.imageList):
            max_index = max([elem[0] for elem in self.imageList])
        else:
            max_index = -1

        final = zip(
            range(max_index + 1, max_index + 1 + len(file[0])), file[0], default_scores, subject_sharpness_scores, centering_scores)

        if len(self.imageList):
            final = list(final) + self.imageList
        final = sorted(final, key=lambda x: x[2], reverse=True)
        print(final)
        self.imageList = final
        self.statusChangedSignal.emit("Successfully loaded images! Check Settings, then click Run Analysis to process your images.", "green")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    bestOfApp = BestOfApp()
    sys.exit(app.exec_())
