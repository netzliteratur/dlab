"""
gui module
"""
import os
import sys 
from PyQt4 import QtGui, QtCore 
from menu import Ui_main_menu as menu
from configure import Ui_baginfo_conf as conf
import create_bag_0
import create_bag_1
import bag
import payload_inspect
import metadata
import hashit
import subprocess
import structmd


class menu_(QtGui.QDialog, menu):
    def __init__(self): 
        QtGui.QDialog.__init__(self) 
        self.setupUi(self)

        # Slots einrichten 
        self.connect(self.b_download_source, QtCore.SIGNAL("clicked()"), self.onDownload)
        self.connect(self.b_create_bag, QtCore.SIGNAL("clicked()"), self.onCreateBag)
        self.connect(self.b_validate_bag, QtCore.SIGNAL("clicked()"), self.onValidate)
        self.connect(self.b_upload_bag, QtCore.SIGNAL("clicked()"), self.onUpload)
        self.connect(self.b_configure, QtCore.SIGNAL("clicked()"), self.onConfigure)
        self.connect(self.b_quit, QtCore.SIGNAL("clicked()"), self.onAbbrechen)

    def onDownload(self):
        QtGui.QMessageBox.question(self, 'Information', "Noch nicht implementiert.", QtGui.QMessageBox.Ok)

    def onCreateBag(self):
        self.create_bag_window = create_bag_()
        self.create_bag_window.show()

    def onValidate(self):
        path_, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 'Pfad zur Bag angeben')
        if ok:
            validated_ = bag.validate_bag(str(path_))
        if validated_ == 0:
           QtGui.QMessageBox.question(self, 'Information', "Bag ist valide.", QtGui.QMessageBox.Ok)

        else:
           QtGui.QMessageBox.question(self, 'Information', "Bag nicht valide!", QtGui.QMessageBox.Ok)

    def onUpload(self):
        bag_file_, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', "Bag inklusive Pfad angeben: ")
        try:
            subprocess.call([sys.executable, 'modules/ftpmod.py', bag_file_])
            subprocess.call([sys.executable, 'modules/ftpmod.py', bag_file_ + "-sha512.txt"])
            # todo Meldung wird immer angezeigt. Rueckgabe von subprocess auswerten
            QtGui.QMessageBox.question(self, 'Information', "Bag und Hashsummendatei erfolgreich hochgeladen.")
        except RuntimeError, err:
            print(str(err))

    def onConfigure(self):
        self.configure_window = configure_()
        self.configure_window.show()

    def onAbbrechen(self): 
        self.close()


class configure_(QtGui.QDialog, conf):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

        # Slots einrichten
        self.connect(self.b_continue, QtCore.SIGNAL("clicked()"), self.onSave)
        self.connect(self.b_cancel, QtCore.SIGNAL("clicked()"), self.onAbbrechen)

    def onSave(self):
        fd = open("config/bag.cfg", "w")
        fd.write("[SETTINGS]\n")
        fd.write("Contact-Name : " + str(self.e_con_name.text()) + "\n")
        fd.write("Contact-Email : " + str(self.e_source.text()) + "\n")
        fd.write("Organization-Address : " + str(self.e_orga_address.text()) + "\n")
        fd.write("Source-Organization : " + str(self.e_source_orga.text()) + "\n")
        fd.write("[SFTP]\n")
        fd.write("Server : " + str(self.e_server.text()) + "\n")
        fd.write("Port : " + str(self.e_port.text()) + "\n")
        fd.write("User : " + str(self.e_user.text()) + "\n")
        fd.write("Password : " + str(self.e_passwd.text()) + "\n")
        fd.write("Directory : \n")

        fd.close()
        self.close()
        QtGui.QMessageBox.question(self, 'Information', "Konfiguration erfolreich geschrieben", QtGui.QMessageBox.Ok)

    def onAbbrechen(self):
        self.close()


class create_bag_(QtGui.QDialog, create_bag_0.Ui_create_bag_0):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        # Slots einrichten
        self.connect(self.b_continue, QtCore.SIGNAL("clicked()"), self.onWeiter_1)
        self.connect(self.b_cancel, QtCore.SIGNAL("clicked()"), self.onAbbrechen)

    def onWeiter_1(self):
        # Daten auslesen
        addinfos_dict = {}
        author_counter = 0

        ppn = self.e_ppn.text()
        source_dir = self.e_source.text()
        addinfos_dict['title_lang'] = str(self.e_lang_title.text())
        addinfos_dict['subtitle_lang'] = str(self.e_lang_subtitle.text())
        addinfos_dict['location_live'] = str(self.e_uri_liveweb.text())
        addinfos_dict['location_archived'] = str(self.e_uri_archiv.text())
        addinfos_dict['access_condition'] = str(self.e_rights.text())
        addinfos_dict['moving_wall_date'] = str(self.e_mw_date.text())

        addinfos_dict['rights_holder'] = []
        rights_holder_ = self.e_rights_holder.text()
        rights_holder_split = rights_holder_.split(";")
        for element in rights_holder_split:
            #addinfos_dict['rights_holder'].append(str(element.toUtf8))
            addinfos_dict['rights_holder'].append(unicode(element))

        try:
            bag_dir = bag.copy_source(str(source_dir))
            bag.create_bag(bag_dir)
        except IOError, err:
            QtGui.QMessageBox.question(self, 'Information', "Es ist ein Fehler aufgetreten: " + str(err), QtGui.QMessageBox.Ok)

        response = metadata.fetch_infos_sru(str(ppn))
        sru_dict = metadata.parse_sru_infos(response)
        for author in sru_dict['author_info']:
            given_ = author['given']
            family_ = author['family']
            text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog',
                                                  'GND von ' + family_ +
                                                  ", " + given_ + " angeben")
            if ok:
                addinfos_dict['gnd_uri_' + str(author_counter)] = str(text)

            author_counter += 1

        self.close()
        self.create_bag_abstracts = get_abstracts()
        self.create_bag_abstracts.ppn = ppn
        self.create_bag_abstracts.addinfos_dict = addinfos_dict
        self.create_bag_abstracts.bag_dir = bag_dir
        self.create_bag_abstracts.sru_dict = sru_dict
        self.create_bag_abstracts.show()

    def onAbbrechen(self):
        self.close()


class get_abstracts(QtGui.QDialog, create_bag_1.Ui_create_bag_1):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)
        # Slots einrichten
        self.connect(self.b_continue, QtCore.SIGNAL("clicked()"), self.complete_it)
        self.connect(self.b_cancel, QtCore.SIGNAL("clicked()"), self.onAbbrechen)
        self.addinfos_dict = {}
        self.bag_dir = ''
        self.sru_dict = {}
        self.ppn = ''

    def complete_it(self):
        abstract_author = self.e_abstract_author.toPlainText()
        abstract_misc = self.e_abstract_misc.toPlainText()
        self.addinfos_dict['abstract_author'] = str(abstract_author.toUtf8())
        self.addinfos_dict['abstract_reflective'] = str(abstract_misc.toUtf8())
        self.close()
        file_list, rep_list, rep_bool = payload_inspect.id_file_rep(self.bag_dir)
        metadata.write_metadata_file(self.bag_dir, self.sru_dict, self.addinfos_dict, file_list, rep_list, rep_bool)
        bag.rename_bag(self.bag_dir, "BSZ" + self.ppn + ".bag")

        # structmd
        struct_md_cont_list = {}
        dir_ = "BSZ" + self.ppn + ".bag"
        for file_ in os.listdir(dir_ + "/data"):
            if str(file_).endswith('.zip'):
                zip_content_ = structmd.get_zip_content(dir_ + "/data/" + str(file_))
                struct_md_cont_list[str(file_)] = zip_content_
                print(struct_md_cont_list[str(file_)] )
                structmd.write_structmd(str(file_), dir_, struct_md_cont_list)
            if str(file_).endswith('.tar.gz'):
                targz_content_ = structmd.get_targz_content(dir_ + "/data/" + str(file_))
                struct_md_cont_list[str(file_)] = targz_content_
                structmd.write_structmd(str(file_), dir_, struct_md_cont_list)


        ppn_ = str(self.ppn)
        bag.create_tar_gz("BSZ" + ppn_ + ".bag")
        hashit.hashit("BSZ" + ppn_ + ".bag.tar.gz")

        QtGui.QMessageBox.question(self, 'Information', "Bag erfolgreich erstellt", QtGui.QMessageBox.Ok)

    def onAbbrechen(self):
        self.close()

app = QtGui.QApplication(sys.argv)
dialog = menu_()
dialog.show() 
sys.exit(app.exec_())
