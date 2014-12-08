#-*- coding: utf-8 -*-
import os
import sys
import re
import uuid
import hashlib
import datetime
from subprocess import check_output


def identify_file_pronom(file_):
    """
    using fido
    :return string format_name, format_registry_key:
    """
    fido_check = check_output([sys.executable, "externals/fido/fido/fido.py", file_])
    first_result = re.search('OK,(.+?)\n', fido_check).group(1).split(",")

    format_name = first_result[2]
    format_registry_key = first_result[1]

    return format_name, format_registry_key


def id_file_rep(bag_dir):
    """
    identify object category
    create uuids for files and representations
    :return list file_list, rep_list, rep_bool:
    """
    payload_dir = bag_dir + "/data/"
    file_list = []
    rep_list = []
    rep_bool = {}
    rep_bool['crawl'] = False
    rep_bool['screencast'] = False
    rep_bool['screenshot'] = False
    rep_bool['source code'] = False
    screenshot_uuid = str(uuid.uuid4())

    for file_ in os.listdir(payload_dir):
        hash_ = hashlib.sha256(payload_dir + file_).hexdigest()
        uuid_ = "_" + str(uuid.uuid4())
        path_ = "data/" + str(file_)
        date_created_ = os.stat(payload_dir + file_).st_ctime
        date_created_ = datetime.datetime.fromtimestamp(date_created_).isoformat()
        file_size_ = os.stat(payload_dir + file_).st_size
        format_name_, format_registry_key_ = identify_file_pronom(payload_dir + file_)

        file_list.append({file_: {'uuid': uuid_,
                                  'hash': hash_,
                                  'format_name': format_name_,
                                  'format_registry_key': format_registry_key_,
                                  'file_size': file_size_,
                                  'path': path_,
                                  'date_created': date_created_
                                  }})

        rep_uuid_ = "_" + str(uuid.uuid4())

        if file_.endswith(".warc"):
            rep_list.append({file_: {'cat': 'crawl', 'uuid': rep_uuid_, 'has_part': uuid_}})
            file_list[-1][file_]['is_part'] = rep_uuid_
            rep_bool["crawl"] = True
        if file_.startswith("crawl_"):
            rep_list.append({file_: {'cat': 'crawl', 'uuid': rep_uuid_, 'has_part': uuid_}})
            file_list[-1][file_]['is_part'] = rep_uuid_
            rep_bool["crawl"] = True
        if file_.startswith("source_"):
            rep_list.append({file_: {'cat': 'source', 'uuid': rep_uuid_, 'has_part': uuid_}})
            file_list[-1][file_]['is_part'] = rep_uuid_
            rep_bool['source code'] = True
        if file_.startswith("screencast_"):
            rep_list.append({file_: {'cat': 'screencast', 'uuid': rep_uuid_, 'has_part': uuid_}})
            file_list[-1][file_]['is_part'] = rep_uuid_
            rep_bool["screencast"] = True
        if file_.startswith("screenshot_"):
            rep_list.append({file_: {'cat': 'screenshot', 'uuid': screenshot_uuid, 'has_part': uuid_}})
            file_list[-1][file_]['is_part'] = screenshot_uuid
            rep_bool["screenshot"] = True

    return file_list, rep_list, rep_bool
