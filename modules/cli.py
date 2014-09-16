#-*- coding:utf-8 -*-
import sys
import bag
import payload_inspect
import metadata


def get_add_infos(sru_dict):
    """
    information asked for interactively
    some defaults are given
    :return:
    """

    addinfos_dict = {}
    author_counter = 0

    # mets
    addinfos_dict['title_lang'] = "ger"
    addinfos_dict['title_lang'] = raw_input("Sprache des Titels, z.B. ger: ")

    addinfos_dict['subtitle_lang'] = "ger"
    addinfos_dict['subtitle_lang'] = raw_input("Sprache des Untertitels, z.B. ger: ")

    addinfos_dict['location_live'] = raw_input("Angabe URI Liveweb, falls vorhanden: ")
    addinfos_dict['location_archived'] = raw_input("Angabe URI Archiv, falls vorhanden: ")

    addinfos_dict['access_condition'] = raw_input("Benutzungshinweis: ")
    if addinfos_dict['access_condition'].lower() == "moving wall":
        addinfos_dict['moving_wall_date'] = raw_input("Datum der Freischaltung [JJJJ-MM-DD]: ")

    print("Rechteinhaber angeben. Eingabe mehrerer durch Enter trennen. [Nachname, Vorname]: ")
    addinfos_dict['rights_holder'] = []
    in_ = "_"
    while in_ != "":
        in_ = raw_input()
        in_ = in_.decode(encoding="utf-8")
        if in_ != "":
            addinfos_dict['rights_holder'].append(in_)

    addinfos_dict['abstract_author'] = raw_input("Beschreibung durch den Autor: \n")
    addinfos_dict['abstract_author'] = addinfos_dict['abstract_author'].decode(encoding="utf-8")
    addinfos_dict['abstract_reflective'] = raw_input("Weitere Beschreibung: \n")
    addinfos_dict['abstract_reflective'] = addinfos_dict['abstract_reflective'].decode(encoding="utf-8")

    for author in sru_dict['author_info']:
        given_ = author['given']
        family_ = author['family']
        print("GND URI von " + family_ + ", " + given_ + " eingeben: ")
        addinfos_dict['gnd_uri_' + str(author_counter)] = raw_input()
        author_counter += 1

    return addinfos_dict


def get_config():
    """

    :return:
    """
    print("* * * Konfiguration * * *\n")
    print("info: Die folgenden Einstellungen konfigurieren bag-info.txt\n")
    contact_name = raw_input("Kontakt Name: ")
    contact_mail = raw_input("Kontakt Mail: ")
    orga_address = raw_input("Kontakt postalische Adresse: ")
    source_orga = raw_input("Name der sendenden Organisation: ")
    print("\ninfo: Die folgenden Einstellungen konfigurieren den ftp-Zugang\n")
    server_ = raw_input("Server: ")
    user_ = raw_input("Benutzername: ")
    port_ = raw_input("Port: ")
    passwd_ = raw_input("Passwort: ")
    dir_ = raw_input("Name des Upload-Ordners: ")

    fd = open("config/bag.cfg", "w")
    fd.write("[SETTINGS]\n")
    fd.write("Contact-Name : " + contact_name + "\n")
    fd.write("Contact-Email : " + contact_mail + "\n")
    fd.write("Organization-Address : " + orga_address + "\n")
    fd.write("Source-Organization : " + source_orga + "\n")
    fd.write("[SFTP]\n")
    fd.write("Server : " + server_ + "\n")
    fd.write("Port : " + port_ + "\n")
    fd.write("User : " + user_ + "\n")
    fd.write("Password : " + passwd_ + "\n")
    fd.write("Directory : " + dir_ + "\n")

    fd.close()


def menu():
    """
    cli menu
    :return: char
    """
    print("\n+ + + DLA Bagger - v0.1 + + +\n\n"
          "+++ [E]rstelle Bag\n"
          "+++ [V]alidiere Bag\n"
          "+++ [K]onfiguriere Bag\n"
          "+++ [B]eende DLAb\n")

    choice = raw_input()
    choice = choice.lower()

    if choice == "e":
        # todo entferne debug values
        source_dir = raw_input("Pfad zur Quelle angeben: ")
        bag_dir = bag.copy_source(source_dir)
        bag.create_bag(bag_dir)
        ppn = raw_input("Eingabe PPN: ")
        #ppn = "396892051"
        # todo end
        response = metadata.fetch_infos_sru(ppn)
        sru_dict = metadata.parse_sru_infos(response)
        add_dict = get_add_infos(sru_dict)
        file_list, rep_list, rep_bool = payload_inspect.id_file_rep(bag_dir)
        metadata.write_metadata_file(bag_dir, sru_dict, add_dict, file_list, rep_list, rep_bool)
        bag.rename_bag(bag_dir, "BSZ" + ppn + ".bag")
        bag.create_tar_gz("BSZ" + ppn + ".bag")
        print("Bag erfolgreich erstellt.")
        _ = raw_input("Mit Enter beenden.\n")

    elif choice == "v":
        to_validate = raw_input("Pfad zur Bag angeben: ")
        try:
            bag.validate_bag(to_validate)
        except IOError, err:
            print("Es ist ein Fehler aufgetreten: " + str(err))

    elif choice == "k":
        try:
            get_config()
            print("\n info: Konfiguration erfolgreich geschrieben.")
        except RuntimeError, err:
            print("\n info: Es ist ein Fehler aufgetreten. Meldung: \n")
            print(str(err))
            sys.exit(1)

    elif choice == "b":
        sys.exit(0)
    else:
        print("Ungültige Eingabe")
        menu()
