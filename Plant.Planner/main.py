import sys
from PyQt5.QtWidgets import *
from windows.windows import centraltab

if __name__ == "__main__":
    app = QApplication([])
    window = centraltab()
    window.show()
    sys.exit(app.exec_())
