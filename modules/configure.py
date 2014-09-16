# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'configure.ui'
#
# Created: Thu Sep 11 10:22:35 2014
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

class Ui_baginfo_conf(object):
    def setupUi(self, baginfo_conf):
        baginfo_conf.setObjectName(_fromUtf8("baginfo_conf"))
        baginfo_conf.resize(596, 580)
        self.verticalLayoutWidget_2 = QtGui.QWidget(baginfo_conf)
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
        self.formLayoutWidget = QtGui.QWidget(baginfo_conf)
        self.formLayoutWidget.setGeometry(QtCore.QRect(30, 60, 381, 102))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.label = QtGui.QLabel(self.formLayoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.label)
        self.e_con_name = QtGui.QLineEdit(self.formLayoutWidget)
        self.e_con_name.setObjectName(_fromUtf8("e_con_name"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.e_con_name)
        self.label_2 = QtGui.QLabel(self.formLayoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_2)
        self.e_source = QtGui.QLineEdit(self.formLayoutWidget)
        self.e_source.setObjectName(_fromUtf8("e_source"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.e_source)
        self.label_3 = QtGui.QLabel(self.formLayoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_3)
        self.label_4 = QtGui.QLabel(self.formLayoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_4)
        self.e_source_orga = QtGui.QLineEdit(self.formLayoutWidget)
        self.e_source_orga.setObjectName(_fromUtf8("e_source_orga"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.e_source_orga)
        self.e_orga_address = QtGui.QLineEdit(self.formLayoutWidget)
        self.e_orga_address.setObjectName(_fromUtf8("e_orga_address"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.e_orga_address)
        self.formLayoutWidget_2 = QtGui.QWidget(baginfo_conf)
        self.formLayoutWidget_2.setGeometry(QtCore.QRect(30, 230, 381, 102))
        self.formLayoutWidget_2.setObjectName(_fromUtf8("formLayoutWidget_2"))
        self.server_conf = QtGui.QFormLayout(self.formLayoutWidget_2)
        self.server_conf.setMargin(0)
        self.server_conf.setObjectName(_fromUtf8("server_conf"))
        self.label_5 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.server_conf.setWidget(0, QtGui.QFormLayout.LabelRole, self.label_5)
        self.e_server = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.e_server.setObjectName(_fromUtf8("e_server"))
        self.server_conf.setWidget(0, QtGui.QFormLayout.FieldRole, self.e_server)
        self.label_6 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.server_conf.setWidget(1, QtGui.QFormLayout.LabelRole, self.label_6)
        self.e_port = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.e_port.setObjectName(_fromUtf8("e_port"))
        self.server_conf.setWidget(1, QtGui.QFormLayout.FieldRole, self.e_port)
        self.label_7 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.server_conf.setWidget(2, QtGui.QFormLayout.LabelRole, self.label_7)
        self.label_8 = QtGui.QLabel(self.formLayoutWidget_2)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.server_conf.setWidget(3, QtGui.QFormLayout.LabelRole, self.label_8)
        self.e_user = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.e_user.setObjectName(_fromUtf8("e_user"))
        self.server_conf.setWidget(2, QtGui.QFormLayout.FieldRole, self.e_user)
        self.e_passwd = QtGui.QLineEdit(self.formLayoutWidget_2)
        self.e_passwd.setObjectName(_fromUtf8("e_passwd"))
        self.server_conf.setWidget(3, QtGui.QFormLayout.FieldRole, self.e_passwd)
        self.label_9 = QtGui.QLabel(baginfo_conf)
        self.label_9.setGeometry(QtCore.QRect(50, 30, 171, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(baginfo_conf)
        self.label_10.setGeometry(QtCore.QRect(50, 200, 171, 16))
        self.label_10.setObjectName(_fromUtf8("label_10"))

        self.retranslateUi(baginfo_conf)
        QtCore.QMetaObject.connectSlotsByName(baginfo_conf)
        baginfo_conf.setTabOrder(self.e_con_name, self.e_source)
        baginfo_conf.setTabOrder(self.e_source, self.e_source_orga)
        baginfo_conf.setTabOrder(self.e_source_orga, self.e_orga_address)
        baginfo_conf.setTabOrder(self.e_orga_address, self.e_server)
        baginfo_conf.setTabOrder(self.e_server, self.e_port)
        baginfo_conf.setTabOrder(self.e_port, self.e_user)
        baginfo_conf.setTabOrder(self.e_user, self.e_passwd)
        baginfo_conf.setTabOrder(self.e_passwd, self.b_continue)
        baginfo_conf.setTabOrder(self.b_continue, self.b_cancel)

    def retranslateUi(self, baginfo_conf):
        baginfo_conf.setWindowTitle(_translate("baginfo_conf", "Dialog", None))
        self.b_continue.setText(_translate("baginfo_conf", "Speichern", None))
        self.b_cancel.setText(_translate("baginfo_conf", "Abbrechen", None))
        self.label.setText(_translate("baginfo_conf", "Contact-Name", None))
        self.label_2.setText(_translate("baginfo_conf", "Contact-Mail", None))
        self.label_3.setText(_translate("baginfo_conf", "Source-Organization", None))
        self.label_4.setText(_translate("baginfo_conf", "Organization Address", None))
        self.label_5.setText(_translate("baginfo_conf", "Server", None))
        self.label_6.setText(_translate("baginfo_conf", "Port", None))
        self.label_7.setText(_translate("baginfo_conf", "Benutzer", None))
        self.label_8.setText(_translate("baginfo_conf", "Passwort", None))
        self.label_9.setText(_translate("baginfo_conf", "Konfiguration bag-info.txt", None))
        self.label_10.setText(_translate("baginfo_conf", "Konfiguration Server", None))

