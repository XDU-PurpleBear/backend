# -*- coding:utf-8 -*-
'''
Created on 2017年10月10日

@author: lenovo
'''
import database as Z

def login(blockInfo):
    returnInfo = {'Status':''}
    password = blockInfo['password']
    value = blockInfo['userKey']
    #
    dbPassword = Z.getPWD(type)['password']
    if dbPassword == '':
        errorInfo = 'I can\'t find this user!'
        returnInfo['Status'] = 'Failure'
        returnInfo['errorInfo'] = errorInfo
    else:
        if dbPassword != password:
            errorInfo = 'Wrong password!'
            returnInfo['Status'] = 'Failure'
            returnInfo['errorInfo'] = errorInfo
        else:
            right = Z.getUserInfo(value)['right']
            returnInfo['token'] = 'testToken'
            returnInfo['tokenDate'] = 1231
            if right == '1':
                returnInfo['usertype'] = 'customer'
            elif right == '2':
                returnInfo['usertype'] = 'admin'
            else :
                print 'others command'
            returnInfo['Status'] = 'Success'
    return returnInfo

def signup(blockInfo):
    returnInfo = {'Status':''} 
    password = blockInfo['password']
    username = blockInfo['username']
    tel = blockInfo['tel']
    dbUser = Z.getPWD(username)
    if dbUser != '':
        returnInfo['Status'] = 'Failure'
        returnInfo['errorInfo'] = 'This username has been existed!'
    else:
        dbTel = Z.getPWD(tel)
        if dbTel != '':
            returnInfo['Status'] = 'Failure'
            returnInfo['errorInfo'] = 'This telphone-number has been registered!'
        else:
            #
            dbInfo = Z.addUser(tel, username, password)
            returnInfo.update(dbInfo)
    return returnInfo

def logout(blockInfo):
    returnInfo = {'Status':''}
    userToken = blockInfo['token']
    #johnReturn = J.delToken(userToken)
    J = {}
    J.status = 'Success'
    J.errorInfo = 'Wrong'
    returnInfo['Status'] = J.status
    if J.status != 'Success':
        returnInfo['errorInfo'] = J.errorInfo
    return returnInfo

def modifyUserInfo(blockInfo):
    returnInfo = {}
    dbInfo = Z.modifyUserInfo(blockInfo)
    returnInfo.update(dbInfo)
    return returnInfo
    
def searchBook(blockInfo):
    returnInfo = {}
    token = blockInfo['token']
    #
    J = {}
    J.tokenDate = 'testDate'
    isISBN = False
    if blockInfo['bookname'] == None : 
        if blockInfo['booktype'] == None :
            queryInfo = blockInfo['ISBN']
            isISBN = True
        else :
            queryInfo = blockInfo['booktype']
    else:
        queryInfo = blockInfo['bookname']

    if isISBN:
        booklist = Z.queryBook(queryInfo)
    else:
        booklist = Z.queryBookKind(queryInfo)
    
    if len(booklist) < 1:
        returnInfo['Status'] = 'Failure'
        returnInfo['errorInfo'] = 'Do not have this book!'
    else:
        returnInfo['Status'] = 'Success'
        returnInfo['tokenDate'] = J.tokenDate
        returnInfo['booklist'] =booklist
    return returnInfo