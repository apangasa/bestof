
import cv2 as cv
from PyQt5 import QtWidgets
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import sys
sys.path.insert(1, '../backend/')
import similarity


def loadImages(filenames):
    for filename in filenames:
        yield cv.imread(filename)


# Reference Source 1: https://learndataanalysis.org/how-to-pass-data-from-one-window-to-another-pyqt5-tutorial/


def main():
    class processingResults(QWidget):
        def __init__(self):
            super().__init__()
            self.options()
            self.setWindowTitle("GoodPics")
            self.setGeometry(1550, 800, 500, 500)
            self.layout = QVBoxLayout()
            self.layout.addWidget(self.des)
            self.setLayout(self.layout)

        def display(self):
            self.show()

        def options(self):
            self.des = QGroupBox("Images Selected.",
                                 alignment=QtCore.Qt.AlignCenter)
            layout = QHBoxLayout()
            self.redo = QPushButton('&Run Again')
            self.redo.clicked.connect(self.imageProcessing)
            layout.addWidget(self.redo)
            self.back = QPushButton('&Back to Main Menu')
            self.back.clicked.connect(self.close)
            layout.addWidget(self.back)
            self.des.setLayout(layout)

        def imageProcessing(self):
            # Code from backend goes here...
            print("Redoing image selection.")

    class settingsMenu(QWidget):
        def __init__(self):
            super().__init__()
            self.options()
            self.setWindowTitle("Settings Menu")
            self.setGeometry(1550, 800, 500, 500)
            self.layout = QVBoxLayout()
            self.layout.addWidget(self.des)
            self.setLayout(self.layout)

        def display(self):
            self.show()

        def options(self):
            self.des = QGroupBox("Apply the following criteria for image refinement.",
                                 alignment=QtCore.Qt.AlignCenter)
            layout = QHBoxLayout()

            self.closeButton = QPushButton('&Close Settings')
            self.closeButton.clicked.connect(self.close)
            layout.addWidget(self.closeButton)
            self.des.setLayout(layout)

    class mainWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("GoodPics: Main Menu")
            self.resize(800, 800)
            self.setGeometry(1550, 800, 500, 500)
            self.nextWindow = settingsMenu()
            self.process = processingResults()
            self.makeUI()
            self.layout = QVBoxLayout()
            self.layout.addWidget(self.firstText)
            self.setLayout(self.layout)

        def makeUI(self):
            self.firstText = QGroupBox("Welcome, browse your computer for images to start picture analysis.",
                                       alignment=QtCore.Qt.AlignCenter)
            layout = QHBoxLayout()
            self.addImage = QPushButton('&Add Images')
            self.addImage.clicked.connect(self.getFiles)
            layout.addWidget(self.addImage)
            self.processImage = QPushButton('&Process Image(s)')
            self.processImage.clicked.connect(self.process.display)
            layout.addWidget(self.processImage)
            self.settings = QPushButton('&More Settings')
            self.settings.clicked.connect(self.nextWindow.display)
            layout.addWidget(self.settings)
            self.firstText.setLayout(layout)

        # Grabs the files for image selection... work in progress...

        def getFiles(self):
            file = QFileDialog.getOpenFileNames(
                self, 'Add Files', QtCore.QDir.rootPath())
            files = ""
            layout = QVBoxLayout
            image_generator = loadImages(list(file[0]))
            vectors = []
            for image in image_generator:
                v = similarity.generate_feature_vector(image)
                vectors.append(v)

            threshold = 0.8  # this should be grabbed from whatever the user set it to in the settings
            groups = similarity.group(vectors, threshold=threshold)
            print(groups)

    newApp = QApplication(sys.argv)  # Creates application class
    wind = mainWindow()
    wind.show()
    newApp.exec()  # Executes app with the window


if __name__ == '__main__':
    main()
