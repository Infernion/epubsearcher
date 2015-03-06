# -*- coding: utf-8 -*-
import importlib

class WordMorphoGenerator(object):
    engine = False

    def __init__(self, word, engineName='pymorphy2'):
        if engineName:
            self.word = word

            mod = importlib.import_module("epubsearch.morpho_engines.%sengine" % engineName)
            # import whooshengine as engine
            self.engine = getattr(mod,'%sEngine' % engineName.capitalize())
            print(self.engine)

    def generate(self):
        result = self.engine(self.word).process()
        return result