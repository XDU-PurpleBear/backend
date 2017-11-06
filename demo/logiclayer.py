# -*- coding:utf-8 -*-
'''
Created on 2017年11月1日

@author: lenovo
'''
from database import Database as Z
import John as J
import tools
import datetime

def login(info):
    fordb = {'type':info['type'],'value':info['value']}
    #查询用户是否存在数据库
    retdb = Z.getUserUUID(fordb)
    if retdb['status'] != 'success':
        return retdb
    #这一步仅为排除系统错误
    retdb = Z.getUserPWD(retdb['uuid'])
    if retdb['status'] != 'success':
        return retdb
    #密码核实
    if retdb['password'] != info['password']:
        retinfo = {'status':'failure','errorInfo':'Wrong password!'}
        return retinfo
    userinfo = Z.getUserInfo(userid)['data']
    right = int(userinfo['right'])
    #提交uuid及权限，使其成为在线用户
    retjohn = J.addToJohn({'uuid':userid,'right':right})
    if retjohn['status'] != 'success':
        return retjohn
    #构建返回值
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
    #检查是否存在token
    if info.has_key(token):
        retjohn = J.searchOnJohn({'token':info['token']})
        if retjohn['status'] != 'success':
            return retjohn
        tokendate = retjohn['tokenDate']
    #获取ISBN
    retdb = Z.searchISBN({'type':info['type'],'value':info['value']})
    if retdb['status'] != 'success':
        if tokendate != '':
            retdb['tokendate'] = tokendate
        return retdb
    isbns = retdb['isbn']
    booklist,languages,roomsthemes = [],[],[]
    for isbn in isbns:
        #根据isbn获取书籍基本信息
        dbkind = Z.searchBookInfo(isbn)
        if dbkind['status'] != 'success':
            continue
        position = tools.divideLocation(Z.searchLocation(dbkind['data']['lc']))
        tag = tools.divideTags(dbkind['data']['tags'])
        #获取筛选器数据
        languages.extend(tag['language'])
        themes.extend(tag['theme'])
        rooms.extend(position['room'])
        #根据isbn获取副本数量信息
        counts = 0
        dbinstance = Z.searchBookInstance(isbn=isbn)
        if dbinstance['status'] == 'success':
            instanceinfo = dbinstance['data']['uuids']
            for i in instanceinfo:
                if i['status'] == 'a---':
                    counts += 1
        #构建书籍信息
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
        #加入列表
        booklist.append(book)
    #构建返回值
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
    #查询token,判断用户在线状态，之后会使用返回值中的right
    tokendate = ''
    if info.has_key('token'):
        retjohn = J.searchOnJohn({'token':info['token']})
        if retjohn['status'] != 'success':
            return retjohn
        tokendate = retjohn['tokenDate']
    #根据isbn查询书籍基本信息
    dbkind = Z.searchBookInfo(info['isbn'])
    if dbkind['status'] != 'success':
        if tokendate != '':
            dbkind['tokendate'] = retjohn['tokenDate']
        return dbkind
    #构建书籍信息
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
    #根据isbn查询副本信息，根据right在bookinfo中添加相应信息
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
    #判断是哪种用户，注册用户，或是游客
    tokendate = ''
    if info.has_key('token'):
        retjohn = J.searchOnJohn({'token':info['token']})
        if retjohn['status'] != 'success':
            return retjohn
        tokendate = retjohn['tokenDate']
    #获取小编推荐的isbn
    isbns = tools.getRecomends(2)
    #查询相应信息
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
    #构建返回值
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
    #在线状态查询
    retjohn = Z.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    #根据权限查询超期订单基本信息
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
    #构建订单信息
    orderlist = []
    if len(orders) != 0:
        for order in orders:
            #提取书籍信息
            dbinstance = Z.searchBookInstance(optid=order['bookid'])
            if dbinstance['status'] != 'success':
                continue
            dbkind = Z.searchBookInfo(dbinstance['data']['isbn'])
            if dbkind['status'] != 'success':
                continue
            #提取书籍副本数量
            dbbooks = Z.searchBookInstance(isbn=dbinstance['data']['isbn'])
            books = dbbooks['data']['uuids']
            counts = 0
            for book in books:
                if book['status'] == 'a---':
                    counts += 1
            #提取借书日期
            dboper = Z.searchOperation(order['bookid'])
            if dboper['status'] != 'success':
                continue
            borrowDate = str(dboper['date'][-1])
            #提取用户信息
            dbuser = Z.getUserInfo(order['userid'])
            if dbuser['status'] != 'success':
                continue
            #计算其他信息
            now = str(datetime.datetime.now())
            overdays = tools.getMinus(now,borrow)
            #构建订单信息
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
    #构建返回值
    retinfo = {
        'status':'success',
        'data':{
            'orderList':orderlist
        }
    }

def getUserInfo(info):
    #在线状态查询
    retjohn = Z.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    #核实身份
    if retjohn['right'] == '2':
        return {
            'status':'failure',
            'errorInfo':'Admin do not have a INfo Page!',
            'tokendate':retjohn['tokenDate']
        }
    #查询用户基本信息
    dbuser = Z.getUserInfo(retjohn['uuid'])
    if dbuser['status'] != 'success':
        dbuser['tokendate'] = retjohn['tokenDate']
        return dbuser
    #查询订单基本信息
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
    #构建用户信息
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
    #在线状态查询
    retjohn = Z.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    #获取历史纪录
    dbhistory = Z.searchHistory(retjohn['uuid'])
    if dbhistory['status'] != 'success':
        dbhistory['toekndate'] = retjohn['toeknDate']
        return dbhistory
    historys = dbhistory['data']
    booklist = []
    for his in historys:
        #获取书籍基本信息
        isbn = his['bookid']
        dbkind = Z.searchBookInfo(isbn)
        if dbkind['status'] != 'success':
            continue
        #构建书籍信息
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
    #构建返回值
    retinfo = {
        'status':'success',
        'data':{
            'bookList':booklist
        },
        'tokendate':retjohn['tokenDate']
    }
    return retinfo
