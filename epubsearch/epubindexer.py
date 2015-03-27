import importlib
from lxml import etree
import re
import logging


class EpubIndexer(object):
    epub = False
    engine = False

    def __init__(self, engineName=False, databaseName='indexdir'):
        if engineName:
            mod = importlib.import_module("epubsearch.search_engines.%sengine" % engineName)
            # import whooshengine as engine
            self.engine = getattr(mod,'%sEngine' % engineName.capitalize())(databaseName)
            logging.info(self.engine)

    def load(self, epub):
        self.epub = epub
        # try:
        #     self.engine.open()
        # except Exception as e:
        #     print(e)
        self.engine.create()

        for spineItem in epub.spine:

            path = epub.base + "/" + spineItem['href']

            self.engine.add(path=path, href=spineItem['href'], title=spineItem['title'], cfiBase=spineItem['cfiBase'], spinePos=spineItem['spinePos'])

        self.engine.finished()

    def search(self, q, limit=None):
        rawresults = self.engine.query(q, limit)
        # print len(rawresults)
        r = {}
        r["results"] = []
        q = q.lower()

        for hit in rawresults:
            baseitem = {}
            baseitem['title'] = hit["title"].decode(encoding="UTF-8")
            baseitem['href'] = hit["href"].decode(encoding="UTF-8")
            baseitem['path'] = hit["path"].decode(encoding="UTF-8")

            # find base of cfi
            cfiBase = hit['cfiBase'].decode(encoding="UTF-8") + "!"

            with open(hit["path"]) as fileobj:
                tree = etree.parse(fileobj)
                parsedString = etree.tostring(tree.getroot())
                # case-insensitive xpath search
                xpath = './/*[contains(translate(text(), "ABCDEFGHIJKLMNOPQRSTUVWXYZ", "abcdefghijklmnopqrstuvwxyz") , "'+ q + '")]'
                #xpath = './/*[contains(text(),"'+ q +'")]'

                matchedList = tree.xpath(xpath)
                # print len(matchedList)
                for word in matchedList:
                    # copy the base
                    item = baseitem.copy()

                    # print word
                    # print word.getparent()
                    item['baseCfi'] = cfiBase
                    item['cfi'] = getCFI(cfiBase, word)
                    #print cfi
                    r["results"].append(item)

        ## Sort results by chapter
        r['results'] = sorted(r['results'], key=lambda x: getCFIChapter(x['baseCfi']))
        return r


def getCFI(cfiBase, word):

    cfi_list = []
    parent = word.getparent()
    child = word
    while parent is not None:
        i = parent.index(child)
        if 'id' in child.attrib:
            cfi_list.insert(0,str((i+1)*2)+'[' + child.attrib['id'] + ']')
        else:
            cfi_list.insert(0,str((i+1)*2))
        child = parent
        parent = child.getparent()

    cfi = cfiBase + '/' + '/'.join(cfi_list)
    return cfi

def getCFIChapter(cfiBase):
    cfiBase = re.sub(r'\[.*\]','',cfiBase)
    chapter_location = cfiBase[cfiBase.rfind('/')+1:cfiBase.find('!')]
    return int(chapter_location)
