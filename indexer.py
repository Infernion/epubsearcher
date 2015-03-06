#!/usr/bin/python
# -*- coding: utf-8 -*-

"""WARNING:  Script is in beta and needs to be tested thoroughly.

The script generates a rudimentary appcache file based upon the content.opf file located in either: 
an uncompressed epub directory or a compressed epub file and places it in the current directory

Usage: acm_gen.py --input='/path/to/content.opf' which links to the uncompressed epub directory that includes the content.opf
OR     --input='/path/to/book.epub' which links to the compressed epub file
"""
 
__author__ = 'Futurepress'
__email__ = 'luis@berkeley.edu'

import os
import xml.etree.ElementTree as ET
import zipfile
import datetime
#import epub
from optparse import OptionParser

from epubsearch import EpubParser
from epubsearch import EpubIndexer
from epubsearch import WordMorphoGenerator

def get_parameters():
    """
        Parse the user input
    """
    parser = OptionParser()
    parser.add_option('-i', '--input', dest='input')
    parser.add_option('-s', '--search', dest='search')
    (options, args) = parser.parse_args()

    # code block to check for empty path, needed? path that includes proper filename, then valid file check
    if not options.input:
        options.input = "moby-dick"

    else:
        return {'input': options.input,'file': options.input[-3:].lower(), 'folder': options.input,
                'search': options.search}


def main():
    # get user defined parameters
    userParams = get_parameters()

    search = userParams['search']
    # search = u'аллат'

    epub = EpubParser(userParams['folder'])

    index = EpubIndexer('whoosh')
    index.load(epub)

    word_for_search = WordMorphoGenerator(search).generate()

    result = []
    for word in word_for_search:
        result.append((word, index.search(word)))

    print('Done!', result)

if __name__ == '__main__':
    main()
