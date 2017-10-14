#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
Book information module.
'''

__author__ = 'Fitzeng'

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

class BookInstance(object):
    def __init__(self, uuid=None, isbn=None, status=None, opt_id=None):
        self.uuid = uuid
        self.isbn = isbn
        self.status = status
        self.opt_id = opt_id