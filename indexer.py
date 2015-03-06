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
import logging
# logging.basicConfig(filename='logs', format='%(levelname)s:%(asctime)s %(message)s', level=logging.INFO)

import pylibmc
mc = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True, "ketama": True})

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
    parser.add_option('-e', '--search-engine', dest='search_engine')
    (options, args) = parser.parse_args()

    # code block to check for empty path, needed? path that includes proper filename, then valid file check
    if not options.search_engine:
        options.search_engine = 'whoosh'

    if not options.input:
        options.input = "Sensei4/"
    else:
        return {'input': options.input, 'file': options.input[-3:].lower(), 'folder': options.input,
                'search': options.search, 'search_engine': options.search_engine}


def main():
    logging.info('*'*20)
    # get user defined parameters
    userParams = get_parameters()

    search = userParams['search']
    folder = userParams['folder']
    search_engine = userParams['search_engine']

    epub = EpubParser(folder)

    logging.info('Indexing is started')
    # when try to load index to mc i got next error: TypeError: cannot serialize '_io.BufferedWriter' object
    # index = mc.get(folder)
    # if not index:
    #     index = EpubIndexer('whoosh')
    #     index.load(epub)
    #     mc.set(folder, index)
    #     logging.info('Epub book index was saved to memcached')
    index = EpubIndexer(search_engine)
    index.load(epub)
    logging.info('Indexing is finish')

    logging.info('Generate words for search')
    word_for_search = WordMorphoGenerator(search).generate()
    logging.info('Generating is done')

    result = []
    logging.info('Making result')
    for word in word_for_search:
        logging.debug('{}'.format(word))
        result.append((word, index.search(word)))

    logging.info('Result {}'.format(result))
    return result


if __name__ == '__main__':
    logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s', level=logging.DEBUG)
    main()
