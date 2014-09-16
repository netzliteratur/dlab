#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This is a SRU client, module and stand-alone.
If used stand-alone, the path to the
config file has to be passed with
parameter -c. The search term has to be
passed with parameter -s.
"""
__date__ = '20140417'
__version__ = '0.1'
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


def read_config(path):
    """
    read SRU configuration
    """
    config = ConfigParser.RawConfigParser()
    config.read(path)

    sru_base_url = config.get("SETTINGS", "SRU_Base_URL")
    sru_database = config.get("SETTINGS", "SRU_Database")
    record_schema = config.get("SETTINGS", "Record_Schema")
    q_attrib = config.get("SETTINGS", "Query_Attribute")

    return sru_base_url, sru_database, record_schema, q_attrib


def search_retrieve(base_url, searchterm, db, schema, q_attrib):
    """
    fetch information as picaxml
    """
    url = base_url + db + '?' + \
        "version=1.1&operation=searchRetrieve&query=pica." + \
        q_attrib + \
        "%3D" + \
        searchterm + \
        "&maximumRecords=10&recordSchema=" + \
        schema
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
        print("USAGE: python sru.py -c CONFIGFILE -s SEARCHTERM")
        sys.exit(0)
    try:
        c = sys.argv.index('-c')
        base_url, database, schema, q_attrib = read_config(sys.argv[c + 1])
    except IOError, err:
        print(str(err))
        sys.exit(1)

    try:
        s = sys.argv.index('-s')
        searchterm = sys.argv[s + 1]
        response = search_retrieve(base_url, searchterm, database, schema, q_attrib)
        
        # aggregate project relevant informations
        meta_dict = extract_information(response)
        for element in meta_dict['lang']:
            print(element)

    except RuntimeError, err:
        print(str(err))
        sys.exit(1)

if __name__ == '__main__':
    main()
