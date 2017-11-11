# -*- coding:utf-8 -*-
'''
Created on 2017��11��1��

@author: lenovo
'''
from database import Database as Z
import John as J
import tools
import datetime

# finish
def login(info):
    fordb = {'type':info['type'],'value':info['value']}
    #��ѯ�û��Ƿ�������ݿ�
    retdb = Z.getUserUUID(fordb)
    if retdb['status'] != 'success':
        return retdb
    userid = retdb['uuid']
    #��һ����Ϊ�ų�ϵͳ����
    retdb = Z.getUserPWD(userid)
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
        'data':{
            'username' : userinfo['username'],
            'image' : userinfo['logo'],
            'usertype' : usertype
        }
    }
    return retinfo

# finish
def logout(info):
    retjohn = J.deleteOnJohn({'token':info['token']})
    return retjohn
    
# finish
def searchBook(info):
    tokendate = ''
    #����Ƿ����token
    if info.has_key('token'):
        retjohn = J.searchOnJohn({'token':info['token']})
        if retjohn['status'] != 'success':
            return retjohn
        tokendate = retjohn['tokenDate']
    #��ȡISBN
    retdb = Z.searchISBN({'type':info['type'],'value':info['value']})
    if retdb['status'] != 'success':
        # if tokendate != '':
            # retdb['tokendate'] = tokendate
        return retdb
    isbns = retdb['isbn']
    booklist,languages,rooms,themes = [],[],[],[]
    for isbn in isbns:
        #����isbn��ȡ�鼮������Ϣ
        dbkind = getBookInfo(isbn)
        if dbkind['status'] != 'success':
            continue
        #��ȡɸѡ������
        # print dbkind
        # print '---------------------'
        roomTemp = dbkind['data']['position']['room']
        languages.extend(dbkind['data']['language'])
        themes.extend(dbkind['data']['theme'])
        rooms.extend([roomTemp])
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
            'position':dbkind['data']['position'],
            'language':dbkind['data']['language'],
            'theme':dbkind['data']['theme'],
            'image':dbkind['data']['imgs'],
            'amount':counts
        }
        #�����б�
        booklist.append(book)
    #��������ֵ
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
    
# finish
def searchBookByISBN(info):
    #��ѯtoken,�ж��û�����״̬��֮���ʹ�÷���ֵ�е�right
    tokendate,right = '',0
    if info.has_key('token'):
        retjohn = J.searchOnJohn({'token':info['token']})
        if retjohn['status'] != 'success':
            return retjohn
        tokendate = retjohn['tokenDate']
        right = retjohn['right']
        Z.addHistory({'userid':retjohn['uuid'],'bookid':info['ISBN']})
    #����isbn��ѯ�鼮������Ϣ
    dbkind = getBookInfo(info['ISBN'])
    if dbkind['status'] != 'success':
        # if tokendate != '':
            # dbkind['tokendate'] = retjohn['tokenDate']
        return dbkind
    #�����鼮��Ϣ
    bookinfo = {
        'name':dbkind['data']['name'],
        'auth':dbkind['data']['auth'],
        'version':dbkind['data']['edition'],
        'ISBN':dbkind['data']['isbn'],
        'publisher':dbkind['data']['publisher'],
        'CLC':dbkind['data']['lc'],
        'image':dbkind['data']['imgs'],
        'description':dbkind['data']['abstract'],
        'position':dbkind['data']['position'],
        'language':dbkind['data']['language'],
        'theme':dbkind['data']['theme'],
    }
    #����isbn��ѯ������Ϣ������right��bookinfo�������Ӧ��Ϣ
    counts = 0
    dbinstance = Z.searchBookInstance(isbn=info['ISBN'])
    if dbinstance['status'] != 'success':
        bookinfo['amount'] = counts
        bookinfo['copys'] = []
    else:
        books = dbinstance['data']['uuids']
        copys = []
        # print books,'in test'
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

# finish
def searchUserInfo(info):
    #����״̬��ѯ
    retjohn = J.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    #��ʵ���
    if retjohn['right'] == 2:
        return {
            'status':'failure',
            'errorInfo':'Admin do not have a Info Page!',
            'tokendate':retjohn['tokenDate']
        }
    #��ѯ�û�������Ϣ
    dbuser = Z.getUserInfo(retjohn['uuid'])
    if dbuser['status'] != 'success':
        return dbuser
    #��ѯ����������Ϣ
    dborder = Z.searchOrder(userid=retjohn['uuid'],status='---o-')
    orders = dborder['data']
    overdays = 0
    if len(orders) != 0:
        for order in orders:
            borrowdate = str(order['timestamp'])
            now = str(datetime.datetime.now())
            overdays += tools.getMinus(now,borrowdate)
    #�����û���Ϣ
    userinfo = {
        'userName':dbuser['data']['username'],
        'uuid':dbuser['data']['uuid'],
        'studentID':str(dbuser['data']['stuid']),
        'tel':str(dbuser['data']['tel']),
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
   
# finish   
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
   
# finish
def searchHistory(info):
    #����״̬��ѯ
    retjohn = J.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    #��ȡ��ʷ��¼
    dbhistory = Z.searchHistory(retjohn['uuid'])
    if dbhistory['status'] != 'success':
        # dbhistory['toekndate'] = retjohn['toeknDate']
        return dbhistory
    historys = dbhistory['date']
    booklist = []
    for his in historys:
        #��ȡ�鼮������Ϣ
        isbn = his['bookid']
        dbkind = getBookInfo(isbn)
        if dbkind['status'] != 'success':
            continue
        #�����鼮��Ϣ
        bookinfo = {
            'name':dbkind['data']['name'],
            'ISBN':dbkind['data']['isbn'],
            'position':dbkind['data']['position'],
            'theme':dbkind['data']['theme'],
            'language':dbkind['data']['language'],
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
    
# finish
def signup(info):
    newUser = info['newUser']
    #��ݺ�ʵ
    retjohn = J.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    if retjohn['right'] != 2:
        return {
            'status':'failure',
            'errorInfo':'You don not have this right!'
        }
    #��ѯ�����ظ���Ϣ�Ƿ��ظ�
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
            #ע��
            fordb = {
                'password':newUser['password'],
                'tel':newUser['tel'],
                'username':newUser['userName'],
                'balance':newUser['balance'],
                'pledge':newUser['deposit'],
                'stu_id':newUser['studentID']
            }
            retdb = Z.addUser(fordb)
            retInfo = retdb
            retInfo['tokendate'] = retjohn['tokenDate']
    return retInfo
    
# finish
def searchUserInfoAdmin(info):
    #��ݺ�ʵ
    retjohn = J.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    if retjohn['right'] != 2:
        return {
            'status':'failure',
            'errorInfo':'You don not have this right!'
        }
    #ѧ����ݺ�ʵ
    if info.has_key('stuid'):
        dbuser = Z.getUserUUID({'type':'stuid','value':info['stuid']})
    else:
        dbuser = Z.getUserUUID({'type':'tel','value':info['tel']})
    if dbuser['status'] != 'success':
        return dbuser
    #��ѯѧ����Ϣ
    userid = dbuser['uuid']
    dbuser = Z.getUserInfo(userid)
    if dbuser['status'] != 'success':
        return dbuser
    #��������ֵ
    retinfo = {
        'status':'success',
        'tokendate':retjohn['tokenDate'],
        'data':{
            'userInfo':{
                "userName": dbuser['data']['username'],
                "uuid": dbuser['data']['uuid'],
                "studentID": str(dbuser['data']['stuid']),
                "tel": str(dbuser['data']['tel']),
                "balance": dbuser['data']['balance'],
                "userImage": dbuser['data']['logo']
            }
        }
    }
    return retinfo
    
# finish
def editUserInfo(info):
    #��ݺ�ʵ
    retjohn = J.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    if retjohn['right'] != 2:
        return {
            'status':'failure',
            'errorInfo':'You don not have this right!'
        }
    #�޸����
    dbuser = Z.modifyUserBalance({'uuid':info['uuid'],'balance':info['balance']})
    if dbuser['status'] != 'success':
        return dbuser
    #�ж��Ƿ��޸�����
    if info['password'] != '':
        dbuser = Z.modifyUserPWD({'uuid':info['uuid'],'password':info['password']})
        if dbuser['status'] != 'success':
            return dbuser
    #��������ֵ
    retinfo = {
        'status':'success',
        'tokendate':retjohn['tokenDate']
    }
    return retinfo
   
# finish
def addBook(info):
    retjohn = J.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    if retjohn['right'] != 2:
        return {
            'status':'failure',
            'errorInfo':'You don not have this right!'
        }
    tags = []
    tags.extend(info['bookInfo']['language'])
    tags.extend(info['bookInfo']['theme'])
    print tags,'in test'
    fordb = {
        'isbn' : info['bookInfo']['ISBN'],
        'lc' : info['bookInfo']['CLC'],
        'name' : info['bookInfo']['name'],
        'auth' : info['bookInfo']['auth'],
        'publisher' : info['bookInfo']['publisher'],
        'edition' : info['bookInfo']['version'],
        'imgs' : info['bookInfo']['image'],
        'tags' : tags,
        'abstract' : info['bookInfo']['description']
    }
    dbkind = Z.addBookInfo(fordb)
    if dbkind['status'] != 'success':
        return dbkind
    dblocation = Z.searchLocation(info['bookInfo']['CLC'])
    if dblocation['status'] != 'success':
        return dblocation
    position = tools.divideLocation(dblocation['location'])
    copys = []
    for i in range(int(info['bookInfo']['amount'])):
        dbinstance = Z.addBookInstance(info['bookInfo']['ISBN'])
        if dbinstance['status'] != 'success':
            continue
        copys.append({'uuid':dbinstance['uuid'],'status':'Available'})
    retinfo = {
        'status':'status',
        'toekndate':retjohn['tokenDate'],
        'data':{
            'bookInfo':info['bookInfo']
        }
    }
    retinfo['data']['bookInfo']['amount'] = len(copys)
    retinfo['data']['bookInfo']['copys'] = copys
    retinfo['data']['bookInfo']['position'] = position
    return retinfo

# finish    
def addBookCopy(info):
    block = {
        'info':info,
        'type':'add'
    }
    return modifyBookCopy(block)
# �鲻���ȼ��ڳɹ�
# finish
def deleteBookCopy(info):
    block = {
        'info':info,
        'type':'delete'
    }
    return modifyBookCopy(block)

# finish
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
    #��ݺ�ʵ
    retjohn = J.searchOnJohn({'token':info['info']['token']})
    if retjohn['status'] != 'success':
        return retjohn
    if retjohn['right'] != 2:
        return {
            'status':'failure',
            'errorInfo':'You don not have this right!'
        }
    #�������ͽ��в���
    if info['type'] == 'add':
        #���
        dbkind = Z.addBookInstance(info['info']['ISBN'])
    elif info['type'] == 'delete':
        #ɾ��
        dbkind = Z.deleteBookInstance(info['info']['uuid'])
    elif info['type'] == 'edit':
        #�޸ĸ���״̬
        dbinstance = Z.searchBookInstance(uuid=info['info']['uuid'])
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
    #��������ֵ
    retinfo = {
        'status':'success',
        'tokendate':retjohn['tokenDate']
    }
    if info['type'] == 'add':
        retinfo['data'] = {'uuid':dbkind['uuid']}
    return retinfo

#finish
def apply(info):
    #��ȡ����״̬
    retjohn = J.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    if retjohn['right'] == 2:
        return {
            'status':'failure',
            'errorInfo':'Sorry ,Admin don not have this right!'
        }
    #��ѯ���û����ж�����
    dborder = Z.searchOrder(userid=retjohn['uuid'])
    counts = 0
    for one in dborder['data']:
        if one['status'] == 'a----':
            counts += 1
        elif one['status'] == '-b---':
            counts += 1
        elif one['status'] == '---o-':
            counts += 1
        else:
            pass
    if counts > 1:
        return {
            'status':'failure',
            'errorInfo':'Sorry ,You can only apply less than two Books!'
        }
    #��ѯ�����Ƿ��ѱ����
    dbinstance = Z.searchBookInstance(uuid=info['uuid'])
    if dbinstance['status'] != 'success':
        return dbinstance
    if dbinstance['data']['uuids'][0]['status'] != 'a---':
        return {
            'status': 'failure',
            'errorInfo': 'This book do not allow to borrow!'
        }
    #��ѯ�����Ƿ��ѱ�����
    dborder = Z.searchOrder(bookid=info['uuid'],status='a----')
    if len(dborder['data']) > 0:
        return {
            'status':'failure',
            'errorInfo':'Sorry ,This book has been applied!'
        }
    #������붩��
    dborder = Z.addOrder({'userid':retjohn['uuid'],'bookid':info['uuid'],'status':'a----'})
    if dborder['status'] != 'success':
        return dborder
    retinfo = {
        'status':'success',
        'tokendate':retjohn['tokenDate']
    }
    return retinfo
  
# finish  
def agreeBorrow(info):
    block = {
        'info':info,
        'type':'agree'
    }
    return actionOfBook(block)
    
# finish
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
    retjohn = J.searchOnJohn({'token':info['info']['token']})
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
        #��ȡ�����е�bookid
        dborder = Z.searchOrder(orderid=info['info']['uuid'])
        if len(dborder['data']) == 0:
            return {
                'status':'failure',
                'errorInfo':'System error in Order!Can not find this order!'
            }
        bookid = dborder['data'][0]['bookid']
        #�޸�book״̬
        dbinstance = Z.modifyBookInstance({'uuid':bookid,'status':'--b-'})
        if dbinstance['status'] != 'success':
            return dbinstance
        #����ͬһ״̬�Ĳ�����
        operdata = {
            'date':[str(datetime.datetime.now())],
            'status':'--b-'
        }
        dboper = Z.addOperation(operdata)
        if dboper['status'] != 'success':
            return dboper
        #��book����Ӳ�����
        dbinstance = Z.modifyBookInstance({'uuid':bookid,'optid':dboper['uuid']})
        if dbinstance['status'] != 'success':
            return dbinstance
        #�ڶ�������Ӳ�����
        dborder = Z.modifyOrderOptid({'uuid':info['info']['uuid'],'optid':dboper['uuid']})
        if dborder['status'] != 'success':
            return dborder
        #�޸Ķ���״̬
        dborder = Z.modifyOrderStatus({'uuid':info['info']['uuid'],'status':'-b---'})
    elif info['type'] == 'return':
        #��ȡ�����е�userid,bookid
        dborder = Z.searchOrder(orderid=info['info']['uuid'])
        if len(dborder['data']) == 0:
            return {
                'status':'failure',
                'errorInfo':'System error in Order!Can not find this order!'
            }
        userid = dborder['data'][0]['userid']
        bookid = dborder['data'][0]['bookid']
        optid = dborder['data'][0]['optid']
        #�޸�book״̬
        dbinstance = Z.modifyBookInstance({'uuid':bookid,'status':'a---'})
        if dbinstance['status'] != 'success':
            return dbinstance
        dbinstance = Z.modifyBookInstance({'uuid':bookid,'optid':None})
        if dbinstance['status'] != 'success':
            return dbinstance
        #�޸�bookopt״̬
        dboper = Z.modifyOperationDate({'uuid':optid,'date':[str(datetime.datetime.now())]})
        if dboper['status'] != 'success':
            return dboper
        dboper = Z.modifyOperationStatus({'uuid':optid,'status':'---r'})
        if dboper['status'] != 'success':
            return dboper
        #�޸��������
        dbuser = Z.modifyUserBalance({'uuid':userid,'balance':info['info']['balance']})
        if dbuser['status'] != 'success':
            return dbuser
        dborder = Z.modifyOrderStatus({'uuid':info['info']['uuid'],'status':'--f--'})
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

# finish
def checkBorrow(info):
    block = {
        'info':info,
        'type':'borrow'
    }
    return checkAction(block)
    
#finish
def checkReturn(info):
    block = {
        'info':info,
        'type':'return'
    }
    return checkAction(block)
  
# finish 
def checkAction(info):
    # info : {
        # 'info':
        # 'type':'borrow'
    # }
    #��ݺ�ʵ
    retjohn = J.searchOnJohn({'token':info['info']['token']})
    if retjohn['status'] != 'success':
        return retjohn
    if retjohn['right'] != 2:
        return {
            'status':'failure',
            'errorInfo':'You don not have this right!'
        }
    #�û���ȡ
    stuid = info['info']['studentID']
    dbuser = Z.getUserUUID({'type':'stuid','value':stuid})
    if dbuser['status'] != 'success':
        return dbuser
    #������ѯ
    orderList = []
    if info['type'] == 'borrow':
        dborder = getOrderList({'userid':dbuser['uuid'],'right':1,'status':'a----'})
        if dborder['status'] != 'success':
            orderList = []
        else:
            orderList = dborder['orderList']
    elif info['type'] == 'return':  
        dborder = getOrderList({'userid':dbuser['uuid'],'right':1,'status':'-b---'})
        if dborder['status'] != 'success':
            orderlistB = []
        else:
            orderlistB = dborder['orderList']
            for i in orderlistB:
                i.pop('timeLeft')
                i['fine'] = 0
                delta = (datetime.datetime.now() - datetime.datetime.strptime(i['borrowDate'],'%Y-%m-%d'))
                i['days'] = delta.days
        orderList.extend(orderlistB)
        dborder = getOrderList({'userid':dbuser['uuid'],'right':1,'status':'---o-'})
        if dborder['status'] != 'success':
            orderlistO = []
        else:
            orderlistO = dborder['orderList']
            for i in orderlistO:
                i.pop('overDays')
                delta = datetime.datetime.now() - datetime.datetime.strptime(i['borrowDate'],'%Y-%m-%d')
                i['days'] = delta.days
                deltaF = delta - datetime.timedelta(days=30)
                i['fine'] = deltaF.days * 1
        orderList.extend(orderlistO)
    target = []
    for one in orderList:
        if one['bookid'] in info['info']['uuids']:
            target.append(one)
     
    retinfo = {
        "status":"success",
        "tokendate":retjohn['tokenDate'],
        "data": {
            'orderList':target
        }
    }
    return retinfo

# finish   
def getOrderList(info):
    # info :{
        # 'userid':
        # 'right':
        # 'status':
    # }
    
    if info['right'] == 1:
        dborder = Z.searchOrder(userid=info['userid'],status=info['status'])
    else:
        dborder = Z.searchOrder(status=info['status'])
    orders = []
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
                "applyDate": _orderinfo["initdate"].split(' ')[0],
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
                orderinfo['applyTime'] = _orderinfo["initdate"].split(' ')[1].split('.')[0]
            elif info['status'] == '-b---':
                orderinfo['borrowDate'] = _orderinfo["initdate"].split(' ')[0]
                b = datetime.datetime.strptime(_orderinfo["initdate"],'%Y-%m-%d %H:%M:%S.%f')
                limit = datetime.timedelta(days=30)
                delta = b + limit - datetime.datetime.now()
                orderinfo['timeLeft'] = delta.days
            elif info['status'] == '---o-':
                orderinfo['borrowDate'] = _orderinfo["initdate"].split(' ')[0]
                b = datetime.datetime.strptime(_orderinfo["initdate"],'%Y-%m-%d %H:%M:%S.%f')
                limit = datetime.timedelta(days=30)
                delta = datetime.datetime.now() - b - limit 
                orderinfo['overDays'] = delta.days
                orderinfo['fine'] = delta.days * 1
            elif info['status'] == '--f--':
                orderinfo['returnDate'] = _orderinfo["bookoperdate"]
                a = datetime.datetime.strptime(_orderinfo["initdate"],'%Y-%m-%d %H:%M:%S.%f')
                b = datetime.datetime.strptime(_orderinfo["bookoperdate"],'%Y-%m-%d %H:%M:%S.%f')
                delta = b - a
                orderinfo['holdDays'] = delta.days
            elif info['status'] == '----i':
                orderinfo['invalidDate'] = _orderinfo["initdate"].split(' ')[0]
            else:
                pass
            orderlist.append(orderinfo)
    retinfo = {
        'status':'success',
        'orderList':orderlist
    }
    return retinfo

# finish
def applyList(info):
    retjohn = J.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    block = {
        'userid':retjohn['uuid'],
        'right':retjohn['right'],
        'status':'a----'
    }
    retinfo = getOrderList(block)
    retinfo['tokendate'] = retjohn['tokenDate']
    return retinfo

# finish    
def borrowList(info):
    retjohn = J.searchOnJohn({'token':info['info']['token']})
    if retjohn['status'] != 'success':
        return retjohn
    block = {
        'userid':retjohn['uuid'],
        'right':retjohn['right'],
        'status':'-b---'
    }
    retinfo = getOrderList(block)
    retinfo['tokendate'] = retjohn['tokenDate']
    return retinfo

# finish   
def overdueList(info):
    retjohn = J.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    block = {
        'userid':retjohn['uuid'],
        'right':retjohn['right'],
        'status':'---o-'
    }
    retinfo = getOrderList(block)
    retinfo['tokendate'] = retjohn['tokenDate']
    return retinfo

# finish    
def finishedList(info):
    retjohn = J.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    block = {
        'userid':retjohn['uuid'],
        'right':retjohn['right'],
        'status':'--f--'
    }
    retinfo = getOrderList(block)
    retinfo['tokendate'] = retjohn['tokenDate']
    return retinfo

# finish
def invalidList(info):
    retjohn = J.searchOnJohn({'token':info['token']})
    if retjohn['status'] != 'success':
        return retjohn
    block = {
        'userid':retjohn['uuid'],
        'right':retjohn['right'],
        'status':'----i'
    }
    retinfo = getOrderList(block)
    retinfo['tokendate'] = retjohn['tokenDate']
    return retinfo
    
def searchOrderInfo(orderid):
    dborder = Z.searchOrder(orderid=orderid)
    if len(dborder['data']) == 0:
        return {
            'status':'failure',
            'errorInfo':'System error in Order!Can not find this order!'
        }
    orderinfo = dborder['data'][0]
    orderdate = str(orderinfo['timestamp'])
    bookid = orderinfo['bookid']
    optid = orderinfo['optid']
    userid = orderinfo['userid']
    orderstatus = orderinfo['status']
    # print orderinfo
    # need calculation to modify order status
    now = str(datetime.datetime.now())
    result = tools.getMinus(now,orderdate)
    if orderinfo['status'] == 'a----':
        if result.seconds > 1800:
            orderstatus = '----i'
            Z.modifyOrderStatus({'uuid':orderid,'status':orderstatus})
    if orderinfo['status'] == '-b---':
        if result.days > 30:
            orderstatus = '---o-'
            Z.modifyOrderStatus({'uuid':orderid,'status':orderstatus})
    dboper = {'date':''}
    if optid != None:
        dboper = Z.searchOperation(optid)
        if dboper['status'] != 'success':
            dboper['date'] = ''
    dbinstance = Z.searchBookInstance(uuid=bookid)
    if dbinstance['status'] != 'success':
        return dbinstance
    isbn = dbinstance['data']['isbn']
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
        'orderid':orderid,
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
        'userName':dbuser['data']['username'],
        'balance':dbuser['data']['balance']
    }
    return retinfo
    
def getBookInfo(isbn):
    dbkind = Z.searchBookInfo(isbn)
    if dbkind['status'] != 'success':
        return dbkind
    dblocation = Z.searchLocation(dbkind['data']['lc'])
    if dblocation['status'] != 'success':
        return dblocation
    position = tools.divideLocation(dblocation['location'])
    tag = tools.divideTags(dbkind['data']['tags'])
    dbkind['data']['position'] = position
    dbkind['data']['language'] = tag['language']
    dbkind['data']['theme'] = tag['theme']
    return dbkind