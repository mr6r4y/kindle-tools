#!/usr/bin/python
#-*- encoding: utf-8 -*-


__all__ = ['COLLECTIONS_FILENAME',
           'BookCollector']


import sys
import os
import json
import hashlib


COLLECTIONS_FILENAME = 'collections.json'


class BookCollector(object):
    _formats = ['pdf', 'mobi']
    _locales = {'us': 'en-US'}
    _kindle_root = "/mnt/us"
    _kindle_document_directory = "documents"
    
    def __init__(self, base_path, locale='us'):
        if(not os.path.isdir(base_path)):
            raise ValueError(("Base path does not exists or "
                              "is not a directory: %s") % base_path)
        if(locale not in self._locales):
            raise ValueError(("Locale is not supported: %s" % locale))
        
        self._locale = locale
        self._base_path = os.path.abspath(base_path)
        self._raw_collections = None
    
    @classmethod
    def _is_book(cls, book_path):
        try:
            if(os.path.splitext(book_path)[1].lstrip('.').lower() in cls._formats):
                return True
        except Exception:
            pass
        return False

    @classmethod
    def _get_books(cls, path, base_path):
        books = []
        for directory, dirnames, filenames in os.walk(path):
            relative_path = os.path.relpath(directory, base_path)
            for book in filenames:
                if(cls._is_book(book)):
                    books.append(os.path.join(relative_path, book))
        
        return books
    
    def _crawl_base_path(self, base_path):
        self._raw_collections = {}
        for item in os.listdir(base_path):
            item_path = os.path.join(base_path, item)
            if(os.path.isdir(item_path)):
                books = self._get_books(item_path, base_path)
                if(books):
                    self._raw_collections[item] = books
    
    def _path_hash(self, path):
        book_path_list = (self._kindle_root, self._kindle_document_directory)
        book_path_list = book_path_list + os.path.split(path)
        book_path = '/'.join(book_path_list)
        
        return '*' + hashlib.sha1(unicode(book_path).encode('utf-8')).hexdigest()
    
    @property
    def raw_collections(self):
        self._crawl_base_path(self._base_path)
        return self._raw_collections
    
    @property
    def collections(self):
        raw_collections = self.raw_collections
        collection_dict = {}
        for cl in raw_collections:
            key = '@'.join((cl, self._locales[self._locale]))
            collection_dict[key] = {}
            collection_dict[key]['lastAccess'] = 0
            collection_dict[key]['items'] = [self._path_hash(bk) for bk in raw_collections[cl]]
        
        return collection_dict
    
    @property
    def collections_json(self):
        collections = self.collections
        return json.dumps(collections, sort_keys=True, separators=(',',':'))

