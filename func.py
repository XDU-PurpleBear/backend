# -*- coding:utf-8 -*-
'''
Created on 2017年10月10日

@author: lenovo
'''
from database import Database as Z
import John as J
import datetime

def login(info):
    retInfo = {}
    fordb = {'type':info['type'],'value':info['value']}
    retdb = Z.getUserUUID(fordb)
    if retdb['status'] != 'success':
        retInfo = retdb
    else:
        userid = retdb['uuid']
        pwddb = Z.getUserPWD(userid)['password']
        password = info['password']
        if pwddb != password:
            retInfo['status'] = 'failure'
            retInfo['errorInfo'] = 'Wrong password!'
        else:
            right = Z.getUserInfo(userid)['data']['right']
            forjohn = {'uuid':userid,'right':right}
            retjohn = J.addToJohn(forjohn)
            if retjohn['status'] != 'success':
                retInfo = retjohn
            else:
                retInfo = retjohn
                retInfo['right'] = right
    return retInfo

def signup(info):
    retInfo = {}
    fordb = {'type':'tel','value':info['tel']}
    telid = Z.getUserUUID(fordb)
    if telid['status'] == 'success':
        retInfo['status'] = 'failure'
        retInfo['errorInfo'] = 'This tel has been registered!'
    else:
        fordb = {'type':'username','value':info['username']}
        nameid = Z.getUserUUID(fordb)
        if nameid['status'] == 'success':
            retInfo['status'] = 'failure'
            retInfo['errorInfo'] = 'This username has been registered!'
        else:
            fordb = {'password':info['password'],'tel':info['tel'],'username':info['username']}
            retdb = Z.addUser(fordb)
            retInfo = retdb
    return retInfo

def logout(info):
    retInfo = {}
    forjohn = {'token':info['token']}
    retjohn = J.deleteOnJohn(forjohn)
    retInfo = retjohn
    return retInfo

def searchUserInfo(info):
    retInfo = {}
    forjohn = {'token':info['token']}
    retjohn = J.searchOnJohn(forjohn)
    if retjohn['status'] != 'success':
        retInfo = retjohn
    else:
        retInfo['tokenDate'] = retjohn['tokenDate']
        retdb = Z.getUserInfo(retjohn['uuid'])
        if retdb['status'] != 'success':
            retInfo = retdb
        else:
            retInfo = retdb
            retInfo['data'].pop('right')
            retInfo['data'].pop('balance')
    return retInfo

def modifyUserInfo(info):
    retInfo = {}
    forjohn = {'token':info['token']}
    retjohn = J.searchOnJohn(forjohn)
    if retjohn['status'] != 'success':
        retInfo = retjohn
    else:
        fordb = info['data']
        retdb = Z.modifyUserInfo(fordb)
        retInfo = retdb
        retInfo['tokenDate'] = retjohn['tokenDate']
    return retInfo

def modifyUserPassword(info):
    return Z.modifyUserPWD(info)

def modifyUserBalance(info):
    return Z.modifyUserBalance(info)

def modifyUserRight(info):
    return Z.modifyUserRight(info)
    
def searchBook(info):
    retInfo = {}
    if info.has_key('token'):
        forjohn = {'token':info['token']}
        retjohn = J.searchOnJohn(forjohn)
        if retjohn['status'] != 'success':
            retInfo = retjohn
            return retInfo
        else:
            retInfo['tokenDate'] = retjohn['tokenDate']
    
    fordb = {'type':info['type'],'value':info['value']}
    retdb = Z.searchISBN(fordb)
    if retdb['status'] != 'success':
        retInfo = retdb
    else:
        isbn = retdb['isbn']
        booklist = []
        for i in isbn:
            dbkind = Z.searchBookInfo(i)
            if dbkind['status'] != 'success':
                return dbkind
            info = dbkind['data']
            info['isbn'] = i
            dbinstance = Z.searchBookInstance(isbn=i, status='a---')
            if dbinstance['status'] != 'success':
                return dbinstance
            uuids = []
            for uid in dbinstance['uuid']:
                uuids.append(uid.keys()[0])
            book = {'uuid':uuids,'info':info}
            booklist.append(book)
        retInfo['data'] = booklist
    return retInfo

def addBook(info):
    retInfo = {}
    forjohn = {'token':info['token']}
    retjohn = J.searchOnJohn(forjohn)
    if retjohn['status'] != 'success':
        retInfo = retjohn
    else:
        retInfo['tokenDate'] = retjohn['tokenDate']
        bookinfo = info['book']
        counts = bookinfo.pop('counts')
        dbkind = Z.addBookInfo(bookinfo)
        if dbkind['status'] != 'success':
            return dbkind
        if type(counts) == 'str':
            counts = int(counts)
        for i in range(counts):
            dbinstance = Z.addBookInstance(bookinfo['isbn'])
            if dbinstance['status'] != 'success':
                return dbinstance
            retInfo = dbinstance
    return retInfo

def modifyBookInfo(info):
    retInfo = {}
    forjohn = {'token':info['token']}
    retjohn = J.searchOnJohn(forjohn)
    if retjohn['status'] != 'success':
        retInfo = retjohn
    else:
        retInfo['tokenDate'] = retjohn['tokenDate']
        bookkind = info['book']
        dbkind = Z.modifyBookInfo(bookkind)
        if dbkind['status'] != 'success':
            return dbkind
        oper = info['books']
        if oper.has_key('add'):
            counts = int(oper['add'])
            for i in range(counts):
                dbinstance = Z.addBookInstance(bookkind['isbn'])
                if dbinstance['status'] != 'success':
                    return dbinstance
        elif oper.has_key('delete'):
            uuids = oper['delete']
            for i in uuids:
                dbinstance = Z.modifyBookInstance({'uuid':i,'status':'-u--'})
                if dbinstance['status'] != 'success':
                    return dbinstance
        retInfo['status'] = 'success'
    return retInfo

def searchUserOrder(info):
    retInfo = {}
    forjohn = {'token':info['token']}
    retjohn = J.searchOnJohn(forjohn)
    if retjohn['status'] != 'success':
        retInfo = retjohn
    else:
        retInfo['tokenDate'] = retjohn['tokenDate']
        userid = retjohn['uuid']
        dborder = Z.searchOrder(status=info['status'],uuid=userid)
        if dborder['status'] != 'success':
            return dborder
        orderlist = []
        orders = dborder['uuid']
        for uid in orders:
            orderid = uid.keys()[0]
            orderinfo = {'orderid':orderid,'timestamp':uid[orderid]['timestamp']}
            optids = uid[orderid]['opt']
            books = []
            for optid in optids:
                dbinstance = Z.searchBookInstance(status=info['status'],optid=optid)
                if dbinstance['status'] != 'success':
                    return dbinstance
                instanceids = dbinstance['uuid']
                bookuuid = []
                for inid in instanceids:
                    id = inid.keys()[0]
                    dbopera = Z.searchOperation(id)
                    if dbopera['status'] != 'success':
                        return dbopera
                    returnDate = dbopera['returnDate']
                    bookuuid.append({'uuid':id,'returnDate':returnDate})
                isbn = dbinstance['isbn']
                dbkind = Z.searchBookInfo(isbn)
                if dbkind['status'] != 'success':
                    return dbkind
                bookinfo = dbkind['data']
                books.append({'uuid':bookuuid,'info':bookinfo})
            orderinfo['books'] = books
            orderlist.append(orderinfo)
        retInfo['status'] = 'success'
        retInfo['data'] = orderlist
    return retInfo

def searchAllUserOrder(info):
    retInfo = {}
    forjohn = {'token':info['token']}
    retjohn = J.searchOnJohn(forjohn)
    if retjohn['status'] != 'success':
        retInfo = retjohn
    else:
        retInfo['tokenDate'] = retjohn['tokenDate']
        dborder = Z.searchOrder(status=info['status'])
        if dborder['status'] != 'success':
            return dborder
        orderlist = []
        orders = dborder['uuid']
        for uid in orders:
            orderid = uid.keys()[0]
            userid = uid[orderid]['userUUID']
            dbuser = Z.getUserInfo(userid)
            if dbuser['status'] != 'success':
                return dbuser
            orderinfo = {'orderid':orderid,'timestamp':uid[orderid]['timestamp'],'user':dbuser['data']['username']}
            optids = uid[orderid]['opt']
            books = []
            for optid in optids:
                dbinstance = Z.searchBookInstance(status=info['status'],optid=optid)
                if dbinstance['status'] != 'success':
                    return dbinstance
                instanceids = dbinstance['uuid']
                bookuuid = []
                for inid in instanceids:
                    id = inid.keys()[0]
                    dbopera = Z.searchOperation(id)
                    if dbopera['status'] != 'success':
                        return dbopera
                    returnDate = dbopera['returnDate']
                    bookuuid.append({'uuid':id,'returnDate':returnDate})
                isbn = dbinstance['isbn']
                dbkind = Z.searchBookInfo(isbn)
                if dbkind['status'] != 'success':
                    return dbkind
                bookinfo = dbkind['data']
                books.append({'uuid':bookuuid,'info':bookinfo})
            orderinfo['books'] = books
            orderlist.append(orderinfo)
        retInfo['status'] = 'success'
        retInfo['data'] = orderlist
    return retInfo

def borrow(info):
    retInfo = {}
    forjohn = {'token':info['token']}
    retjohn = J.searchOnJohn(forjohn)
    if retjohn['status'] != 'success':
        retInfo = retjohn
    else:
        retInfo['tokenDate'] = retjohn['tokenDate']
        userid = retjohn['uuid']
        books = info['books']
        optids = []
        for i in books:
            currentTime = str(datetime.datetime.now() + datetime.timedelta(45))
            date = [currentTime]
            dboper = Z.addOperation({'returnDate':date,'status':'--b-'})
            if dboper['status'] != 'success':
                return dboper
            optid = dboper['uuid']
            dbinstance = Z.modifyBookInstance({'uuid':i,'optid':optid})
            if dbinstance['status'] != 'success':
                return dbinstance
            dbinstance = Z.modifyBookInstance({'uuid':i,'status':'--b-'})
            if dbinstance['status'] != 'success':
                return dbinstance
            optids.append(optid)
        dborder = Z.addOrder({'userUUID':userid,'optid':optids,'status':'applying'})
        if dborder['status'] != 'success':
            return dborder
    return retInfo

def returnBook(info):
    retInfo = {}
    forjohn = {'token':info['token']}
    retjohn = J.searchOnJohn(forjohn)
    if retjohn['status'] != 'success':
        retInfo = retjohn
    else:
        retInfo['tokenDate'] = retjohn['tokenDate']
        userid = retjohn['uuid']
        books = info['books']
        for i in books:
            
            dbinstance = Z.searchBookInstance(status='--b-',uuid=i)
            if dbinstance['status'] != 'success':
                return dbinstance
            optid = dbinstance['uuid'][0][i]
            dbinstance = Z.modifyBookInstance({'uuid':i,'status':'a---'})
            if dbinstance['status'] != 'success':
                return dbinstance
            dbinstance = Z.modifyBookInstance({'uuid':i,'optid':None})
            if dbinstance['status'] != 'success':
                return dbinstance
            dboper = Z.modifyOperationStatus({'uuid':optid,'status':'a---'})
            if dboper['status'] != 'success':
                return dboper
    return retInfo   