import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from GUI.pyNotePadGUI import Ui_MainWindow


class NotePadWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.show()


app = QApplication(sys.argv)
window = NotePadWindow()
sys.exit(app.exec_())
