#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
User information module.
'''

__author__ = 'Fitzeng'

class User(object):
    def __init__(self, user_name=None, first_name=None, last_name=None, birthday=None,
                 register_date=None, balance=None, sex=None, tel=None, right=None):
        self.user_name = user_name
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.register_date = register_date
        self.balance = balance
        self.sex = sex
        self.tel = tel
        self.right = right