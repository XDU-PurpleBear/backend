# -*- coding:utf-8 -*-
'''
Created on 2017年10月10日

@author: lenovo
'''
import database as Z
import John as J



def login(blockInfo):
    returnInfo = {'Status':''}
    password = blockInfo['password']
    value = blockInfo['userKey']
    userType = blockInfo['userType']
    if userType == 'tel':
        dbPassword = Z.Database.getPWD(tel=value)['password']
    elif userType == 'userName':
        dbPassword = Z.Database.getPWD(user_name=value)['password']
    else:
        dbPassword == ''
    print dbPassword
    if dbPassword == '':
        errorInfo = 'I can\'t find this user!'
        returnInfo['Status'] = 'Failure'
        returnInfo['errorInfo'] = errorInfo
    else:
        if dbPassword != password:
            print password
            errorInfo = 'Wrong password!'
            returnInfo['Status'] = 'Failure'
            returnInfo['errorInfo'] = errorInfo
        else:
            if userType == 'userName':
                user= Z.Database.getUserInfo(user_name=value)
            elif userType == 'tel':
                user = Z.Database.getUserInfo(tel=value)

            username = user.user_name

            retJohn = J.getToken(username)

            right = user.right

            returnInfo['username'] = username
            returnInfo['token'] = retJohn['token']
            returnInfo['tokenDate'] = retJohn['nextExipre']
            if right == 1:
                returnInfo['userType'] = 'customer'
            elif right == 2:
                returnInfo['userType'] = 'admin'
            else :
                returnInfo['userType'] = 'customer'
            returnInfo['Status'] = 'Success'
    return returnInfo

def signup(blockInfo):

    returnInfo = {'Status':''}
    password = blockInfo['password']
    username = blockInfo['username']
    tel = blockInfo['tel']
    dbUser = Z.Database.getPWD(user_name=username)['password']
    print dbUser
    if dbUser != '':
        returnInfo['Status'] = 'Failure'
        returnInfo['errorInfo'] = 'This username has been existed!'
        print returnInfo['errorInfo']
    else:
        dbTel = Z.Database.getPWD(tel=tel)['password']
        if dbTel != '':
            returnInfo['Status'] = 'Failure'
            returnInfo['errorInfo'] = 'This telphone-number has been registered!'
            print returnInfo['errorInfo']
        else:
            dbInfo = Z.Database.addUser(tel, username, password)
            returnInfo.update(dbInfo)
    return returnInfo

def logout(blockInfo):
    returnInfo = {'Status':''}
    userToken = blockInfo['token']
    #johnReturn = J.delToken(userToken)
    username = blockInfo['username']
    retJohn = J.deleteToken(username)
    if retJohn['status'] != 'success':
        returnInfo['Status'] = 'Falure'
        returnInfo['errorInfo'] = retJohn['msg']
    else :
        returnInfo['Status'] = 'Success'
    return returnInfo

def modifyUserInfo(blockInfo):
    returnInfo = {}
    dbInfo = Z.Database.modifyUserInfo(blockInfo)
    returnInfo.update(dbInfo)
    return returnInfo

def searchBook(blockInfo):
    returnInfo = {}
    token = blockInfo['token']
    #
    J = {'tokenDate':'testDate',}
    isISBN = False

    if blockInfo['bookname'] == None :
        if blockInfo['booktype'] == None :
            queryInfo = blockInfo['ISBN']
            isISBN = True
            booklist = Z.Database.queryBook(queryInfo)
        else :
            queryInfo = blockInfo['booktype']
            booklist = Z.Database.queryBookKind(clc=queryInfo)
    else:
        queryInfo = blockInfo['bookname']
        booklist = Z.Database.queryBookKind(name=queryInfo)

    #print 'xxxxx', len(booklist)
    books = []
    for book in booklist:
        books.append(book.__dict__)
    if len(booklist) < 1:
        returnInfo['Status'] = 'Failure'
        returnInfo['errorInfo'] = 'Do not have this book!'
    else:
        returnInfo['Status'] = 'Success'
        returnInfo['tokenDate'] = J['tokenDate']
        returnInfo['booklist'] =books
    return returnInfo
