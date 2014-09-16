# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'menu.ui'
#
# Created: Tue Sep  9 15:10:38 2014
#      by: PyQt4 UI code generator 4.11.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_main_menu(object):
    def setupUi(self, main_menu):
        main_menu.setObjectName(_fromUtf8("main_menu"))
        main_menu.resize(398, 323)
        self.verticalLayoutWidget = QtGui.QWidget(main_menu)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 60, 160, 201))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.left_row = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.left_row.setMargin(0)
        self.left_row.setObjectName(_fromUtf8("left_row"))
        self.b_download_source = QtGui.QPushButton(self.verticalLayoutWidget)
        self.b_download_source.setObjectName(_fromUtf8("b_download_source"))
        self.left_row.addWidget(self.b_download_source)
        self.b_create_bag = QtGui.QPushButton(self.verticalLayoutWidget)
        self.b_create_bag.setObjectName(_fromUtf8("b_create_bag"))
        self.left_row.addWidget(self.b_create_bag)
        self.b_validate_bag = QtGui.QPushButton(self.verticalLayoutWidget)
        self.b_validate_bag.setObjectName(_fromUtf8("b_validate_bag"))
        self.left_row.addWidget(self.b_validate_bag)
        self.b_upload_bag = QtGui.QPushButton(self.verticalLayoutWidget)
        self.b_upload_bag.setObjectName(_fromUtf8("b_upload_bag"))
        self.left_row.addWidget(self.b_upload_bag)
        self.verticalLayoutWidget_2 = QtGui.QWidget(main_menu)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(210, 150, 160, 111))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.right_row = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.right_row.setMargin(0)
        self.right_row.setObjectName(_fromUtf8("right_row"))
        self.b_configure = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.b_configure.setObjectName(_fromUtf8("b_configure"))
        self.right_row.addWidget(self.b_configure)
        self.b_quit = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.b_quit.setObjectName(_fromUtf8("b_quit"))
        self.right_row.addWidget(self.b_quit)
        self.label = QtGui.QLabel(main_menu)
        self.label.setGeometry(QtCore.QRect(240, 50, 101, 75))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(main_menu)
        QtCore.QMetaObject.connectSlotsByName(main_menu)
        main_menu.setTabOrder(self.b_download_source, self.b_create_bag)
        main_menu.setTabOrder(self.b_create_bag, self.b_validate_bag)
        main_menu.setTabOrder(self.b_validate_bag, self.b_upload_bag)
        main_menu.setTabOrder(self.b_upload_bag, self.b_configure)
        main_menu.setTabOrder(self.b_configure, self.b_quit)

    def retranslateUi(self, main_menu):
        main_menu.setWindowTitle(_translate("main_menu", "Dialog", None))
        self.b_download_source.setText(_translate("main_menu", "Download Source", None))
        self.b_create_bag.setText(_translate("main_menu", "Bag erstellen", None))
        self.b_validate_bag.setText(_translate("main_menu", "Bag validieren", None))
        self.b_upload_bag.setText(_translate("main_menu", "Upload Bag", None))
        self.b_configure.setText(_translate("main_menu", "DLAb konfigurieren", None))
        self.b_quit.setText(_translate("main_menu", "Beenden", None))
        self.label.setText(_translate("main_menu", "DLAb - v 0.1", None))

