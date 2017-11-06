# -*- coding:utf-8 -*-
'''
Created on 2017��11��1��

@author: lenovo
'''
from database import Database as Z
import John as J
import tools
import datetime

def login(info):
    fordb = {'type':info['type'],'value':info['value']}
    #��ѯ�û��Ƿ�������ݿ�
    retdb = Z.getUserUUID(fordb)
    if retdb['status'] != 'success':
        return retdb
    #��һ����Ϊ�ų�ϵͳ����
    retdb = Z.getUserPWD(retdb['uuid'])
    if retdb['status'] != 'success':
        return retdb
    #�����ʵ
    if retdb['password'] != info['password']:
        retinfo = {'status':'failure','errorInfo':'Wrong password!'}
        return retinfo
    userinfo = Z.getUserInfo(userid)['data']
    right = int(userinfo['right'])
    #�ύuuid��Ȩ�ޣ�ʹ���Ϊ�����û�
    retjohn = J.addToJohn({'uuid':userid,'right':right})
    if retjohn['status'] != 'success':
        return retjohn
    #��������ֵ
    if right == 1:
        usertype = 'customer'
    elif right == 2:
        usertype  = 'admin'
    else:
        usertype  = 'unknown'
    retinfo = {
        'status':'success',
        'token' : retjohn['token'],
        'tokendate' : retjohn['tokenDate'],
        'username' : userinfo['username'],
        'usertype' : usertype,
        'data':{
            'image' : userinfo['image'],
        }
    }
    return retinfo

def logout(info):
    retjohn = Z.deleteOnJohn({'token':info['token']})
    return retjohn

def searchBook(info):
    tokendate = ''
    #����Ƿ����token
    if info.has_key(token):
        retjohn = J.searchOnJohn({'token':info['token']})
        if retjohn['status'] != 'success':
            return retjohn
        tokendate = retjohn['tokenDate']
    #��ȡISBN
    retdb = Z.searchISBN({'type':info['type'],'value':info['value']})
    if retdb['status'] != 'success':
        if tokendate != '':
            retdb['tokendate'] = tokendate
        return retdb
    isbns = retdb['isbn']
    booklist,languages,roomsthemes = [],[],[]
    for isbn in isbns:
        #����isbn��ȡ�鼮������Ϣ
        dbkind = Z.searchBookInfo(isbn)
        if dbkind['status'] != 'success':
            continue
        position = tools.divideLocation(Z.searchLocation(dbkind['data']['lc']))
        tag = tools.divideTags(dbkind['data']['tags'])
        #��ȡɸѡ������
        languages.extend(tag['language'])
        themes.extend(tag['theme'])
        rooms.extend(position['room'])
        #����isbn��ȡ����������Ϣ
        counts = 0
        dbinstance = Z.searchBookInstance(isbn=isbn)
        if dbinstance['status'] == 'success':
            instanceinfo = dbinstance['data']['uuids']
            for i in instanceinfo:
                if i['status'] == 'a---':
                    counts += 1
        #�����鼮��Ϣ
        book = {
            'name':dbkind['data']['name'],
            'ISBN':dbkind['data']['isbn'],
            'auth':dbkind['data']['auth'],
            'position':position,
            'language':tag['language'],
            'theme':tag['theme'],
            'image':dbkind['data']['imgs'],
            'amount':counts
        }
        #�����б�
        booklist.append(book)
    #��������ֵ
    retinfo = {
        'status':'failure',
        'data':{
            'bookList':booklist,
            'filter':{
                'language':list(set(languages)),
                'room':list(set(rooms)),
                'theme':list(set(themes))
            }
        }
    }
    if tokendate != '':
        retinfo['tokendate'] = tokendate
    return retinfo

def searchBookByISBN(info):
    #��ѯtoken,�ж��û�����״̬��֮���ʹ�÷���ֵ�е�right
    tokendate = ''
    if info.has_key('token'):
        retjohn = J.searchOnJohn({'token':info['token']})
        if retjohn['status'] != 'success':
            return retjohn
        tokendate = retjohn['tokenDate']
    #����isbn��ѯ�鼮������Ϣ
    dbkind = Z.searchBookInfo(info['isbn'])
    if dbkind['status'] != 'success':
        if tokendate != '':
            dbkind['tokendate'] = retjohn['tokenDate']
        return dbkind
    #�����鼮��Ϣ
    position = tools.divideLocation(Z.searchLocation(dbkind['data']['lc']))
    tag = tools.divideTags(dbkind['data']['tags'])
    bookinfo = {
        'name':dbkind['data']['name'],
        'auth':dbkind['data']['auth'],
        'version':dbkind['data']['edition'],
        'ISBN':dbkind['data']['isbn'],
        'publisher':dbkind['data']['publisher'],
        'CLC':dbkind['data']['lc'],
        'image':dbkind['data']['imgs'],
        'description':dbkind['data']['abstract'],
        'position':position,
        'language':tag['language'],
        'theme':tag['theme'],
    }
    #����isbn��ѯ������Ϣ������right��bookinfo�������Ӧ��Ϣ
    counts = 0
    dbinstance = Z.searchBookInstance(info['isbn'])
    if dbinstance['status'] != 'success':
        bookinfo['amount'] = counts
        bookinfo['copys'] = []
    else:
        books = dbinstance['data']['uuids']
        copys = []
        for book in books:
            if retjohn['right'] == 2:
                copys.append({
                    'uuid':book['uuid'],
                    'status':tools.changeBookStatus(book['status'])
                })
                counts = len(books)
            elif book['status'] == 'a---':
                copys.append({
                    'uuid':book['uuid'],
                    'status':'Available'
                })
                counts += 1
            else:
                pass
        bookinfo['amount'] = counts
        bookinfo['copys'] = copys
    retinfo = {
        'status':'success',
        'data':{
            'bookInfo':bookinfo
        }
    }
    if tokendate != '':
        retinfo['tokendate'] = tokendate
    return retinfo

def recomends(info):
    #�ж��������û���ע���û��������ο�
    tokendate = ''
    if info.has_key('token'):
        retjohn = J.searchOnJohn({'token':info['token']})
        if retjohn['status'] != 'success':
            return retjohn
        tokendate = retjohn['tokenDate']
    #��ȡС���Ƽ���isbn
    isbns = tools.getRecomends(2)
    #��ѯ��Ӧ��Ϣ
    booklist = []
    for isbn in isbns:
        dbkind = Z.searchBookInfo(isbn)
        if dbkind['status'] != 'success':
            continue
        book = {
            'name':dbkind['data']['name'],
            'ISBN':dbkind['data']['isbn'],
            'description':dbkind['data']['abstract'],
            'image':dbkind['data']['imgs']
        }
        booklist.append(book)
    #��������ֵ
    retinfo = {
        'status':'success',
        'data':{
            'bookList':booklist
        }
    }
    if tokendate != '':
        retinfo['tokendate'] = tokendate
    return retinfo

def searchOverdueOrder(info):
    #����״̬��ѯ
    retjohn = Z.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    #����Ȩ�޲�ѯ���ڶ���������Ϣ
    if retjohn['right'] == 1:
        dborder = Z.searchOrder(userid=retjohn['uuid'],status='---o-')
        if dborder['status'] != 'success':
            orders = []
        else:
            orders = dborder['data']
    else:
        dborder = Z.searchOrder(status='---o-')
        if dborder['status'] != 'success':
            orders = []
        else:
            orders = dborder['data']
    #����������Ϣ
    orderlist = []
    if len(orders) != 0:
        for order in orders:
            #��ȡ�鼮��Ϣ
            dbinstance = Z.searchBookInstance(optid=order['bookid'])
            if dbinstance['status'] != 'success':
                continue
            dbkind = Z.searchBookInfo(dbinstance['data']['isbn'])
            if dbkind['status'] != 'success':
                continue
            #��ȡ�鼮��������
            dbbooks = Z.searchBookInstance(isbn=dbinstance['data']['isbn'])
            books = dbbooks['data']['uuids']
            counts = 0
            for book in books:
                if book['status'] == 'a---':
                    counts += 1
            #��ȡ��������
            dboper = Z.searchOperation(order['bookid'])
            if dboper['status'] != 'success':
                continue
            borrowDate = str(dboper['date'][-1])
            #��ȡ�û���Ϣ
            dbuser = Z.getUserInfo(order['userid'])
            if dbuser['status'] != 'success':
                continue
            #����������Ϣ
            now = str(datetime.datetime.now())
            overdays = tools.getMinus(now,borrow)
            #����������Ϣ
            orderinfo = {
                'orderid':order['orderid'],
                'applyDate':str(order['timestamp']),
                'ISBN':dbinstance['data']['isbn'],
                'borrowDate':borrowDate,
                'overDays':overdays,
                'fine':overdays * 1,
                'bookName':dbkind['data']['name'],
                'auth':dbkind['data']['auth'],
                'image':dbkind['data']['imgs'],
                'position':tools.divideLocation(Z.searchLocation(dbkind['data']['lc'])),
                'bookid':dbinstance['data']['uuids']['uuid'],
                'amount':counts,
                'userid':dbuser['data']['uuid'],
                'userName':dbuser['data']['username'],
                'balance':dbuser['data']['balance']
            }
        orderlist.append(orderinfo)
    #��������ֵ
    retinfo = {
        'status':'success',
        'data':{
            'orderList':orderlist
        }
    }

def getUserInfo(info):
    #����״̬��ѯ
    retjohn = Z.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    #��ʵ���
    if retjohn['right'] == '2':
        return {
            'status':'failure',
            'errorInfo':'Admin do not have a INfo Page!',
            'tokendate':retjohn['tokenDate']
        }
    #��ѯ�û�������Ϣ
    dbuser = Z.getUserInfo(retjohn['uuid'])
    if dbuser['status'] != 'success':
        dbuser['tokendate'] = retjohn['tokenDate']
        return dbuser
    #��ѯ����������Ϣ
    dborder = Z.searchOrder(userid=retjohn['uuid'],status='---o-')
    if dborder['status'] != 'success':
        dborder['tokendate'] = retjohn['tokenDate']
        return dborder
    orders = dborder['data']
    overdays = 0
    for order in orders:
        optid = order['bookid']
        borrowdate = str(Z.searchOperation(uuid))
        now = str(datetime.datetime.now())
        overdays += tools.getMinus(now,borrowdate)
    #�����û���Ϣ
    userinfo = {
        'userName':dbuser['data']['username'],
        'uuid':dbuser['data']['uuid'],
        'studentID':dbuser['data']['stuid'],
        'tel':dbuser['data']['tel'],
        'balance':dbuser['data']['balance'],
        'userImage':dbuser['data']['logo'],
        'orderNumber':len(orders),
        'fine':overdays * 1
    }


def searchHistory(info):
    #����״̬��ѯ
    retjohn = Z.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    #��ȡ��ʷ��¼
    dbhistory = Z.searchHistory(retjohn['uuid'])
    if dbhistory['status'] != 'success':
        dbhistory['toekndate'] = retjohn['toeknDate']
        return dbhistory
    historys = dbhistory['data']
    booklist = []
    for his in historys:
        #��ȡ�鼮������Ϣ
        isbn = his['bookid']
        dbkind = Z.searchBookInfo(isbn)
        if dbkind['status'] != 'success':
            continue
        #�����鼮��Ϣ
        tag = tools.divideTags(dbkind['tags'])
        bookinfo = {
            'name':dbkind['data']['name'],
            'ISBN':dbkind['data']['isbn'],
            'position':tools.divideLocation(Z.searchLocation(dbkind['data']['lc'])),
            'theme':tag['theme'],
            'language':tag['language'],
            'image':dbkind['data']['imgs']
        }
        booklist.append(bookinfo)
    #��������ֵ
    retinfo = {
        'status':'success',
        'data':{
            'bookList':booklist
        },
        'tokendate':retjohn['tokenDate']
    }
    return retinfo
