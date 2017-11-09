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
        'data':{
            'username' : userinfo['username'],
            'image' : userinfo['image'],
            'usertype' : usertype
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
        # if tokendate != '':
            # retdb['tokendate'] = tokendate
        return retdb
    isbns = retdb['isbn']
    booklist,languages,roomsthemes = [],[],[]
    for isbn in isbns:
        #根据isbn获取书籍基本信息
        dbkind = getBookInfo(isbn)
        if dbkind['status'] != 'success':
            continue
        #获取筛选器数据
        languages.extend(dbkind['data']['language'])
        themes.extend(dbkind['data']['theme'])
        rooms.extend(dbkind['data']['position']['room'])
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
            'position':dbkind['data']['position'],
            'language':dbkind['data']['language'],
            'theme':dbkind['data']['theme'],
            'image':dbkind['data']['imgs'],
            'amount':counts
        }
        #加入列表
        booklist.append(book)
    #构建返回值
    retinfo = {
        'status':'success',
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
    tokendate,right = '',0
    if info.has_key('toekn')
        retjohn = J.searchOnJohn({'token':info['token']})
        if retjohn['status'] != 'success':
            return retjohn
        tokendate = retjohn['tokenDate']
        right = retjohn['right']
    #根据isbn查询书籍基本信息
    dbkind = getBookInfo(info['isbn'])
    if dbkind['status'] != 'success':
        # if tokendate != '':
            # dbkind['tokendate'] = retjohn['tokenDate']
        return dbkind
    #构建书籍信息
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
            if right == 2:
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
    if info.has_key('token')
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
    
def getImage(route):
    dbimg = Z.searchImg(route)
    if dbimg['status'] != 'success':
        return dbimg
    return {
        'data':{
            'binarydata':'',
            'MIME':''
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
            'errorInfo':'Admin do not have a Info Page!',
            'tokendate':retjohn['tokenDate']
        }
    #查询用户基本信息
    dbuser = Z.getUserInfo(retjohn['uuid'])
    if dbuser['status'] != 'success':
        # dbuser['tokendate'] = retjohn['tokenDate']
        return dbuser
    #查询订单基本信息
    dborder = Z.searchOrder(userid=retjohn['uuid'],status='---o-')
    if dborder['status'] != 'success':
        # dborder['tokendate'] = retjohn['tokenDate']
        return dborder
    orders = dborder['data']
    overdays = 0
    if len(orders) != 0:
        for order in orders:
            optid = order['bookid']
            borrowdate = str(order['timestamp'])
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
    return {
        'status':'success',
        'tokendate':retjohn['tokenDate'],
        'data':{
            'userInfo':userinfo
        }
    }
    
    
def searchHistory(info):
    #在线状态查询
    retjohn = Z.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    #获取历史纪录
    dbhistory = Z.searchHistory(retjohn['uuid'])
    if dbhistory['status'] != 'success':
        # dbhistory['toekndate'] = retjohn['toeknDate']
        return dbhistory
    historys = dbhistory['data']
    booklist = []
    for his in historys:
        #获取书籍基本信息
        isbn = his['bookid']
        dbkind = getBookInfo(isbn)
        if dbkind['status'] != 'success':
            continue
        #构建书籍信息
        bookinfo = {
            'name':dbkind['data']['name'],
            'ISBN':dbkind['data']['isbn'],
            'position':dbkind['data']['position'],
            'theme':dbkind['data']['theme'],
            'language':dbkind['data']['language'],
            'image':dbkind['data']['imgs']
        }
        booklist.append(bookinfo)
    #构建返回值
    retinfo = {
        'status':'success',
        'data':{
            'bookList':booklist
        }
        'tokendate':retjohn['tokenDate']
    }
    return retinfo
    
def signup(info):
    newUser = info['newUser']
    #身份核实
    retjohn = J.searchOnJohn({'token':info['token'})
    if retjohn['status'] != 'success':
        return retjohn
    if retjohn['right'] != 2:
        return {
            'status':'failure',
            'errorInfo':'You don not have this right!'
        }
    #查询不可重复信息是否重复
    fordb = {
        'type':'tel',
        'value':newUser['tel']
    }
    telid = Z.getUserUUID(fordb)
    if telid['status'] == 'success':
        retInfo['status'] = 'failure'
        retInfo['errorInfo'] = 'This tel has been registered!'
    else:
        fordb = {
            'type':'stuid',
            'value':newUser['studentID']
        }
        nameid = Z.getUserUUID(fordb)
        if nameid['status'] == 'success':
            retInfo['status'] = 'failure'
            retInfo['errorInfo'] = 'This username has been registered!'
        else:
            #注册
            fordb = {
                'password':newUser['password'],
                'tel':newUser['tel'],
                'username':newUser['username']
                'balance':newUser['balance'],
                'plege':newUser['deposit'],
                'stu_id':newUser['studentID']
            }
            retdb = Z.addUser(fordb)
            retInfo = retdb
            retInfo['tokendate'] = retjohn['tokenDate']
    return retInfo
    
def searchUserInfoAdmin(info):
    #身份核实
    retjohn = Z.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    if retjohn['right'] != 2:
        return {
            'status':'failure',
            'errorInfo':'You don not have this right!'
        }
    #学生身份核实
    if info.has_key('stuid'):
        dbuser = Z.getUserUUID({'type':'stuid','value':info['stuid']})
    else:
        dbuser = Z.getUserUUID({'type':'tel','value':info['tel']})
    if dbuser['status'] != 'success':
        return dbuser
    #查询学生信息
    userid = dbuser['uuid']
    dbuser = Z.getUserInfo(userid)
    if dbuser['status'] != 'success':
        return dbuser
    #构建返回值
    retinfo = {
        'status':'success',
        'tokendate':retjohn['tokenDate'],
        'data':{
            'userInfo':{
                "userName": dbuser['data']['username'],
                "uuid": dbuser['data']['uuid'],
                "studentID": dbuser['data']['stuid'],
                "tel": dbuser['data']['tel'],
                "balance": dbuser['data']['balance'],
                "userImage": dbuser['data']['logo']
            }
        }
    }
    return retinfo
    
def editUserInfo(info):
    #身份核实
    retjohn = Z.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    if retjohn['right'] != 2:
        return {
            'status':'failure',
            'errorInfo':'You don not have this right!'
        }
    #修改余额
    dbuser = Z.modifyUserBalance({'uuid':info['uuid'],'balance':info['balance']})
    if dbuser['status'] != 'success':
        return dbuser
    #判断是否修改密码
    if info['password'] != '':
        dbuser = Z.modifyUserPWD({'uuid':info['uuid'],'password':info['password']})
        if dbuser['status'] != 'success':
            return dbuser
    #构建返回值
    retinfo = {
        'status':'success',
        'tokendate':retjohn['tokenDate']
    }
    return retinfo
   
# def addBook(info):
    # retjohn = Z.searchOnJohn({'token':info['token']})
    # if retjohn['status'] != 'success':
        # return retjohn
    # if retjohn['right'] != 2:
        # return {
            # 'status':'failure',
            # 'errorInfo':'You don not have this right!'
        # }
    # img = info['bookinfo'].pop('image')
    
def addBookCopy(info):
    block = {
        'info':info,
        'type':'add'
    }
    return modifyBookCopy(block)

def deleteBookCopy(info):
    block = {
        'info':info,
        'type':'delete'
    }
    return modifyBookCopy(block)

def editBookCopy(info):
    block = {
        'info':info,
        'type':'edit'
    }
    return modifyBookCopy(block)

def modifyBookCopy(info):
    # info :{
        # 'info':info,
        # 'type':'add'
    # }
    #身份核实
    retjohn = Z.searchOnJohn({'token':info['info']['token']})
    if retjohn['status'] != 'success':
        return retjohn
    if retjohn['right'] != 2:
        return {
            'status':'failure',
            'errorInfo':'You don not have this right!'
        }
    #根据类型进行操作
    if info['type'] == 'add':
        #添加
        dbkind = Z.addBookInstance(info['info']['ISBN'])
    elif info['type'] == 'delete':
        #删除
        dbkind = Z.deleteBookInstance(info['info']['uuid'])
    elif info['type'] == 'edit':
        #修改副本状态
        dbinstance = Z.searchBookInstance(info['info']['uuid'])
        if dbinstance['status'] != 'success':
            return dbinstance
        if dbinstance['data']['uuids'][0]['status'] == '--b-':
            return {
                'status':'failure',
                'errorInfo':'Even you are an admin,you can not change the status of a borrowed book!'
            }
        dbkind = Z.modifyBookInstance({'uuid':info['info']['uuid'],'status':info['info']['status']})
    else:
        return {
            'status':'failure',
            'errorInfo':'which action do you want to do on a bookcopy?'
        }
    if dbkind['status'] != 'success':
        # dbkind['tokendate'] = retjohn['tokenDate']
        return dbkind
    #构建返回值
    retinfo = {
        'status':'success',
        'tokendate':retjohn['tokenDate']
    }
    if info['type'] == 'add':
        retinfo['data'] = {'uuid':dbkind['uuid']}
    return retinfo

def apply(info):
    #获取在线状态
    retjohn = Z.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    #添加申请订单
    dborder = Z.addOrder({'userid':retjohn['uuid'],'bookid':info['uuid'],'status':'a----'})
    if dborder['status'] != 'success':
        # dborder['tokendate'] = retjohn['tokenDate']
        return dborder
    retinfo = {
        'status':'success',
        'tokendate':retjohn['tokenDate']
    }
    return retinfo
    
def agreeBorrow(info):
    block = {
        'info':info,
        'type':'agree'
    }
    return actionOfBook(block)
    
def refuseBorrow(info):
    block = {
        'info':info,
        'type':'refuse'
    }
    return actionOfBook(block)
    
def returnBook(info):
    block = {
        'info':info,
        'type':'return'
    }
    return actionOfBook(block)
    
def actionOfBook(info):
    # info : {
        # 'info':
        # 'type':'agree'
    # }
    retjohn = Z.searchOnJohn({'token':info['info']['token']})
    if retjohn['status'] != 'success':
        return retjohn
    if retjohn['right'] != 2:
        return {
            'status':'failure',
            'errorInfo':'You don not have this right!'
        }
    if info['type'] == 'refuse':
        dborder = Z.modifyOrderStatus({'uuid':info['info']['uuid'],'status':'----i'})
    elif info['type'] == 'agree':
        #获取订单中的bookid
        dborder = Z.searchOrder(orderid=info['info']['uuid'])
        if dborder['status'] != 'success':
            return dborder
        bookid = dborder['data'][0]['bookid']
        #修改book状态
        dbinstance = Z.modifyBookInstance({'uuid':bookid,'status':'--b-'})
        if dbinstance['status'] != 'success':
            return dbinstance
        #生成同一状态的操作表
        operdata = {
            'date':[str(datetime.datetime.now())],
            'status':'--b-'
        }
        dboper = Z.addOperation(operdata)
        if dboper['status'] != 'success':
            return dboper
        #在book中添加操作表
        dbinstance = Z.modifyBookInstance({'uuid':bookid,'optid':dboper['uuid']})
        if dbinstance['status'] != 'success':
            return dbinstance
        #修改订单状态
        dborder = Z.modifyOrderStatus({'uuid':info['info']['uuid'],'status':'-b---'})
    elif info['type'] == 'return':
        #获取订单中的userid,bookid
        dborder = Z.searchOrder(orderid=info['info']['uuid'])
        if dborder['status'] != 'success':
            return dborder
        userid = dborder['data'][0]['userid']
        bookid = dborder['data'][0]['bookid']
        #修改book状态
        dbinstance = Z.modifyBookInstance({'uuid':bookid,'status':'a---'})
        if dbinstance['status'] != 'success':
            return dbinstance
        dbinstance = Z.modifyBookInstance({'uuid':bookid,'optid':None})
        if dbinstance['status'] != 'success':
            return dbinstance
        #修改最新余额
        dbuser = Z.modifyUserBalance({'uuid':userid,'balance':info['info']['balance']})
        if dbuser['status'] != 'success':
            return dbuser
        dborder = Z.modifyOrderStatus({'uuid':info['uuid'],'status':'--f--'})
    else:
        return {
            'status':'failure',
            'errorInfo':'Unexpect order operation!'
        }
    if dborder['status'] != 'success':
        # dborder['tokendate'] = retjohn['tokenDate']
        return dborder
    retinfo = {
        'status':'success',
        'tokendate':retjohn['tokenDate']
    }
    return retinfo

def checkBorrow(info):
    block = {
        'info':info,
        'type':'borrow'
    }
    return checkAction(block)
    
def checkReturn(info):
    block = {
        'info':info,
        'type':'return'
    }
    return checkAction(block)
  
  
def checkAction(info):
    # info : {
        # 'info':
        # 'type':'borrow'
    # }
    #身份核实
    retjohn = Z.searchOnJohn({'token':info['info']['token']})
    if retjohn['status'] != 'success':
        return retjohn
    if retjohn['right'] != 2:
        return {
            'status':'failure',
            'errorInfo':'You don not have this right!'
        }
    #用户提取
    stuid = info['info']['studentID']
    dbuser = Z.getUserUUID({'type':'stuid','value':stuid})
    if dbuser['status'] != 'success':
        return dbuser
    #订单查询
    if info['type'] == 'borrow':
        dborder = orderList({'userid':dbuser['uuid'],'right':'1','status':'a----'})
        if dborder['status'] != 'success':
            orderList = []
        else:
            orderList = dborder['orderList']
    elif info['type'] == 'return':  
        dborder = orderList({'userid':dbuser['uuid'],'right':'1','status':'-b---'})
        if dborder['status'] != 'success':
            orderlistB = []
        else:
            orderlistB = dborder['orderList']
            for i in orderlistB:
                i.pop('timeLeft')
                i['fine'] = 0
                delta = (datetime.datetime.now() - datetime.datetime.strptime(i['borrowDate'],'%Y-%m-%d %H:%M:%S.%f'))
                i['days'] = delta.days
        dborder = orderList({'userid':dbuser['uuid'],'right':'1','status':'---o-'})
        if dborder['status'] != 'success':
            orderlistO = []
        else:
            orderlistO = dborder['orderList']
            for i in orderlistO:
                i.pop('overDays')
                delta = datetime.datetime.now() - datetime.datetime.strptime(i['borrowDate'],'%Y-%m-%d %H:%M:%S.%f')
                i['days'] = delta.days
                deltaF = delta - datetime.timedelta(days=30)
                i['fine'] = deltaF.days * 1
        orderList = orderlistB.extend(orderlistO)
    target = []
    for one in orderList:
        if one['bookid'] in info['info']['uuids']
        target.append(one)
     
    retinfo = {
        "status":"success",
        "tokendate":retjohn['tokenDate'],
        "data": {
            'orderList':target
        }
    }
    return retinfo
    
def orderList(info):
    # info :{
        # 'userid':
        # 'right':
        # 'status':
    # }
    
    if info['right'] == 1:
        dborder = Z.searchOrder(userid=info['userid'],status=info['status'])
    else:
        dborder = Z.searchOrder(status=info['status'])
    orderids = []
    orderlist = []
    for one in dborder['data']:
        orders.append(one['orderid'])
    if len(orders) != 0:
        for id in orders:
            _orderinfo = searchOrderInfo(id)
            if _orderinfo['status'] != 'success':
                continue
            if _orderinfo['orderstatus'] != info['status']:
                continue
            orderinfo = {
                #_orderinfo[""]
                "orderid": _orderinfo["orderid"],
                "applyDate": _orderinfo["initdate"],
                "ISBN": _orderinfo["isbn"],
                "bookName": _orderinfo["bookname"],
                "image": _orderinfo["image"],
                "auth": _orderinfo["auth"],
                "position": _orderinfo["position"],
                "bookid":_orderinfo["bookid"],
                "amount": _orderinfo["amount"],
                "userid": _orderinfo["userid"],
                "userName": _orderinfo["userName"],
                "balance": _orderinfo["balance"]
            }
            if info['status'] == 'a----':
                orderinfo['applyTime'] = _orderinfo["initdate"].split(' ')[1]
            elif info['status'] == '-b---':
                orderinfo['borrowDate'] = _orderinfo["initdate"]
                b = datetime.datetime.strptime(_orderinfo["initdate"],'%Y-%m-%d %H:%M:%S.%f')
                limit = datetime.timedelta(days=30)
                delta = b + limit - datetime.datetime.now()
                orderinfo['timeLeft'] = delta.days
            elif info['status'] == '---o-':
                orderinfo['borrowDate'] = _orderinfo["initdate"]
                b = datetime.datetime.strptime(_orderinfo["initdate"],'%Y-%m-%d %H:%M:%S.%f')
                limit = datetime.timedelta(days=30)
                delta = datetime.datetime.now() - b - limit 
                orderinfo['overDays'] = delta.days
                orderinfo['fine'] = delta.days * 1
            elif info['status'] == '--f--':
                pass
                #here
            elif info['status'] == '----i':
                orderinfo['invalidDate'] = _orderinfo["initdate"]
            else:
                pass
            orderlist.append(orderinfo)
    retinfo = {
        'status':'success',
        'orderList':orderlist
    }
    return retinfo

def applyList(info):
    retjohn = Z.searchOnJohn({'token':info['info']['token']})
    if retjohn['status'] != 'success':
        return retjohn
    block = {
        'userid':retjohn['uuid'],
        'right':retjohn['right'],
        'status':'a----'
    }
    retinfo = orderList(block)
    retinfo['tokendate'] = retjohn['tokenDate']
    return retinfo
    
def returnList(info):
    retjohn = Z.searchOnJohn({'token':info['info']['token']})
    if retjohn['status'] != 'success':
        return retjohn
    block = {
        'userid':retjohn['uuid'],
        'right':retjohn['right'],
        'status':'a----'
    }
    retinfo = orderList(block)
    retinfo['tokendate'] = retjohn['tokenDate']
    return retinfo
    
def borrowList(info):
    retjohn = Z.searchOnJohn({'token':info['info']['token']})
    if retjohn['status'] != 'success':
        return retjohn
    block = {
        'userid':retjohn['uuid'],
        'right':retjohn['right'],
        'status':'-b---'
    }
    retinfo = orderList(block)
    retinfo['tokendate'] = retjohn['tokenDate']
    return retinfo
    
def overdueList(info):
    retjohn = Z.searchOnJohn({'token':info['info']['token']})
    if retjohn['status'] != 'success':
        return retjohn
    block = {
        'userid':retjohn['uuid'],
        'right':retjohn['right'],
        'status':'---o-'
    }
    retinfo = orderList(block)
    retinfo['tokendate'] = retjohn['tokenDate']
    return retinfo
    
def finishedList(info):
    retjohn = Z.searchOnJohn({'token':info['info']['token']})
    if retjohn['status'] != 'success':
        return retjohn
    block = {
        'userid':retjohn['uuid'],
        'right':retjohn['right'],
        'status':'--f--'
    }
    retinfo = orderList(block)
    retinfo['tokendate'] = retjohn['tokenDate']
    return retinfo

def invalidList(info):
    retjohn = Z.searchOnJohn({'token':info['info']['token']})
    if retjohn['status'] != 'success':
        return retjohn
    block = {
        'userid':retjohn['uuid'],
        'right':retjohn['right'],
        'status':'----i'
    }
    retinfo = orderList(block)
    retinfo['tokendate'] = retjohn['tokenDate']
    return retinfo
    
def searchOrderInfo(orderid):
    dborder = Z.searchOrder(orderid=orderid)
    if dborder['status'] != 'success':
        return dborder
    orderinfo = dborder['data'][0]
    orderdate = orderinfo['timestamp']
    # need calculation to modify order status
    now = str(datetime.datetime.now())
    result = tools.getMinus(now,orderdate)
    if orderinfo['status'] == 'a----':
        if result.seconds > 1800:
            orderstatus = '----i'
        orderstatus = orderinfo['status']
    if orderinfo['status'] == '-b---':
        if result.days > 30:
            orderstatus = '--o--'
        orderstatus = orderinfo['status']
    bookid = orderinfo['bookid']
    userid = orderinfo['userid']
    dboper = Z.searchOperation(optid)
    if dboper['status'] != 'success':
        return dboper
    dbinstance = Z.searchBookInstance(uuid=bookid)
    if dbinstance['status'] != 'success':
        return dbinstance
    isbn = dbinstance['data']['isbn']
    optid = dbinstance['data']['uuids'][0]['optid']
    bookstatus = dbinstance['data']['uuids'][0]['status']
    dbuser = Z.getUserInfo(userid)
    if dbuser['status'] != 'success':
        return dbuser
    dbkind = getBookInfo(isbn)
    if dbkind['status'] != 'success':
        return dbkind
    dbinstance = Z.searchBookInstance(isbn=isbn)
    if dbinstance['status'] != 'success':
        return dbinstance
    books = dbinstance['data']['uuids']
    copys = []
    for book in books:
        copys.append({'uuid':book['uuid'],'status':book['status']})
    retinfo = {
        'status':'success',
        'orderid':info['uuid'],
        'initdate':orderdate,
        'orderstatus':orderstatus,
        'userid':userid,
        'bookoptid':optid,
        'bookid':bookid,
        'bookstatus':bookstatus,
        'bookoperdate':str(dboper['date']),
        'isbn':isbn,
        'bookname':dbkind['data']['name'],
        'auth':dbkind['data']['auth'],
        'version':dbkind['data']['edition'],
        'publisher':dbkind['data']['publisher'],
        'language':dbkind['data']['language'],
        'theme':dbkind['data']['theme'],
        'CLC':dbkind['data']['lc'],
        'image':dbkind['data']['imgs'],
        'description':dbkind['data']['abstract'],
        'position':dbkind['data']['position'],
        'amount':len(copys),
        'copys':copys,
        'userid':userid,
        'userName':dbuser['data']['usename'],
        'balance':dbuser['data']['balance']
    }
    return retinfo
    
def getBookInfo(isbn):
    dbkind = Z.searchBookInfo(isbn)
    if dbkind['status'] != 'success':
        return dbkind
    position = tools.divideLocation(Z.searchLocation(dbkind['data']['lc']))
    tag = tools.divideTags(dbkind['data']['tags'])
    dbkind['data']['position'] = position
    dbkind['data']['language'] = tag['language']
    dbkind['data']['theme'] = tag['theme']
    return dbkind