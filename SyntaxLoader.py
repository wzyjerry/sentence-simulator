# -*- coding: utf-8 -*-
import json
import codecs
import logging

class SyntaxLoader(object):
    def __init__(self, filename, logger=logging):
        self.__filename = filename
        self.__logger = logger
        self.__index = 0
        self.__data = None
        self.__stat = {
            'n_intent'
        }

    def __load(self):
        with codecs.open(self.__filename, 'r', 'utf-8') as fin:
            self.__data = json.load(fin)

    def __check(self, node):
        if node['type'] == 'holder':
            return
        node['id'] = self.__index
        self.__index += 1
        if 'children' in node:
            for child in node['children']:
                self.__check(child)

    def check(self):
        self.__load()
        self.__check(self.__data)
        self.__logger.warn('123')

if __name__ == '__main__':
    sl = SyntaxLoader('data/syntaxTree.json')
    sl.check()
