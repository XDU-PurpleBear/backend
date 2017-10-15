# -*- coding:utf-8 -*-
'''
Created on 2017年10月15日

@author: lenovo
'''
class Book(object):
        def __init__(self, isbn=None, clc=None, name=None, auth=None,
                     publisher=None, edition=None, publish_date=None, imgs=None):
            self.isbn = isbn
            self.clc = clc
            self.name = name
            self.auth = auth
            self.publisher = publisher
            self.edition = edition
            self.publish_date = publish_date
            self.imgs = imgs