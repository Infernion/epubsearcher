# -*- coding: utf-8 -*- 
from epubsearch import EpubParser
from epubsearch import EpubIndexer
# from epubsearch import EpubRetriever


epub = EpubParser("Sensei4")

index = EpubIndexer("whoosh")
index.load(epub)

results = index.search(u"аллат", 2)
if results:	
	with open('logs', 'w+') as f:
		f.write(str(results).decode("utf-8"))
    	print results

