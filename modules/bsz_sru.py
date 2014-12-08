#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
This is a SRU client, module and stand-alone.
If used stand-alone, the path to the
config file has to be passed with
parameter -c. The search term has to be
passed with parameter -s.
"""
__version__ = '0.4'
__date__ = '08/12/2014'
__status__ = 'Testing'
__author__ = 'steffen fritz'
__contact__ = 'fritz@dla-marbach.de'
__license__ = 'MIT'
__copyright__ = 'Copyright (c) 2014 Deutsches Literaturarchiv Marbach'
__maintainer__ = 'steffen fritz'

import urllib
import ConfigParser


def read_config(path):
    """
    read SRU configuration
    :return string user_name, user_passwd:
    """
    config = ConfigParser.RawConfigParser()
    config.read(path)

    user_name = config.get("SETTINGS", "USER_NAME")
    user_passwd = config.get("SETTINGS", "USER_PASSWD")

    return user_name, user_passwd 


def search_retrieve(searchterm, user_name, user_passwd):
    """
    fetch information as picaxml
    :return string response:
    """
    url = "http://castor.bsz-bw.de:8000/sru/DB=1.1&username=" + user_name + \
          "/password=" + user_passwd + "/?query=pica.ppn+%3D+%22" + searchterm + \
          "%22&version=1.1&operation=searchRetrieve&recordSchema=ppxml" + \
          "&maximumRecords=1&startRecords=1&startRecord=1&recordPacking=xml"
    urlh = urllib.urlopen(url)
    response = urlh.read()
    urlh.close()
    
    return response
