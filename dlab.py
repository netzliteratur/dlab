#!/usr/bin/env python2
#-*- coding: utf-8 -*-
"""
dlab creates bags
"""
__file__ = "dlab.py"
__version = "1.0b"
__date__ = "12/08/2014"
__author__ = "steffen fritz"
__contact__ = "fritz@dla-marbach.de"
__license = "The MIT License (c) 2014 DLA Marbach"
__status__ = "Testing"
__maintainer__ = 'steffen fritz'

import sys
import ConfigParser
import modules.bagit


def main():
    """
    the main function
    returns exit code
    """

    # gui or cli
    if "-cli" in sys.argv:
        import modules.cli
        modules.cli.menu()
    else:
        import modules.gui

    return 0


if __name__ == '__main__':
    main()
