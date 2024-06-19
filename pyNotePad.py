import sys

from PyQt5.QtCore import QFileInfo
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
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
        self.actionPrint.triggered.connect(self.print_file)
        self.actionPrint_Preview.triggered.connect(self.preview_dialog)
        self.actionExport_PDF.triggered.connect(self.export_pdf)
        self.actionQuit.triggered.connect(self.exit_app)

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

    def print_file(self):
        """
        Print the contents of the textEdit widget to the printer.

        This function opens a print dialog and allows the user to select a printer and configure the printing settings.
        If the user accepts the dialog, the contents of the textEdit widget are printed using the selected printer.
        """
        printer = QPrinter(QPrinter.HighResolution)
        dialog = QPrintDialog(printer)

        if dialog.exec_() == QPrintDialog.Accepted:
            self.textEdit.print(printer)

    def preview_dialog(self):
        """
        Opens a print preview dialog for the current text in the textEdit widget.

        This function creates a QPrinter object with high resolution and assigns it to the `printer` variable.
        Then, it creates a QPrintPreviewDialog object with the `printer` and `self` as arguments and assigns it to the `preview_dialog` variable.
        The `paintRequested` signal of the `preview_dialog` is connected to the `print_preview` method.
        Finally, the `exec_` method of the `preview_dialog` is called to display the print preview dialog.
        """
        printer = QPrinter(QPrinter.HighResolution)
        preview_dialog = QPrintPreviewDialog(printer, self)
        preview_dialog.paintRequested.connect(self.print_preview)
        preview_dialog.exec_()

    def print_preview(self, printer):
        """
        A function that prints a preview of the text in the textEdit widget using the provided printer.

        Parameters:
            printer: The printer object to use for printing the text.
        """
        self.textEdit.print(printer)

    def export_pdf(self):
        """
        Export the contents of the textEdit widget to a PDF file.

        This function opens a file dialog and prompts the user to select a file to save the PDF.
        If a file is selected, the function creates a QPrinter object with high resolution and sets the output format to PDF.
        The output file name is set to the selected file name or the selected file name with a ".pdf" extension if it doesn't have one.
        The contents of the textEdit widget are then printed to the PDF file using the print method of the document.
        """
        filename, _ = QFileDialog.getSaveFileName(self, 'Export PDF', '', '.pdf')

        if filename and filename != "":
            if QFileInfo(filename).suffix() == "":
                filename += ".pdf"

            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(filename)
            self.textEdit.document().print(printer)

    def exit_app(self):
        """
        Closes the application by calling the `close()` method of the current object.
        """
        self.close()


app = QApplication(sys.argv)
window = NotePadWindow()
sys.exit(app.exec_())
