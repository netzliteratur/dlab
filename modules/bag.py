#-*- coding:utf-8 -*-
import os
import tarfile
import shutil
import ConfigParser
import modules.bagit


def copy_source(source_dir):
    """
    copy source directory
    to temp directory
    return code
    """
    try:
        bag_name = os.path.basename(os.path.normpath(source_dir))
        if os.path.exists("temp_" + bag_name):
            shutil.rmtree("temp_" + bag_name)
        shutil.copytree(source_dir, "temp_" + bag_name)

        return "temp_" + bag_name

    except OSError, err:
        print("FEHLER: " + str(err))


def create_bag(bag_dir):
    """
    :return:
    """
    config = ConfigParser.RawConfigParser()
    config.read("config/bag.cfg")
    try:
        modules.bagit.make_bag(bag_dir, {'Contact-Name': config.get("SETTINGS", "Contact-Name"),
                                         'Contact-Mail': config.get("SETTINGS", "Contact-Email"),
                                         'Source-Organizaion': config.get("SETTINGS", "Source-Organization"),
                                         'Organization-Address': config.get("SETTINGS", "Organization-Address")})
        modules.bagit.Bag(bag_dir)
    except RuntimeError, err:
        print(str(err))


def rename_bag(src, dst):
    """
    :return:
    """
    os.rename(src, dst)


def create_tar_gz(bag_):
    """
    :return:
    """
    targz = tarfile.open(bag_ + ".tar.gz", "w:gz")
    targz.add(bag_)
    targz.close()


def validate_bag(path_to_bag):
    """

    :return:
    """
    bag = modules.bagit.Bag(path_to_bag)
    try:
        bag.validate()

        return 0

    except modules.bagit.BagValidationError, err:
        print(str(err))

        return 1