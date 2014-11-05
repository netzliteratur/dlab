#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This is a SRU client, module and stand-alone.
If used stand-alone, the path to the
config file has to be passed with
parameter -c. The search term has to be
passed with parameter -s.
"""
__date__ = '20141029'
__version__ = '0.2'
__status__ = 'Developing'
__author__ = 'steffen fritz'
__contact__ = 'fritz@dla-marbach.de'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2014 Deutsches Literaturarchiv Marbach'
__maintainer__ = 'steffen fritz'

import sys
import urllib
import xml.etree.ElementTree as ET
import ConfigParser
#from metadata import parse_bsz_sru_infos as parse_infos


def read_config(path):
    """
    read SRU configuration
    """
    config = ConfigParser.RawConfigParser()
    config.read(path)

    user_name = config.get("SETTINGS", "USER_NAME")
    user_passwd = config.get("SETTINGS", "USER_PASSWD")

    return user_name, user_passwd 


def search_retrieve(searchterm, user_name, user_passwd):
    """
    fetch information as picaxml
    """
    url = "http://castor.bsz-bw.de:8000/sru/DB=1.1&username=" + user_name + \
          "/password=" + user_passwd + "/?query=pica.ppn+%3D+%22" + searchterm + \
          "%22&version=1.1&operation=searchRetrieve&recordSchema=ppxml" + \
          "&maximumRecords=1&startRecords=1&startRecord=1&recordPacking=xml"
    urlh = urllib.urlopen(url)
    response = urlh.read()
    urlh.close()
    
    return response


def main():
    """
    if not used as module
    execute main function
    """
    if len(sys.argv) < 3:
        print("USAGE: python bsz_sru.py -c CONFIGFILE -s PPN")
        sys.exit(0)
    try:
        c = sys.argv.index('-c')
        user_name, user_passwd = read_config(sys.argv[c + 1])
    except IOError, err:
        print(str(err))
        sys.exit(1)

    try:
        s = sys.argv.index('-s')
        searchterm = sys.argv[s + 1]
        response = search_retrieve(searchterm, user_name, user_passwd)
        return_dict = parse_infos(response)

        print(return_dict)

    except RuntimeError, err:
        print(str(err))
        sys.exit(1)

if __name__ == '__main__':
    main()
