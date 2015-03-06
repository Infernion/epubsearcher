# -*- coding: utf-8 -*-
import importlib
import logging

class WordMorphoGenerator(object):
    engine = False

    def __init__(self, word, engineName='pymorphy2'):
        if engineName:
            self.word = word

            mod = importlib.import_module("epubsearch.morpho_engines.%sengine" % engineName)
            # import whooshengine as engine
            self.engine = getattr(mod,'%sEngine' % engineName.capitalize())
            logging.info(self.engine)

    def generate(self):
        '''
        run morpho procces for selected engine
        :return: list of words
        '''
        result = self.engine(self.word).process()
        return result