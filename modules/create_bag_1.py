# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'create_bag_1.ui'
#
# Created: Wed Sep 10 13:40:02 2014
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

class Ui_create_bag_1(object):
    def setupUi(self, create_bag_1):
        create_bag_1.setObjectName(_fromUtf8("create_bag_1"))
        create_bag_1.resize(596, 580)
        self.verticalLayoutWidget_2 = QtGui.QWidget(create_bag_1)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(420, 420, 160, 80))
        self.verticalLayoutWidget_2.setObjectName(_fromUtf8("verticalLayoutWidget_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.b_continue = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.b_continue.setObjectName(_fromUtf8("b_continue"))
        self.verticalLayout_2.addWidget(self.b_continue)
        self.b_cancel = QtGui.QPushButton(self.verticalLayoutWidget_2)
        self.b_cancel.setObjectName(_fromUtf8("b_cancel"))
        self.verticalLayout_2.addWidget(self.b_cancel)
        self.e_abstract_author = QtGui.QTextEdit(create_bag_1)
        self.e_abstract_author.setGeometry(QtCore.QRect(30, 30, 351, 251))
        self.e_abstract_author.setObjectName(_fromUtf8("e_abstract_author"))
        self.e_abstract_misc = QtGui.QTextEdit(create_bag_1)
        self.e_abstract_misc.setGeometry(QtCore.QRect(30, 310, 351, 251))
        self.e_abstract_misc.setObjectName(_fromUtf8("e_abstract_misc"))
        self.label = QtGui.QLabel(create_bag_1)
        self.label.setGeometry(QtCore.QRect(30, 10, 181, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(create_bag_1)
        self.label_2.setGeometry(QtCore.QRect(30, 290, 201, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))

        self.retranslateUi(create_bag_1)
        QtCore.QMetaObject.connectSlotsByName(create_bag_1)

    def retranslateUi(self, create_bag_1):
        create_bag_1.setWindowTitle(_translate("create_bag_1", "Dialog", None))
        self.b_continue.setText(_translate("create_bag_1", "Weiter", None))
        self.b_cancel.setText(_translate("create_bag_1", "Abbrechen", None))
        self.label.setText(_translate("create_bag_1", "Beschreibung durch Autor", None))
        self.label_2.setText(_translate("create_bag_1", "Beschreibung durch Sonstige", None))

