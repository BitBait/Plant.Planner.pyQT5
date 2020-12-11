from PyQt5.QtWidgets import *
from windows.web import fetch
from pandas import DataFrame, read_csv
import seaborn as sns
import matplotlib.pyplot as plt

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
                self.yearsBox.setEnabled(False)
                break
            if character == " ":
                pass
            elif character == ",":
                self.vegList.append(string)
                self.numberplantedList.append(int(self.numberplanted.text()))
                self.seasonsList.append(str(self.seasonsBox.currentText()))
                self.yearsList.append(str(self.yearsBox.currentText()))
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
        dataframe.to_csv("files/{year}.csv".format(year=year))
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
            elif vegetable == "Brassicaceae":
                self.vegfamilyList.append("Brassica")
            elif vegetable == "chenopodiaceae":
                self.vegfamilyList.append("Chenopodiaceae")



class ViewDataWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("View Vegetable Data")
        self.layout = QGridLayout()
        self.dataFrame = None

        self.label = QLabel("Choose year and\nseason to view: ")
        self.layout.addWidget(self.label, 0, 0)

        self.yearsBox = QComboBox()
        for i in range(100):
            i = i + 2000
            self.yearsBox.addItem(str(i))
        self.layout.addWidget(self.yearsBox, 0, 1)

        self.submitButton = QPushButton("Get data", self)
        self.submitButton.clicked.connect(self.loaddata)
        self.layout.addWidget(self.submitButton, 1, 1)

        self.setLayout(self.layout)

    def loaddata(self):
        try:
            year = self.yearsBox.currentText()
            file = "files/{year}.csv".format(year=year)
            dataframe = read_csv(file)
            self.dataFrame = dataframe
            self.showdata()
        except:
            print("File Not Found")

    def showdata(self):
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
        self.layout.addWidget(self.label, 0, 0)
        self.layout.addWidget(self.submitButton, 1, 1)
        self.layout.addWidget(self.yearsBox, 0, 1)
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
        self.algorithmsList = ["Simple"]
        self.vegFamilyList = ["Solanaceae", "Asteraceae", "Amaryllidaceae", "Fabaceae", "Cucurbitaceae", "Apiaceae", "Brassicaceae", "Chenopodiaceae"]
        self.layout = QGridLayout()

        self.label = QLabel("What year do you want to predict: ")
        self.layout.addWidget(self.label, 0, 0)

        self.yearsBox = QComboBox()
        for i in range(100):
            i = i + 2000
            self.yearsBox.addItem(str(i))
        self.layout.addWidget(self.yearsBox, 0, 1)

        self.label2 = QLabel("Choose algorithm: ")
        self.layout.addWidget(self.label2, 1, 0)

        self.algorithmBox = QComboBox()
        for alg in self.algorithmsList:
            self.algorithmBox.addItem(alg)
        self.layout.addWidget(self.algorithmBox, 1, 1)

        self.predButton = QPushButton("Predict")
        self.predButton.clicked.connect(self.predict)
        self.layout.addWidget(self.predButton, 2, 0, 1, 2)

        self.setLayout(self.layout)

    def predict(self):
        algorithm = self.algorithmBox.currentText()
        if algorithm == "Simple":
            year = self.yearsBox.currentText()
            prevyear = str(int(year) - 1)
            nextyear = str(int(year) + 1)

            try:
                file = "files/{year}.csv".format(year=prevyear)
                dataframe = read_csv(file)
                print(dataframe)

            except:
                print("File Not Found, possible no previous year try again")

            winter = dataframe[dataframe.loc[:, "Season Planted"] == "Winter"]
            spring = dataframe[dataframe.loc[:, "Season Planted"] == "Spring"]
            summer = dataframe[dataframe.loc[:, "Season Planted"] == "Summer"]
            autumn = dataframe[dataframe.loc[:, "Season Planted"] == "Autumn"]

            winterfamily = winter.loc[:, "Vegetable Family"].items()
            winterFamilyList = []
            for i, j in winterfamily:
                winterFamilyList.append(j)
            winterplantnextyear = []
            for i in self.vegFamilyList:
                if i in winterFamilyList:
                    pass
                else:
                    winterplantnextyear.append(i)

            if winterFamilyList == []:
                winterFamilyList = [""]

            springfamily = spring.loc[:, "Vegetable Family"].items()
            springFamilyList = []
            for i, j in springfamily:
                springFamilyList.append(j)
            springplantnextyear = []
            for i in self.vegFamilyList:
                if i in springFamilyList:
                    pass
                else:
                    springplantnextyear.append(i)

            if springFamilyList == []:
                springFamilyList = [""]

            summerfamily = summer.loc[:, "Vegetable Family"].items()
            summerFamilyList = []
            for i, j in summerfamily:
                summerFamilyList.append(j)
            summerplantnextyear = []
            for i in self.vegFamilyList:
                if i in summerFamilyList:
                    pass
                else:
                    summerplantnextyear.append(i)

            if summerFamilyList == []:
                summerFamilyList = [""]

            autumnfamily = autumn.loc[:, "Vegetable Family"].items()
            autumnFamilyList = []
            for i, j in autumnfamily:
                autumnFamilyList.append(j)
            autumnplantnextyear = []
            for i in self.vegFamilyList:
                if i in autumnFamilyList:
                    pass
                else:
                    autumnplantnextyear.append(i)

            if autumnFamilyList == []:
                autumnFamilyList = [""]

            output = f"In the winter of {prevyear} you planted {set(winterFamilyList)}" \
                          f", so in the winter of {year}, you should plant {winterplantnextyear}. In the" \
                          f"spring of {prevyear} you planted {set(springFamilyList)}, so in the spring of {year}," \
                          f"you should plant {springplantnextyear}. In the summer of {prevyear} you planted {set(summerFamilyList)}," \
                     f"so in the spring of {year}, you should plant {summerplantnextyear}. Finally in the autumn of {prevyear}" \
                     f"you planted {set(autumnFamilyList)}, so in the spring of {year}, you should plant {autumnplantnextyear}"

            outputlabel = QLabel(output)
            outputlabel.setWordWrap(True)

            self.layout.addWidget(outputlabel, 3, 0)

        # elif algorithm == "Complex":


class PlotWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plots")
        self.plots = ["Simple Summary"]
        self.layout = QGridLayout()
        self.dataFrame = None
        self.plot = None

        self.label = QLabel("Choose year and\nseason to view: ")
        self.layout.addWidget(self.label, 0, 0)

        self.yearsBox = QComboBox()
        for i in range(100):
            i = i + 2000
            self.yearsBox.addItem(str(i))
        self.layout.addWidget(self.yearsBox, 0, 1)

        self.submitButton = QPushButton("Get data", self)
        self.submitButton.clicked.connect(self.loaddata)
        self.layout.addWidget(self.submitButton, 1, 1)

        self.plottype = QComboBox()
        for i in self.plots:
            self.plottype.addItem(i)
        self.layout.addWidget(self.plottype, 0, 2)

        self.plotthedata = QPushButton("Plot Data")
        self.plotthedata.clicked.connect(self.plotdata)
        self.layout.addWidget(self.plotthedata, 1, 2)

        self.setLayout(self.layout)

    def loaddata(self):
        try:
            year = self.yearsBox.currentText()
            file = "files/{year}.csv".format(year=year)
            dataframe = read_csv(file)
            self.dataFrame = dataframe
        except:
            print("File Not Found")

    def plotdata(self):
        self.plot = self.plottype.currentText()
        if self.plot == "Simple Summary":
            myplot = sns.barplot(data=self.dataFrame, x="Season Planted", y="Number Planted", hue="Vegetable")
            plt.show()

class centraltab(QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.tab1 = EnterDataWindow()
        self.tab2 = ViewDataWindow()
        self.tab3 = PredictWindow()
        self.tab4 = PlotWindow()

        self.addTab(self.tab1, self.tab1.windowTitle())
        self.addTab(self.tab2, self.tab2.windowTitle())
        self.addTab(self.tab3, self.tab3.windowTitle())
        self.addTab(self.tab4, self.tab4.windowTitle())