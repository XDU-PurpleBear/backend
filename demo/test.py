# -*- coding:utf-8 -*-
'''
Created on 2017年10月16日

@author: lenovo
'''
import func as X
import datetime

def testSignup():
    blockInfos = [{'tel':'13918102925','username':'last','password':'1111'}]
    for blockInfo in blockInfos:
        print 'block->',blockInfo
        fromX = X.signup(blockInfo)
        print fromX
        print '-------------------------------------------------'

def testLogin():
    blockInfos = [{'type':'tel','value':'13918102925','password':'1111'}]
    for blockInfo in blockInfos:
        print 'block->',blockInfo
        fromX = X.login(blockInfo)
        print fromX
        print '-------------------------------------------------'
    return fromX

def testLogout(uuid):
    logoutBlock = {'token':uuid}
    #X.login(loginBlock)
    #logoutBlock = [{'username':'Number1','token':''},{'username':'Number@','token':''}]
    fromX = X.logout(logoutBlock)
    print fromX


def testSearchUserInfo(uuid):
    info = {'token':uuid}
    fromX = X.searchUserInfo(info)
    print fromX

def testModifyUserInfo(uuid):
    info = {
        'token':uuid,
        'data':{
            'username':'first',
            'firstname':'second',
            'lastname':'third',
            'birthday':str(datetime.datetime.now()),
            'sex':'False',
            'tel':'13918102925'
        }
    }
    fromX = X.modifyUserInfo(info)
    print fromX

def testSearchBook(uuid):
    info = {'type':'auth','value':['Macmillan'],'token':uuid}
    fromX = X.searchBook(info)
    print fromX

def testAddBook(uuid):
    bookinfo = {
        'counts':'2',
        'isbn':'testisbn3',
        'clc':'testclc',
        'name':'testname',
        'auth':['auth1','auth2'],
        'publisher':'testpublisher',
        'edition':3,
        'publish_date':str(datetime.datetime.now()),
        'tags':['python','xxl'],
        'snapshot':'hahahahah'
    }
    info = {
        'token':uuid,
        'book':bookinfo
    }
    fromX = X.addBook(info)
    print fromX

def testBorrow(uuid):
    info = {'token':uuid,'books':['bf978c5e-945e-4a8e-bda3-55e5af445adc','d4221dde-e3cb-4a77-89f9-8a4e7b7e0c6a']}
    fromX = X.borrow(info)
    print fromX

def testSearchUserInfo(uuid):
    info = {'token':uuid,'status':['a']}
    fromX = X.searchUserOrder(info)
    print fromX

def testSearchAllUserInfo(uuid):
    info = {'token':uuid,'status':['a']}
    fromX = X.searchUserOrder(info)
    print fromX

def testReturn(uuid):
    info = {'token':uuid,'books':['bf978c5e-945e-4a8e-bda3-55e5af445adc','d4221dde-e3cb-4a77-89f9-8a4e7b7e0c6a']}
    fromX = X.returnBook(info)
    print fromX

if __name__ == '__main__':

    #X.Z.initUsers()
    X.Z.setConnDefalt()
    X.addFakerOrder()
    #testSignup()
    #token = testLogin()['token']
    #testSearchUserInfo(token)
    #testModifyUserInfo(token)
    #testSearchBook(token)
    #testAddBook(token)
    #testBorrow(token)
    #testSearchUserInfo(token)
    #testSearchAllUserInfo(token)
    #testReturn(token)
    #testLogout()
