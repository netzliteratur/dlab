#-*- coding:utf-8 -*-
import zipfile
import tarfile
from lxml import etree as ET


def get_zip_content(archive_):
    """
    :return:
    """
    cont_dict_ = {}
    if zipfile.is_zipfile(archive_):
        zip_ = zipfile.ZipFile(archive_)
        zip_content_ = zip_.namelist()
        for element_ in zip_content_:
            e_ = zip_.getinfo(element_)
            cont_dict_[element_] = {e_.file_size}

    return cont_dict_


def get_targz_content(archive_):
    """
    :return:
    """
    cont_dict_ = {}
    if tarfile.is_tarfile(archive_):
        tar_ = tarfile.open(archive_, "r:gz")
        for tarinfo in tar_:
           cont_dict_[tarinfo.name] = tarinfo.size

    return cont_dict_


def write_structmd(temp_dir, file_list_):
    """
    :return:
    """
    ET.register_namespace("dla", "https://wwik-prod.dla-marbach.de/line/Projektpapiere/DLA_schema.xsd")
    root = ET.Element("{https://wwik-prod.dla-marbach.de/line/Projektpapiere/DLA_schema.xsd}fileMap")

    #for archiv_entry_ in file_list_:
    #    dir_ = ET.SubElement(root, "{https://wwik-prod.dla-marbach.de/line/Projektpapiere/DLA_schema.xsd}dir")
    #    dir_.set("name", archiv_entry_.key)
    #    dir_file_name = ET.SubElement(dir_, "{https://wwik-prod.dla-marbach.de/line/Projektpapiere/DLA_schema.xsd}")

    tree = ET.ElementTree(root)
    tree.write(temp_dir + "/structmd.xml",  encoding="UTF-8", pretty_print=True, xml_declaration=True)