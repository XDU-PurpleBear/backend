# -*- coding:utf-8 -*-
'''
Created on 2017年10月15日

@author: lenovo
'''
class User(object):
    def __init__(self, user_name=None, first_name=None, last_name=None, birthday=None,register_date=None, balance=None, sex=None, tel=None, right=None,password=None):
        self.user_name = user_name
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.birthday = birthday
        self.register_date = register_date
        self.balance = balance
        self.sex = sex
        self.tel = tel
        self.right = right
    def turnDict(self):
        return self.__dict__