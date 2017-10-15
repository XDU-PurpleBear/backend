# -*- coding:utf-8 -*-
'''
Created on 2017年10月12日

@author: lenovo
'''

def modifyUserInfo(user,UUID):
    return {'test':'test'}

def queryBookKind(clc):
    return  [{
                "ISBN": "a",
                "CLC":"b",
                "name":"c",
                "auth":[
                    "d",
                    "e"
                ],
                "publisher": "f",
                "edition":"g",
                "imgs": "h",
            },{
                        "ISBN": "a",
                        "CLC":"b",
                        "name":"c",
                        "auth":[
                            "d",
                            "e"
                        ],
                        "publisher": "f",
                        "edition":"g",
                        "imgs": "h",
                    }]

def queryBook(isbn):
    return {'test':'test'}

def addUser(tel,username,password):
    one = {'Status':'Success'}
    two = {'Status':'Failure','errorInfo':'xxx'}
    return one

def getPWD(str):
    one = {'password':'xxl'}
    no = {'password':''}
    two = {'password':'1'}
    return ''


def getUserUUID(str):
    return {'UUID':'1234556789'}

def getUserInfo(str):
    reader = {
        'user-name':'',
        'first-name':'',
        'last-name':'',
        'birthday':'',
        'date-of-registering':'',
        'balance':'',
        'sex':'',
        'tel-phone-number':'',
        'right':'1'
        }
    librarian = {
        'user-name':'',
        'first-name':'',
        'last-name':'',
        'birthday':'',
        'date-of-registering':'',
        'balance':'',
        'sex':'',
        'tel-phone-number':'',
        'right':'2'
        }
    return reader
