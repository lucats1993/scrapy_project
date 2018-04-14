# -*- coding: utf-8 -*-

import json


class Category(object):
    __species = None
    __first_init = True

    def __new__(cls, *args, **kwargs):
        if cls.__species == None:
            cls.__species = object.__new__(cls)
        return cls.__species

    def __init__(self, key):
        if self.__first_init:
            with open('./module/category.json', 'r') as f:
                self.maps = json.load(f)
            self.__class__.__first_init = False
        self.key = key

    def realType(self):
        return self.maps.get(self.key)

    def __str__(self):
        return "-------str---%s" % self.key


if __name__ == '__main__':
    c=Category(u'趣站')
    print c.realType()
