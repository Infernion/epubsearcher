Что умеет
==========
Ищет заданое слово в книге формата  epub. В качестве результата возвращет JSON cледующего формата:
```javascript
{'word': 'POB',
 'lexemes': ['POBOB', 'POBAM']
'results': [{'baseCfi': '/6/24[id15]!',
'cfi': '/6/24[id15]!/4/62',
'href': 'index_split_011.html',
'path': 'Sensei4///index_split_011.html',
'title': ''},
{'baseCfi': '/6/24[id15]!',
'cfi': '/6/24[id15]!/4/66/2',
'href': 'index_split_011.html',
'path': 'Sensei4///index_split_011.html',
'title': ''}]}
```


Архитектура
===========
![Архитектура](/Infernion/epubsearcher/raw/master/docs/epubsearcher_architecture.png)

Как утсановить
==============
Должен быть установлен python3.4, над другими версия не тестировал, но с 
версиями 3.Х должно работать без нареканий. На 2.Х будут проблемы с кодировкой.

Для получения исходников
    
    git clone https://bitbucket.org/Infernion/epubsearcher/

Для установки дев версии

    pip install https://bitbucket.org/Infernion/epubsearcher/get/dev.tar.bz2 

Для установки стабильной версии

    pip install epubsearcher

![Способы использования](/Infernion/epubsearcher/raw/master/docs/inputData.png)

Для запуска с терминала
=======================
Перейдите в склонированую директорию, полный путь epubsearcher_module/

Установить зависимости с помощью команды 
    
    pip install -r requirements.txt

Так можно запустить поиск одного слова
    
    python main.py --search=аллат --book-address="./test_data/Sensei4.epub" 
--lang=ru

А так поиск слова со всеми его лексемами
    
    python main.py --search=аллат --book-address="./test_data/Sensei4.epub" 
--lang=ru --lexemes=yes

Использование как библиотеки
============================
Импортируем библиотеку и загружаем книгу 
``` python
from epubseacher import EpubWorker
worker = EpubWorker(book_address, language)
```
В экземляре появится проиндексированая книга, по которой можно производить поиск.
Поиск одного слова
```python
print(worker.search_word(search))
```
Поиск с лексемами 
``` python
print(worker.search_lexemes(search))
```

Если поиск производится по заархиварованой книге, то что бы удалить временные файли по завершению закрыть поток ``worker.close()`` или использовать оператор ``with`` для автоматического закрытия потока.
```python
with EpubWorker(book_address, language) as worker:
    worker.search_lexemes(search)
```