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
    print info
    fordb = {'type':info['type'],'value':info['value']}
    retdb = Z.getUserUUID(fordb)
    #print '--------login--------'
    if retdb['status'] != 'success':
        retInfo = retdb
    else:

        userid = retdb['uuid']
        pwddb = Z.getUserPWD(userid)['password']
        password = info['password']
        #print pwddb
        #print password
        if pwddb != password:
            retInfo['status'] = 'failure'
            retInfo['errorInfo'] = 'Wrong password!'
        else:
            #print '--------login--------'
            user = Z.getUserInfo(userid)['data']
            right = int(user['right'])
            name = user['username']
            forjohn = {'uuid':userid,'right':right}
            retjohn = J.addToJohn(forjohn)
            print 'ret john',retjohn
            if retjohn['status'] != 'success':
                retInfo = retjohn
            else:
                retInfo = retjohn
                retInfo['username'] = name
                if right == 1:
                    retInfo['userType'] = 'customer'
                elif right == 2:
                    retInfo['userType'] = 'admin'
                else:
                    pass
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
            retInfo['data'] = retdb['data']
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
        fordb['uuid'] = retjohn['uuid']
        retdb = Z.modifyUserInfo(fordb)
        retInfo = retdb
        retInfo['tokenDate'] = retjohn['tokenDate']
        if retInfo.has_key('errorInfo'):
            print retInfo['errorInfo']
    return retInfo

def modifyUserPassword(info):
    return Z.modifyUserPWD(info)

def modifyUserBalance(info):
    return Z.modifyUserBalance(info)

def modifyUserRight(info):
    return Z.modifyUserRight(info)

def searchBook(info):
    retInfo = {}
    if info['token'] != None:
        forjohn = {'token':info['token']}
        retjohn = J.searchOnJohn(forjohn)
        if retjohn['status'] != 'success':
            retInfo = retjohn
            return retInfo
        else:
            retInfo['tokenDate'] = retjohn['tokenDate']
    #print info['value']
    fordb = {'type':info['type'],'value':info['value']}
    #print fordb
    print 'in func db for search -> ',fordb,' info -> ',info
    retdb = Z.searchISBN(fordb)
    #print 'in func'
    if retdb['status'] != 'success':
        retInfo = retdb
        print retInfo
    else:
        isbn = retdb['isbn']
        print isbn
        booklist = []
        #print isbn,"in func"
        for i in isbn:
            #print i,'in func'
            dbkind = Z.searchBookInfo(i)

            if dbkind['status'] != 'success':
                continue
            print 'on here'
            info = dbkind['data']
            info['isbn'] = i
            book = info
            dbinstance = Z.searchBookInstance(isbn=i, status='a---')
            if dbinstance['status'] != 'success':
                book['amount'] = 0
            else:
                uuids = []
                for uid in dbinstance['uuid']:
                    uuids.append(uid)
                book['amount'] = len(uuids)
            book['image'] = '/res/image?isbn='+ i
            booklist.append(book)
            #print booklist
        retInfo['data'] = booklist
        retInfo['status'] = 'success'

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
        #counts = bookinfo.pop('counts')
        bookinfo['publish_date'] = str(datetime.datetime.now())
        dbkind = Z.addBookInfo(bookinfo)
        if dbkind['status'] != 'success':
            print dbkind['errorInfo']
            return dbkind
        #counts = int(counts)
        #print type(counts)
        '''
        for i in range(counts):
            dbinstance = Z.addBookInstance(bookinfo['isbn'])
            if dbinstance['status'] != 'success':
                return dbinstance
            retInfo = dbinstance
        '''
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
            orderid = uid
            orderinfo = {'orderid':orderid,'timestamp':orders[orderid]['timestamp']}
            optids = orders[orderid]['opt']
            books = []
            optids = optids.replace('{','')
            optids = optids.replace('}','')
            optids = optids.split(',')
            for optid in optids:
                if info['status'] == 'a':
                    bookstatus = 'a---'
                else:
                    bookstatus = '--b-'
                dbinstance = Z.searchBookInstance(status=bookstatus,optid=optid)
                if dbinstance['status'] != 'success':
                    return dbinstance

                instanceids = dbinstance['uuid']
                isbn = dbinstance['isbn']

                dbkind = Z.searchBookInfo(isbn)
                if dbkind['status'] != 'success':
                    return dbkind
                book = dbkind['data']
                book['isbn'] = isbn
                book['image'] = 'res/image?isbn=' + isbn
                inid = instanceids.keys()[0]
                book['uuid'] = inid
                dbopera = Z.searchOperation(optid)
                if dbopera['status'] != 'success':
                    return dbopera
                returnDate = dbopera['returnDate']
                book['returnDate'] = returnDate
                books.append(book)
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
        userid = retjohn['uuid']
        dborder = Z.searchOrder(status=info['status'],uuid=userid)
        if dborder['status'] != 'success':
            return dborder
        orderlist = []
        orders = dborder['uuid']
        for uid in orders:
            orderid = uid
            userid = orders[orderid]['userUUID']
            dbuser = Z.getUserInfo(userid)
            if dbuser['status'] != 'success':
                return dbuser
            orderinfo = {'orderid':orderid,'timestamp':orders[orderid]['timestamp'],'user':dbuser['data']['username']}
            optids = orders[orderid]['opt']
            books = []
            optids = optids.replace('{','')
            optids = optids.replace('}','')
            optids = optids.split(',')
            for optid in optids:
                if info['status'] == 'a':
                    bookstatus = 'a---'
                else:
                    bookstatus = '--b-'
                dbinstance = Z.searchBookInstance(status=bookstatus,optid=optid)
                if dbinstance['status'] != 'success':
                    return dbinstance

                instanceids = dbinstance['uuid']
                isbn = dbinstance['isbn']

                dbkind = Z.searchBookInfo(isbn)
                if dbkind['status'] != 'success':
                    return dbkind
                book = dbkind['data']
                book['isbn'] = isbn
                inid = instanceids.keys()[0]
                book['uuid'] = inid
                dbopera = Z.searchOperation(optid)
                if dbopera['status'] != 'success':
                    return dbopera
                returnDate = dbopera['returnDate']
                book['returnDate'] = returnDate
                books.append(book)
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
        dborder = Z.addOrder({'userUUID':userid,'optid':optids,'status':['a']})
        if dborder['status'] != 'success':
            print dborder['errorInfo']
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
            optid = dbinstance['uuid'][i]
            dbinstance = Z.modifyBookInstance({'uuid':i,'status':'a---'})
            if dbinstance['status'] != 'success':
                return dbinstance
            '''
            dbinstance = Z.modifyBookInstance({'uuid':i,'optid':'null'})
            if dbinstance['status'] != 'success':
                return dbinstance
            '''
            print 'test'
            dboper = Z.modifyOperationStatus({'uuid':optid,'status':'a---'})
            if dboper['status'] != 'success':
                return dboper
    return retInfo

def getBookInfo(info):
    retInfo = {}
    print info
    if info['token'] != None:
        forjohn = {'token':info['token']}
        retjohn = J.searchOnJohn(forjohn)
        if retjohn['status'] != 'success':
            retInfo = retjohn
            return retInfo
        else:
            retInfo['tokenDate'] = retjohn['tokenDate']
    #print retInfo
    isbn = info['ISBN']
    dbkind = Z.searchBookInfo(isbn)
    if dbkind['status'] != 'success':
        return dbkind
    print isbn
    dbinstance = Z.searchBookInstance(isbn=isbn, status='a---')
    if dbinstance['status'] != 'success':
        return dbinstance
    #print '00000000000000'
    uuids = []
    for uid in dbinstance['uuid']:
        uuids.append({'uuid':uid,'status':'a---'})
    bookinfo = dbkind['data']
    bookinfo['copys'] = uuids
    bookinfo['image'] = '/res/image?isbn=' + isbn
    retInfo = {'status':'success','data':bookinfo}
    return retInfo

def addBookInfoNew(info):
    retInfo = {}
    forjohn = {'token':info['token']}
    retjohn = J.searchOnJohn(forjohn)
    if retjohn['status'] != 'success':
        retInfo = retjohn
        return retInfo

    data = info

    #print data
    print 'add book in func info->',info,' data -> ',data
    dbkind = Z.addBookInfo(data)
    if dbkind['status'] != 'success':
        return dbkind
    pic = data['image']['data']
    retInfo = Z.addBookPicture({'isbn':info['isbn'],'data':pic})

    retInfo['tokenDate'] = retjohn['tokenDate']
    return retInfo

def editBookInfoNew(info):
    retInfo = {}
    forjohn = {'token':info['token']}
    retjohn = J.searchOnJohn(forjohn)
    if retjohn['status'] != 'success':
        retInfo = retjohn
        return retInfo
    data = info
    dbkind = Z.modifyBookInfo(data)
    if dbkind['status'] != 'success':
        return dbkind
    pic = data.pop('image')
    retInfo = Z.modifyBookPicture({'isbn':info['isbn'],'data':pic})
    retInfo['tokenDate'] = retjohn['tokenDate']
    return retInfo

def addCopy(info):
    retInfo = {}
    forjohn = {'token':info['token']}
    retjohn = J.searchOnJohn(forjohn)
    if retjohn['status'] != 'success':
        retInfo = retjohn
        return retInfo
    retInfo = Z.addBookInstance(info['isbn'])
    print info['isbn']
    print retInfo,'in func'
    retInfo['tokenDate'] = retjohn['tokenDate']
    return retInfo

def getImage(isbn):
    dbkind = Z.searchPicture(isbn)
    if dbkind == 'this isbn not exits!':
        retInfo = {'status':'failure','errorInfo':dbkind}
    else:
        retInfo = {'status':'success','image':dbkind}
    return retInfo

def addFakerOrder():
    info = {'type':'auth','value':['Macmillan'],'token':None}
    ret = searchISBN(info)
    print ret

def applyBook(info):
    retInfo = {}
    forjohn = {'token':info['token']}
    retjohn = J.searchOnJohn(forjohn)
    if retjohn['status'] != 'success':
        retInfo = retjohn
        return retInfo
    retInfo['tokenDate'] = retjohn['tokenDate']
    fordb={}
    fordb["uuid"]=retjohn["uuid"]
    fordb["books"]=info["books"]
    retdb = Z.addWondefList(fordb)
    if retdb["status"] != "success":
        return retdb
    else:
        return retdb

def addWonderCopy(info):
    retInfo = {}
    forjohn = {'token':info['token']}
    retjohn = J.searchOnJohn(forjohn)
    if retjohn['status'] != 'success':
        retInfo = retjohn
        return retInfo
    retInfo['tokenDate'] = retjohn['tokenDate']
    #print retInfo
    retdb = Z.searchWonderList(retjohn["uuid"])
    if retdb["status"] != "success":
        dbWonder = Z.addWondefList({'uuid':retjohn['uuid'],'books':info['books']})
    else:
        old = retdb['books']
        old.append(info['books'])
        dbWonder = Z.modifyWonderList({'uuid':retjohn['uuid'],'books':old})
    dbWonder['tokenDate'] = retjohn['tokenDate']
    return dbWonder

def getApplyList(info):
    retInfo = {}
    forjohn = {'token':info['token']}
    retjohn = J.searchOnJohn(forjohn)
    if retjohn['status'] != 'success':
        retInfo = retjohn
        return retInfo
    retInfo['tokenDate'] = retjohn['tokenDate']

    uerid = retjohn['uuid']
    retdb = Z.searchWonderList(retjohn["uuid"])
    if retdb["status"] != "success":
        return retdb
    booids = retdb['books']
    books = []
    for book in bookids:
        dbinstance = Z.searchBookInstance(status='a---',uuid=book)
        if dbinstance['status'] != 'success':
            return dbinstance
        isbn = dbinstance['isbn']
        dbkind = Z.searchBookInfo(isbn)
        bookinfo['name'] = dbkind['data']['name']
        bookinfo['ISBN'] = dbkind['data']['isbn']
        bookinfo['auth'] = dbkind['data']['auth']
        bookinfo['position'] = dbkind['data']['clc']
        bookinfo['uuid'] = bookinfo
        books.append(bookinfo)
    return {'status':'success','data':books}
