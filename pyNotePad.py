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
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)

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

    def maybe_save(self):
        """
        A function that handles the action of saving a file.
        It checks if the text is modified, prompts the user with a warning message,
        and based on the user's choice, it either saves the file using the save_file method
        or cancels the operation. Returns True if the operation completes successfully.
        """
        if not self.textEdit.document().isModified():
            return True

        ret = QMessageBox.warning(
            self, 'Application',
            "The document has been modified.\n"
            "Do you want to save your changes ?",
            QMessageBox.Save | QMessageBox.Discard | QMessageBox.Cancel
        )

        if ret == QMessageBox.Save:
            self.save_file()
        if ret == QMessageBox.Cancel:
            return False
        return True

    def new_file(self):
        """
        Clears the text in the textEdit widget if the user chooses to save any changes.

        This function first checks if there are any changes made to the text in the textEdit widget.
        If there are changes, it prompts the user with a warning message asking if they want to save their changes.
        If the user chooses to save their changes, the function calls the `save_file` method to save the file.
        If the user chooses not to save their changes or cancels the operation, the function continues without saving the file.
        Regardless of the user's choice, the function clears the text in the textEdit widget.

        Parameters:
            None

        Returns:
            None
        """
        if self.maybe_save():
            self.textEdit.clear()

    def open_file(self):
        """
        A function that opens a file dialog to select a file to open, reads the content of the selected file,
        and sets the content to the text edit widget.
        """
        filename = QFileDialog.getOpenFileName(self, 'Open File', '', 'Text files (*.txt)')

        if filename[0]:
            with open(filename[0], 'r', encoding='utf-8') as file:
                self.textEdit.setText(file.read())


app = QApplication(sys.argv)
window = NotePadWindow()
sys.exit(app.exec_())
