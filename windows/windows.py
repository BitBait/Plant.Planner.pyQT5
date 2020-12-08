from PyQt5.QtWidgets import *
from windows.web import fetch
from pandas import DataFrame, read_csv

brassicas = ["broccoli", "cauliflower", "brussel sprouts", "kale", "kohl rabi", "collards", "turnip",
             "mustard greens", "asian greens", "bok choi", "radish"]


class EnterDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.vegList = []
        self.numberplantedList = []
        self.vegfamilyList = []
        self.seasons = ["Winter", "Spring", "Summer", "Autumn"]
        self.seasonsList = []
        self.yearsList = []
        self.vegfamilygroupingList = []
        self.setWindowTitle("Enter Vegetable Data")
        self.layout = QGridLayout()

        self.label = QLabel("Enter Data\n(comma at the end\n of every vegetable): ")
        self.layout.addWidget(self.label, 0, 0)

        self.textbox = QLineEdit(self)
        self.layout.addWidget(self.textbox, 0, 1)

        self.submitbox = QPushButton("Submit Vegetable",self)
        self.submitbox.clicked.connect(self.submit)
        self.layout.addWidget(self.submitbox, 0, 2)

        self.label2 = QLabel("Enter number planted: ")
        self.layout.addWidget(self.label2, 1, 0)

        self.numberplanted = QLineEdit(self)
        self.layout.addWidget(self.numberplanted, 1, 1)

        self.savebox = QPushButton("Save all data", self)
        self.savebox.clicked.connect(self.save)
        self.layout.addWidget(self.savebox, 4, 1)

        self.label3 = QLabel("Choose the season planted: ")
        self.layout.addWidget(self.label3, 2, 0)

        self.seasonsBox = QComboBox()
        for s in self.seasons:
            self.seasonsBox.addItem(s)
        self.layout.addWidget(self.seasonsBox, 2, 1)

        self.label4 = QLabel("Choose year planted: ")
        self.layout.addWidget(self.label4, 3, 0)

        self.yearsBox = QComboBox()
        for i in range(100):
            i = i + 2000
            self.yearsBox.addItem(str(i))
        self.layout.addWidget(self.yearsBox, 3, 1)

        self.setLayout(self.layout)

    def submit(self):
        string = ""
        for character in self.textbox.text():
            if self.textbox.text() in self.vegList:
                break
            if "," not in self.textbox.text():
                string = self.textbox.text()
                self.vegList.append(string.lower())
                self.numberplantedList.append(int(self.numberplanted.text()))
                self.seasonsList.append(str(self.seasonsBox.currentText()))
                self.yearsList.append(str(self.yearsBox.currentText()))
                self.seasonsBox.setEnabled(False)
                self.yearsBox.setEnabled(False)
                break
            if character == " ":
                pass
            elif character == ",":
                self.vegList.append(string)
                self.numberplantedList.append(int(self.numberplanted.text()))
                self.seasonsList.append(str(self.seasonsBox.currentText()))
                self.yearsList.append(str(self.yearsBox.currentText()))
                self.seasonsBox.setEnabled(False)
                self.yearsBox.setEnabled(False)
                self.textbox.setText("")
                self.numberplanted.setText("")
                string = ""
            else:
                string += character.lower()
        print(self.vegList)

    def save(self):
        self.googleveg()
        dataframe = DataFrame({
            "Vegetable": self.vegList,
            "Number Planted": self.numberplantedList,
            "Vegetable Family": self.vegfamilyList,
            "Season Planted": self.seasonsList,
            "Year Planted": self.yearsList
        })
        print(dataframe)
        year = str(self.yearsList[0])
        season = str(self.seasonsList[0])
        dataframe.to_csv("files/{year}-{season}.csv".format(year=year, season=season))
        self.seasonsBox.setEnabled(True)
        self.yearsBox.setEnabled(True)

    def googleveg(self):
        for vegetable in self.vegList:
            try:
                family = fetch.getVegFamily(str(vegetable))
                self.vegfamilyList.append(family)
                family = ""
            except:
                family = "NA"
                self.vegfamilyList.append(family)
                family = ""

    def groupfamilies(self):
        for vegetable in self.vegfamilyList:
            if vegetable == "Solanaceae":
                self.vegfamilyList.append("Nightshades")
            elif vegetable == "Asteraceae":
                self.vegfamilyList.append("Sunflower")
            elif vegetable == "Amaryllidaceae":
                self.vegfamilyList.append("Alliums")
            elif vegetable == "Fabaceae":
                self.vegfamilyList.append("Legumes")
            elif vegetable == "Cucurbitaceae":
                self.vegfamilyList.append("Gourds")
            elif vegetable == "Apiaceae":
                self.vegfamilyList.append("Carrot")


class ViewDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Vegetable Data")
        self.layout = QGridLayout()
        self.seasons = ["Winter", "Spring", "Summer", "Autumn"]
        self.dataFrame = None

        self.label = QLabel("Choose year and\nseason to view: ")
        self.layout.addWidget(self.label, 0, 0)

        self.seasonsBox = QComboBox()
        for s in self.seasons:
            self.seasonsBox.addItem(s)
        self.layout.addWidget(self.seasonsBox, 0, 1)

        self.yearsBox = QComboBox()
        for i in range(100):
            i = i + 2000
            self.yearsBox.addItem(str(i))
        self.layout.addWidget(self.yearsBox, 0, 2)

        self.submitButton = QPushButton("Get data", self)
        self.submitButton.clicked.connect(self.loaddata)
        self.layout.addWidget(self.submitButton, 1, 1)

        self.setLayout(self.layout)

    def loaddata(self):
        year = self.yearsBox.currentText()
        season = self.seasonsBox.currentText()
        file = "files/{year}-{season}.csv".format(year=year, season=season)
        dataframe = read_csv(file)
        self.dataFrame = dataframe
        print(self.dataFrame)
        self.showdata()

    def showdata(self):
        for i, j in enumerate(self.dataFrame.columns):
            label = QLabel(str(j))
            self.layout.addWidget(label, 3, i)
            for k, data in enumerate(self.dataFrame.loc[:, str(j)]):
                label = QLabel(str(data))
                self.layout.addWidget(label, k+4, i)


class PredictWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Predict")
        self.layout = QGridLayout()

class centraltab(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.tab1 = EnterDataWindow()
        self.tab2 = ViewDataWindow()
        self.tab3 = PredictWindow()

        self.addTab(self.tab1, self.tab1.windowTitle())
        self.addTab(self.tab2, self.tab2.windowTitle())
        self.addTab(self.tab3, self.tab3.windowTitle())