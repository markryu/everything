# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'first_try.ui',
# licensing of 'first_try.ui' applies.
#
# Created: Wed Mar  6 17:42:16 2019
#      by: pyside2-uic  running on PySide2 5.12.1
# WARNING! All changes made in this file will be lost!

import pandas as pd
from mailmerge import MailMerge
from PySide2 import QtCore, QtGui, QtWidgets
from PySide2.QtWidgets import QFileDialog
import os

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Sticker Templating")
        Dialog.resize(800, 320)
        Dialog.setMinimumSize(QtCore.QSize(800, 320))

        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(580, 230, 181, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")

        self.widget = QtWidgets.QWidget(Dialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 381, 211))
        self.widget.setMinimumSize(QtCore.QSize(381, 141))
        self.widget.setObjectName("widget")

        self.csvLabel = QtWidgets.QLabel(self.widget)
        self.csvLabel.setGeometry(QtCore.QRect(10, 30, 101, 21))
        self.csvLabel.setObjectName("csvLabel")

        self.templateLabel = QtWidgets.QLabel(self.widget)
        self.templateLabel.setGeometry(QtCore.QRect(10, 90, 121, 21))
        self.templateLabel.setObjectName("templateLabel")

        self.outputLabel = QtWidgets.QLabel(self.widget)
        self.outputLabel.setGeometry(QtCore.QRect(10, 150, 111, 21))
        self.outputLabel.setObjectName("outputLabel")

        self.openCsv = QtWidgets.QPushButton(self.widget)
        self.openCsv.setGeometry(QtCore.QRect(190, 20, 161, 31))
        self.openCsv.setObjectName("openCsv")

        self.openTemplate = QtWidgets.QPushButton(self.widget)
        self.openTemplate.setGeometry(QtCore.QRect(190, 80, 161, 31))
        self.openTemplate.setObjectName("openTemplate")

        self.outputFolder = QtWidgets.QPushButton(self.widget)
        self.outputFolder.setGeometry(QtCore.QRect(190, 130, 161, 31))
        self.outputFolder.setObjectName("outputFolder")

        self.fileLabelCsv = QtWidgets.QLabel(self.widget)
        self.fileLabelCsv.setGeometry(QtCore.QRect(190, 50, 151, 20))
        self.fileLabelCsv.setObjectName("fileLabelCsv")

        self.fileLabelTemplate = QtWidgets.QLabel(self.widget)
        self.fileLabelTemplate.setGeometry(QtCore.QRect(190, 110, 151, 20))
        self.fileLabelTemplate.setObjectName("fileLabelTemplate")

        self.fileLabelOutput = QtWidgets.QLabel(self.widget)
        self.fileLabelOutput.setGeometry(QtCore.QRect(190, 170, 151, 20))
        self.fileLabelOutput.setObjectName("fileLabelOutput")

        self.widget_2 = QtWidgets.QWidget(Dialog)
        self.widget_2.setGeometry(QtCore.QRect(410, 10, 381, 211))
        self.widget_2.setMinimumSize(QtCore.QSize(380, 0))
        self.widget_2.setObjectName("widget_2")

        self.label_8 = QtWidgets.QLabel(self.widget_2)
        self.label_8.setGeometry(QtCore.QRect(0, 10, 251, 21))
        self.label_8.setObjectName("label_8")

        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.widget_2)
        self.plainTextEdit.setGeometry(QtCore.QRect(60, 50, 301, 151))
        self.plainTextEdit.setObjectName("plainTextEdit")

        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(230, 230, 151, 31))
        self.pushButton_3.setObjectName("pushButton_3")


        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.openCsv.clicked.connect(self.csvOpen)
        self.openTemplate.clicked.connect(self.templateOpen)
        self.outputFolder.clicked.connect(self.getOutputFolder)
        self.pushButton_3.clicked.connect(self.stickerTemplate)

    def stickerTemplate(self):
        positions_needed = self.plainTextEdit.toPlainText()
        csv_filename = self.fileLabelCsv.text()
        template_filename = self.fileLabelTemplate.text()
        output_folder = self.fileLabelOutput.text()

        df = pd.read_csv(f"{csv_filename}", encoding ='ISO-8859-1')
        df = df.astype(str)
        
        template = f'{template_filename}'
        document = MailMerge(template)
        positions = positions_needed.split('\n')
        list_per_company_per_position = list()
        for each_row in df.iterrows():

            for position in positions:
                company_address = each_row[1].address
                company = each_row[1].company
                receiver_name = position
        
                list_per_company_per_position.append({'receiver':receiver_name,
                                'address': company_address,
                                'company': company
                                })
        
        document.merge_rows('receiver', list_per_company_per_position)        
        document.write(f'{output_folder}/stickerOutput.docx')
        document.close()

    def csvOpen(self):
        csv_filename = QFileDialog.getOpenFileName(None, 'Open CSV', '', 'CSV files (*.csv)')
        self.fileLabelCsv.setText(csv_filename[0])

    def templateOpen(self):
        template_filename = QFileDialog.getOpenFileName(None, 'Open template', '', 'DOC files (*.doc, *.docx)')
        self.fileLabelTemplate.setText(template_filename[0])

    def getOutputFolder(self):
        outputFolder = os.path.normpath(QFileDialog.getExistingDirectory(None, 'Open Folder', '', QFileDialog.ShowDirsOnly))
        self.fileLabelOutput.setText(outputFolder)
            
    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtWidgets.QApplication.translate("Dialog", "Dialog", None, -1))
        self.csvLabel.setText(QtWidgets.QApplication.translate("Dialog", "CSV Filename", None, -1))
        self.templateLabel.setText(QtWidgets.QApplication.translate("Dialog", "Template Filename", None, -1))
        self.outputLabel.setText(QtWidgets.QApplication.translate("Dialog", "Output Filename", None, -1))
        self.openCsv.setText(QtWidgets.QApplication.translate("Dialog", "Open CSV", None, -1))
        self.openTemplate.setText(QtWidgets.QApplication.translate("Dialog", "Open Template", None, -1))
        self.outputFolder.setText(QtWidgets.QApplication.translate("Dialog", "Open Folder", None, -1))
        self.fileLabelCsv.setText(QtWidgets.QApplication.translate("Dialog", "<html><head/><body><p><span style=\" font-size:6pt;\">Open CSV</span></p></body></html>", None, -1))
        self.fileLabelTemplate.setText(QtWidgets.QApplication.translate("Dialog", "<html><head/><body><p><span style=\" font-size:6pt;\">Open Template</span></p></body></html>", None, -1))
        self.fileLabelOutput.setText(QtWidgets.QApplication.translate("Dialog", "<html><head/><body><p><span style=\" font-size:6pt;\">Output name</span></p></body></html>", None, -1))
        self.label_8.setText(QtWidgets.QApplication.translate("Dialog", "Positions Separated per new line", None, -1))
        self.plainTextEdit.setPlainText(QtWidgets.QApplication.translate("Dialog", "COO / General Manager\n"
"Procurement Head\n"
"HR Manager", None, -1))
        self.pushButton_3.setText(QtWidgets.QApplication.translate("Dialog", "RUN Templating", None, -1))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
