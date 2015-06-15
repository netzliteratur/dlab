# -*- coding:utf-8 -*-
import os
import zipfile
import tarfile
from lxml import etree as ET


def get_zip_content(archive_):
    """
    :return dict cont_dict_:
    """
    cont_dict_ = {}
    if zipfile.is_zipfile(str(archive_)):
        zip_ = zipfile.ZipFile(str(archive_))
        zip_content_ = zip_.namelist()
        for element_ in zip_content_:
            e_ = zip_.getinfo(element_)
            #cont_dict_[element_] = {e_.file_size}
            cont_dict_[element_] = e_.file_size

    return cont_dict_


def get_targz_content(archive_):
    """
    :return: dict cont_dict
    """
    cont_dict_ = {}
    if tarfile.is_tarfile(str(archive_)):
        tar_ = tarfile.open(str(archive_), "r:gz")
        for tarinfo in tar_:
            cont_dict_[tarinfo.name] = tarinfo.size

    return cont_dict_


def write_structmd(source_file, temp_dir, file_list_):
    """
    :return:
    """
    ET.register_namespace("dla", "https://wwik-prod.dla-marbach.de/line/")
    root = ET.Element("{https://wwik-prod.dla-marbach.de/line/}fileMap")
    for archive_entry_ in file_list_:
        for element_ in file_list_[archive_entry_]:
            if os.path.isdir(element_):
                dir_ = ET.SubElement(root, "{https://wwik-prod.dla-marbach.de/line/}dir")
                dir_.set("name", element_)
            else:
                file_ = ET.SubElement(root, "{https://wwik-prod.dla-marbach.de/line/}file")
                u_element = unicode(element_, "utf-8", "ignore")
                file_.set("name", u_element)
                file_size = ET.SubElement(file_,
                                          "{https://wwik-prod.dla-marbach.de/line/}size")
                file_size.text = str(file_list_[archive_entry_][element_])

    tree = ET.ElementTree(root)
    tree.write(str(temp_dir) + "/" + source_file + "_structmd.xml",
               encoding="UTF-8", pretty_print=True, xml_declaration=True)
