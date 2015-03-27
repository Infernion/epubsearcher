Что умеет
==========
Ищет заданое слово в книге формата  epub


Архитектура
===========

![Архитектура](/docs/epubseacher_architecture.png)

Как использовать
==============
Должен быть установлен python3.4

1. Склонировать репозитарий
2. Установить зависимости
   ``pip install -r requirements.txt``

![Способы использования](/docs/inputData.png)

Для запуска с терминала
=======================
Так можно запустить поиск одного слова
``python main.py --search=аллат --book-address="./test_data/Sensei4.epub" --lang=ru``

А так поиск слова со всеми его лексемами
``python main.py --search=аллат --book-address="./test_data/Sensei4.epub" --lang=ru --lexemes=yes``

Использование как библиотеки
============================
Импортируем библиотеку и загружаем книгу 
``` python
from epubseacher import EpubWorker
worker = EpubWorker(book_address, language):
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