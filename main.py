import logging
logging.basicConfig(filename='logs', format='%(levelname)s:%(asctime)s %(message)s', level=logging.DEBUG)

from optparse import OptionParser

from epubsearch import EpubParser
from epubsearch import EpubIndexer
from epubsearch import WordMorphoGenerator


class EpubWorker(object):
    def __init__(self, book_address, lang='ru'):
        epub = EpubParser(book_address)
        self.index = EpubIndexer('whoosh')
        logging.info('Indexing')
        self.index.load(epub)

    def search_word(self, search_word):
        logging.info('Search word {}'.format(search_word))
        return self.index.search(search_word)

    def search_lexemes(self, search_word):
        logging.info('Generate words for search')
        search_words = WordMorphoGenerator(search_word).generate()
        logging.info('Search word {} and lexemes'.format(search_word, search_words))
        results_dirty = []
        results_formatted = []
        for word in search_words:
            results_dirty.append(self.index.search(word))
        for result in results_dirty:
            result = result.get('results')
            if result:
                for item in result:
                    results_formatted.append(item['baseCfi'])

        return {'word': search_word,
                'lexemes': search_words,
                'results': results_formatted}


def get_parameters():
    """
        Parse the user input
    """
    parser = OptionParser()
    parser.add_option('-b', '--book-input', dest='book_input')
    parser.add_option('-s', '--search', dest='search')
    parser.add_option('--lang', dest='language')
    parser.add_option('--lexemes', dest='lexemes')
    (options, args) = parser.parse_args()

    if not options.book_input:
        options.book_input = "Sensei4/"
    else:
        return {'book_input': options.book_input,
                'search': options.search, 'language': options.language, 'lexemes': options.lexemes}


def main():
    logging.info('*'*20)
    # get user defined parameters
    # userParams = get_parameters()

    # search = userParams['search']
    # book_input = userParams['book_input']
    # language = userParams['language']
    # lexemes = userParams['lexemes']
    book_input = "Sensei4/"
    search = "аллат"
    lexemes = ""

    worker = EpubWorker(book_input)
    if lexemes:
        return worker.search_lexemes(search)
    return worker.search_word(search)

if __name__ == '__main__':
    # logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s', level=logging.DEBUG)
    print(main())

