# -*- coding:utf-8 -*-
'''
Created on 2017年10月10日

@author: lenovo
'''
from X import zzj as Z
from X import john as J

def login(blockInfo):
    #返回值
    returnInfo = {'status':''}
    #解析
    password = blockInfo['password']
    keys = blockInfo.keys()
    keys.remove('password')
    #print keys
    type = keys.pop()
    value = blockInfo[type]
    #data form db
    dbPassword = Z.queryUser(type)['password']
    #judge
    if dbPassword == '':
        errorInfo = 'I can\'t find this user!'
        returnInfo['status'] = 'Failed'
        returnInfo['errorInfo'] = errorInfo
    else:
        if dbPassword != password:
            errorInfo = 'Wrong password!'
            returnInfo['status'] = 'Failure'
            returnInfo['errorInfo'] = errorInfo
        else:
            UUID = Z.getUserUUID(value)['UUID']
            returnInfo.update(J.getToken(UUID))
            right = Z.getUserInfo(UUID)['right']
            if right == '1':
                returnInfo['usertype'] = 'reader'
            elif right == '2':
                returnInfo['usertype'] = 'librarian'
            else :
                print 'others command'
            returnInfo['status'] = 'Success'
    return returnInfo

def signup(blockInfo):
    returnInfo = {'status':''}
    password = blockInfo['password']
    keys = blockInfo.keys()
    keys.remove('password')
    #print keys
    type = keys.pop()
    value = blockInfo[type]
    dbPassword = Z.queryUser(type)['password']
    if dbPassword != '':
        errorInfo = 'This user has existed!'
        returnInfo['status'] = 'Failure'
        returnInfo['errorInfo'] = errorInfo
    else:
        dbInfo = Z.addUser(value, password)
        returnInfo.update(dbInfo)
    return returnInfo

def logout(blockInfo):
    returnInfo = {'status':''}
    userToken = blockInfo['token']
    johnReturn = J.delToken(userToken)
    returnInfo.update(johnReturn)
    return returnInfo

def modifyUserInfo(blockInfo):
    returnInfo = {}
    dbInfo = Z.modifyUserInfo(blockInfo)
    returnInfo.update(dbInfo)
    return returnInfo
    
def searchBook(blockInfo):
    returnInfo = {}
    clc = blockInfo['CLC']
    bookname = blockInfo['BookName']
    books = Z.queryBookKind(clc)
    if books.len() == 0:
        books = Z.queryBookKind(bookname)
    bookList = []
    for isbn in books:
        book = Z.queryBook(isbn)
        bookList.append(book)
    returnInfo['status'] = 'Success'
    returnInfo['booklist'] = bookList
    return returnInfo