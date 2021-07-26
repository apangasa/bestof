
from PyQt5.QtGui import *
import sys
import numpy as np

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QFileDialog
from torch._C import layout
import res
import json
from analyzing_page import Ui_AnalyzingPage
from main import Ui_MainWindow
from menu import Ui_MainMenu
from settings import Ui_Settings
from results import Ui_Results
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5 import QtCore
from threading import Thread
import time

import bestOf.backend.similarity as similarity
import bestOf.backend.blinkDetector as blinkDetector
import bestOf.backend.cropDetector as cropDetector
import bestOf.backend.evaluateSharpness as evaluateSharpness
import bestOf.backend.identifyPeople as identifyPeople
import bestOf.backend.evaluateCentering as evaluateCentering
import bestOf.backend.sitePackagePathConstructor as sitePackagePathConstructor


def read_settings():
    path = sitePackagePathConstructor.get_site_package_path(
        './bestOf/backend/settings.json')
    settings = {}
    with open(path, 'r') as settings_file:
        settings = json.load(settings_file)
    return settings


def write_settings(settings):
    path = sitePackagePathConstructor.get_site_package_path(
        './bestOf/backend/settings.json')
    with open(path, 'w') as settings_file:
        json.dump(settings, settings_file)


def loadImages(filenames):
    for filename in filenames:
        image = identifyPeople.read_img(filename)
        yield (image * 255).astype(np.uint8)[:, :, :3] if 'png' in filename else image


def simulateAnalyzing(imagelist, groups, settings, callback):
    imagelistLen = len(imagelist)

    maxProgress = 0
    maxProgress += min(1, settings["sharpness"]) * imagelistLen
    maxProgress += min(1, settings["centering"]) * imagelistLen
    maxProgress += min(1, settings["lighting"]) * imagelistLen
    maxProgress += min(1, settings["resolution"]) * imagelistLen
    progress = 0

    if settings["sharpness"]:
        for group in groups:
            for index in group:
                for item in imagelist:
                    if item[0] == index:
                        time.sleep(0.1)  # Analyze sharpness
                        progress += 1
                        callback("sharpness", item[1], int(
                            progress / maxProgress * 100))

    if settings["centering"]:
        for group in groups:
            for index in group:
                for item in imagelist:
                    if item[0] == index:
                        time.sleep(0.1)  # Analyze centering
                        progress += 1
                        callback("centering", item[1], int(
                            progress / maxProgress * 100))

    if settings["lighting"]:
        for group in groups:
            for index in group:
                for item in imagelist:
                    if item[0] == index:
                        time.sleep(0.1)  # Analyze lighting
                        progress += 1
                        callback("lighting", item[1], int(
                            progress / maxProgress * 100))

    if settings["resolution"]:
        for group in groups:
            for index in group:
                for item in imagelist:
                    if item[0] == index:
                        time.sleep(0.1)  # Analyze resolution
                        progress += 1
                        callback("resolution", item[1], int(
                            progress / maxProgress * 100))

    return groups  # should return sorted groups


class BestOfApp(QObject):
    progressChangedSignal = pyqtSignal(int)
    statusChangedSignal = pyqtSignal(str, str)
    analyzingCriteriaChangedSignal = pyqtSignal(str)
    analyzingImageChangedSignal = pyqtSignal(str)
    analyzingFinishedSignal = pyqtSignal()

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
        self.AnalyzingPage = QWidget()
        self.Ui_AnalyzingPage = Ui_AnalyzingPage()
        self.Ui_AnalyzingPage.setupUi(self.AnalyzingPage)
        self.Results = QWidget()
        self.Ui_Results = Ui_Results()
        self.Ui_Results.setupUi(self.Results)

        self.MainWindow.installEventFilter(self)

        self.Ui_MainWindow.stackedWidget.addWidget(self.MainMenu)
        self.Ui_MainWindow.stackedWidget.addWidget(self.Settings)
        self.Ui_MainWindow.stackedWidget.addWidget(self.AnalyzingPage)
        self.Ui_MainWindow.stackedWidget.addWidget(self.Results)

        self.Ui_MainWindow.progressBar.setVisible(False)

        self.Ui_Settings.criteriaChangedSignal.connect(self.onCriteriaChanged)
        self.Ui_Settings.thresholdChangedSignal.connect(
            self.onThresholdChanged)

        self.Ui_MainMenu.Add.clicked.connect(self.getFiles)
        self.Ui_MainMenu.Run.clicked.connect(self.analyzeImages)

        self.Ui_MainMenu.Settings.clicked.connect(
            lambda: self.Ui_MainWindow.stackedWidget.setCurrentIndex(1))
        self.Ui_Settings.Back.clicked.connect(
            lambda: self.Ui_MainWindow.stackedWidget.setCurrentIndex(0))
        self.Ui_Results.Back.clicked.connect(
            lambda: self.Ui_MainWindow.stackedWidget.setCurrentIndex(0))

        self.analyzingCriteriaChangedSignal.connect(
            self.Ui_AnalyzingPage.setCriteria)
        self.analyzingImageChangedSignal.connect(
            self.Ui_AnalyzingPage.setImage)
        self.progressChangedSignal.connect(self.Ui_MainWindow.changeProgress)
        self.statusChangedSignal.connect(self.Ui_MainWindow.changeStatus)
        self.analyzingFinishedSignal.connect(self.onAnalyzingFinished)

        self.settings = read_settings()
        self.Ui_Settings.setSettings(self.settings)

        self.imageList = []
        self.groups = []

        self.MainWindow.show()

    def onCriteriaChanged(self, criteria, value):
        self.settings[criteria] = value

    def onThresholdChanged(self, value):
        self.settings["threshold"] = value

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.Close:
            write_settings(self.settings)
        return super().eventFilter(obj, event)

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

        loaded = []
        if len(self.imageList):
            loaded = [item[1] for item in self.imageList]

        image_generator = loadImages(list(file[0]) + loaded)
        vectors = []
        for image in image_generator:
            v = similarity.generate_feature_vector(image)
            vectors.append(v)
            progress += 1
            self.progressChangedSignal.emit(int(progress / maxProgress * 100))

        groups = similarity.group(
            vectors, threshold=self.settings["threshold"])
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
                self.progressChangedSignal.emit(
                    int(progress / maxProgress * 100))
                continue

            blink_score = (len(subjects) - blinks) / len(subjects)
            crop_score = (len(subjects) - crops) / len(subjects)

            default_score = blink_score + crop_score
            default_scores.append(default_score)

            progress += 1
            self.progressChangedSignal.emit(int(progress / maxProgress * 100))

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
        self.statusChangedSignal.emit(
            "Successfully loaded images! Check Settings, then click Run Analysis to process your images.", "green")

    def analyzeImages(self):
        if len(self.imageList) == 0:
            self.Ui_MainWindow.changeStatus(
                "Images not loaded, upload images first", "red")
            return
        self.Ui_MainWindow.changeStatus("Analyzing...")
        self.Ui_MainWindow.stackedWidget.setCurrentIndex(2)
        thread = Thread(target=self.analyzingThread)
        thread.start()

    def analyzingThread(self):
        self.groups = simulateAnalyzing(self.imageList, self.groups,
                                        self.settings, self.analyzingCallback)
        self.analyzingFinishedSignal.emit()

    def analyzingCallback(self, criteria, image, progress):
        self.analyzingCriteriaChangedSignal.emit(criteria)
        self.analyzingImageChangedSignal.emit(image)
        self.progressChangedSignal.emit(progress)

    def onAnalyzingFinished(self):
        self.Ui_MainWindow.changeStatus(
            "Analyzing finished successfully", "green")
        self.Ui_MainWindow.stackedWidget.setCurrentIndex(3)
        self.Ui_Results.display(self.imageList, self.groups)

    def onImageToggled(self, selected, id):
        pass


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    bestOfApp = BestOfApp()
    sys.exit(app.exec_())
