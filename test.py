# -*- coding: utf-8 -*- 
from main import EpubWorker
import unittest
# import subprocess

class TestMainPy(unittest.TestCase):
    def setUp(self):
        pass


WRONG_REQUEST = {'results': []}
RIGHT_REQUEST = {'baseCfi': '/6/24[id15]!', 'title': '', 'path': './tmp/Sensei4//index_split_011.html',
                              'href': 'index_split_011.html', 'cfi': '/6/24[id15]!/4/62'}

class TestEpubWorker(unittest.TestCase):
    def setUp(self):
        test_dir = './test_data/'
        self.epub_dir = EpubWorker(test_dir + 'Sensei4/')
        self.epub_file = EpubWorker(test_dir + 'Sensei4.epub')

    def test_search_in_dir(self):
        self.assertDictEqual(self.epub_dir.search_word('хряк'), WRONG_REQUEST)
        self.assertDictEqual(self.epub_dir.search_word('аллат')['results'][0], RIGHT_REQUEST)

    def test_search_in_epub(self):
        self.assertDictEqual(self.epub_file.search_word('хряк'), WRONG_REQUEST)
        self.assertDictEqual(self.epub_file.search_word('аллат')['results'][0], RIGHT_REQUEST)


if __name__ == '__main__':
    unittest.main()

