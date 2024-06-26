import sys

from PyQt5.QtCore import QFileInfo, Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox, QFontDialog, QColorDialog
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from GUI.pyNotePadGUI import Ui_MainWindow


class NotePadWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.setup_connects()
        self.show()

    def setup_connects(self):
        # File menu actions
        self.actionSave.triggered.connect(self.save_file)
        self.actionNew.triggered.connect(self.new_file)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionPrint.triggered.connect(self.print_file)
        self.actionPrint_Preview.triggered.connect(self.preview_dialog)
        self.actionExport_PDF.triggered.connect(self.export_pdf)
        self.actionQuit.triggered.connect(self.exit_app)

        # Edit menu actions
        self.actionUndo.triggered.connect(self.textEdit.undo)
        self.actionRedo.triggered.connect(self.textEdit.redo)
        self.actionCut.triggered.connect(self.textEdit.cut)
        self.actionCopy.triggered.connect(self.textEdit.copy)
        self.actionPaste.triggered.connect(self.textEdit.paste)

        # Format menu actions
        self.actionBold.triggered.connect(self.bold_text)
        self.actionItalic.triggered.connect(self.italic_text)
        self.actionUnderline.triggered.connect(self.underline_text)
        self.actionLeft.triggered.connect(self.align_left_text)
        self.actionCenter.triggered.connect(self.align_center_text)
        self.actionRight.triggered.connect(self.align_right_text)
        self.actionJustify.triggered.connect(self.justify_text)
        self.actionFont.triggered.connect(self.font_dialog)
        self.actionColor.triggered.connect(self.color_dialog)

        # About menu actions
        self.actionAbout_App.triggered.connect(self.about)

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

    def bold_text(self):
        font = QFont()
        font.setBold(True)
        self.textEdit.setFont(font)

    def italic_text(self):
        font = QFont()
        font.setItalic(True)
        self.textEdit.setFont(font)

    def underline_text(self):
        font = QFont()
        font.setUnderline(True)
        self.textEdit.setFont(font)

    def align_left_text(self):
        self.textEdit.setAlignment(Qt.AlignLeft)

    def align_center_text(self):
        self.textEdit.setAlignment(Qt.AlignCenter)

    def align_right_text(self):
        self.textEdit.setAlignment(Qt.AlignRight)

    def justify_text(self):
        self.textEdit.setAlignment(Qt.AlignJustify)

    def font_dialog(self):
        font, ok = QFontDialog.getFont()

        if ok:
            self.textEdit.setFont(font)

    def color_dialog(self):
        color = QColorDialog.getColor()
        self.textEdit.setTextColor(color)

    def about(self):
        QMessageBox.information(self, "About NotePad", "This is a simple note taking application.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NotePadWindow()
    sys.exit(app.exec_())
