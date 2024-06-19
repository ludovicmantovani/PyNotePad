import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from GUI.pyNotePadGUI import Ui_MainWindow


class NotePadWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setup_connects()
        self.show()

    def setup_connects(self):
        self.actionSave.triggered.connect(self.save_file)

    def save_file(self):
        """
        Save the current file.

        This function prompts the user to select a file to save.
        If a file is selected, the function opens the file in write mode and writes the content of the text edit widget to it.
        After the file is saved, a message box is displayed to inform the user that the file has been saved successfully.

        Parameters:
            None

        Returns:
            None
        """
        filename = QFileDialog.getSaveFileName(self, 'Save File', '', 'Text files (*.txt)')

        if filename[0]:
            with open(filename[0], 'w', encoding='utf-8') as file:
                file.write(self.textEdit.toPlainText())
            QMessageBox.information(self, 'Save File', 'File saved successfully')


app = QApplication(sys.argv)
window = NotePadWindow()
sys.exit(app.exec_())
