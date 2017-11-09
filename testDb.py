#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Database tese case
'''

__author__ = 'Fitzeng'


import datetime
import uuid

from database import Database as DB

_uuid1 = '7188ffb5-c041-11e7-a774-186590dcbd6f'
_uuid2 = '718b789c-c041-11e7-aadc-186590dcbd6f'

# ******* addUser *******
# {'username': 'Tony', 'password': 'pw111', 'tel': '15932881234', 'pledge': 300, 'stu_id': 14130120111, 'balance': 100}
# {'status': 'success'}
# {'status': 'failure', 'errorInfo': 'duplicate key value violates unique constraint "table_account_key_user_name_key"\nDETAIL:  Key (key_user_name)=(Tony) already exists.\n'}
# {'status': 'success'}
def testAddUser():
    print '''******* addUser *******'''
    user = {}
    user['tel'] = '15932881234'
    user['username'] = 'Tony'
    user['password'] = 'pw111'
    user['balance'] = 100
    user['pledge'] = 300
    user['stu_id'] = 14130120111
    print user
    print DB.addUser(user)
    user['tel'] = '15932881235'
    print DB.addUser(user)
    user['username'] = 'Stark'
    user['stu_id'] = 14130120112
    print DB.addUser(user)
    print '''\n\n'''

# ******* deleteUser *******
# {'status': 'success'}
def testDeleteUser():
    print '''******* deleteUser *******'''
    print DB.deleteUser(_uuid1)
    print '''\n\n'''

# ******* modifyUserPWD *******
# {'status': 'failure', 'errorInfo': 'invalid input syntax for type uuid: ""\nLINE 1: ...table_account SET key_password = \'pwd2\' WHERE key_uuid = \'\';\n                                                                    ^\n'}
# {'status': 'success'}
def testModifyUserPWD():
    print '''******* modifyUserPWD *******'''
    userInfo = {}
    userInfo['uuid'] = ''
    userInfo['password'] = 'pwd2'
    print DB.modifyUserPWD(userInfo)
    userInfo['uuid'] = _uuid2
    print DB.modifyUserPWD(userInfo)
    print '''\n\n'''

# ******* modifyUserBalance *******
# {'status': 'failure', 'errorInfo': 'column "a1" does not exist\nLINE 1: UPDATE table_account SET key_balance = a1 WHERE key_uuid = \'...\n                                               ^\n'}
# {'status': 'success'}
def testModifyUserBalance():
    print '''******* modifyUserBalance *******'''
    userBalance = {}
    userBalance['uuid'] = _uuid2
    userBalance['balance'] = 'a1'
    print DB.modifyUserBalance(userBalance)
    userBalance['balance'] = 999
    print DB.modifyUserBalance(userBalance)
    print '''\n\n'''

# ******* modifyUserRight *******
# {'status': 'success'}
def testModifyUserRight():
    print '''******* modifyUserRight *******'''
    userRight = {}
    userRight['uuid'] = _uuid2
    userRight['right'] = 2
    print DB.modifyUserRight(userRight)
    print '''\n\n'''

# ******* getUserUUID *******
# {'status': 'success', 'uuid': '718b789c-c041-11e7-aadc-186590dcbd6f'}
# {'status': 'failure', 'errorInfo': 'uuid not exist!'}
# {'status': 'success', 'uuid': '718b789c-c041-11e7-aadc-186590dcbd6f'}
# {'status': 'failure', 'errorInfo': 'uuid not exist!'}
def testGetUserUUID():
    print '''******* getUserUUID *******'''
    getUserUuid = {}
    getUserUuid['type'] = 'tel'
    getUserUuid['value'] = '15932881235'
    print DB.getUserUUID(getUserUuid)
    getUserUuid['type'] = 'tel'
    getUserUuid['value'] = '15932881236'
    print DB.getUserUUID(getUserUuid)
    getUserUuid['type'] = 'stuid'
    getUserUuid['value'] = '14130120112'
    print DB.getUserUUID(getUserUuid)
    getUserUuid['type'] = 'stuid'
    getUserUuid['value'] = '14130120113'
    print DB.getUserUUID(getUserUuid)
    print '''\n\n'''

# ******* getUserPWD *******
# {'status': 'success', 'password': 'pwd2'}
# {'status': 'failure', 'errorInfo': 'this uuid not exist!'}
def testGetUserPWD():
    print '''******* getUserPWD *******'''
    print DB.getUserPWD(_uuid2)
    print DB.getUserPWD('527899c7-ba52-11e7-b900-186590dcbd6f')
    print '''\n\n'''

# ******* getUserInfo *******
# {'status': 'success', 'data': {'username': 'Stark', 'right': 2.0, 'tel': 15932881235L, 'pledge': '300.00', 'logo': 'None', 'balance': '999.00', 'stuid': 14130120112L, 'uuid': '718b789c-c041-11e7-aadc-186590dcbd6f'}}
# {'status': 'failure', 'errorInfo': 'this uuid not exist!'}
def testGetUserInfo():
    print '''******* getUserInfo *******'''
    print DB.getUserInfo(_uuid2)
    print DB.getUserInfo('527899c7-ba52-11e7-b900-186590dcbd60')
    print '''\n\n'''

# ******* addBookInfo *******
# {'status': 'success'}
# {'status': 'success'}
def testAddBookInfo():
    print '''******* addBookInfo *******'''
    bookInfo = {}
    bookInfo['isbn'] = 'isbn 2'
    bookInfo['lc'] = 'clclclc'
    bookInfo['name'] = 'Book Name'
    bookInfo['auth'] = ['auth1', 'auth2']
    bookInfo['publisher'] = 'p1'
    bookInfo['edition'] = 1
    bookInfo['imgs'] = str(uuid.uuid1())
    bookInfo['tags'] = ['tag1']
    bookInfo['abstract'] = 'sp'
    print DB.addBookInfo(bookInfo)
    bookInfo['isbn'] = '9780000000002'
    bookInfo['tags'] = ['tag1', "tag2"]
    print DB.addBookInfo(bookInfo)
    print '''\n\n'''

# ******* deleteBookInfo *******
# {'status': 'success'}
# {'status': 'success'} : 代表语句执行成功，说明数据库里已经没有该书了
def testDeleteBookInfo():
    print '''******* deleteBookInfo *******'''
    print DB.deleteBookInfo('isbn 2')
    print DB.deleteBookInfo('isbn 2')
    print '''\n\n'''

def testModifyBookInfo():
    pass

# ******* searchISBN *******
# {'status': 'success', 'isbn': ['isbn 2', '9780000000002']}
# {'status': 'success', 'isbn': ['isbn 2', '9780000000002']}
# {'status': 'success', 'isbn': ['isbn 2', '9780000000002']}
# {'status': 'failure', 'errorInfo': 'this kind book not exist!'}
# --------------
# {'status': 'success', 'isbn': ['isbn 2', '9780000000002']}
# {'status': 'success', 'isbn': ['isbn 2', '9780000000002']}
# {'status': 'failure', 'errorInfo': 'this kind book not exist!'}
# {'status': 'failure', 'errorInfo': 'this kind book not exist!'}
# {'status': 'success', 'isbn': ['isbn 2', '9780000000002']}
# --------------
# {'status': 'success', 'isbn': ['isbn 2', '9780000000002']}
# {'status': 'success', 'isbn': ['9780000000002']}
# {'status': 'failure', 'errorInfo': 'this kind book not exist!'}
# {'status': 'success', 'isbn': ['9780000000002']}
def testSearchISBN():
    print '''******* searchISBN *******'''
    info = {}
    info['type'] = 'name'
    info['value'] = 'Boo'
    print DB.searchISBN(info)
    info['value'] = 'Book Name'
    print DB.searchISBN(info)
    info['value'] = 'book '
    print DB.searchISBN(info)
    info['value'] = 'Book a'
    print DB.searchISBN(info)
    print '''--------------'''

    info['type'] = 'auth'
    info['value'] = ['auth1']
    print DB.searchISBN(info)
    info['value'] = ['auth2']
    print DB.searchISBN(info)
    info['value'] = ['auth3']
    print DB.searchISBN(info)
    info['value'] = ['auth2', 'auth']
    print DB.searchISBN(info)
    info['value'] = ['auth2', 'auth1']
    print DB.searchISBN(info)
    print '''--------------'''

    info['type'] = 'tags'
    info['value'] = ['tag1']
    print DB.searchISBN(info)
    info['value'] = ['tag2']
    print DB.searchISBN(info)
    info['value'] = ['tag3']
    print DB.searchISBN(info)
    info['value'] = ['tag1', 'tag2']
    print DB.searchISBN(info)
    print '''\n\n'''

# ******* searchBookInfo *******
# {'status': 'success', 'data': {'publisher': 'p1', 'isbn': '9780000000002', 'lc': 'clclclc', 'tags': ['tag1', 'tag2'], 'abstract': 'sp', 'auth': ['auth1', 'auth2'], 'edition': 1, 'imgs': '0ca384f5-c051-11e7-8f91-186590dcbd6f', 'name': 'Book Name'}}
# {'status': 'success', 'data': {'publisher': 'p1', 'isbn': 'isbn 2', 'lc': 'clclclc', 'tags': ['tag1'], 'abstract': 'sp', 'auth': ['auth1', 'auth2'], 'edition': 1, 'imgs': '0ca384f5-c051-11e7-8f91-186590dcbd6f', 'name': 'Book Name'}}
# {'status': 'failure', 'errorInfo': 'this isbn not exist!'}
def testSearchBookInfo():
    print '''******* searchBookInfo *******'''
    print DB.searchBookInfo('9780000000002')
    print DB.searchBookInfo('isbn 2')
    print DB.searchBookInfo('9780000000003')
    print '''\n\n'''

# ******* addBookInstance *******
# {'status': 'success'}
# {'status': 'success'}
# {'status': 'success'}
# {'status': 'success'}
# {'status': 'success'}
def testAddBookInstance():
    print '''******* addBookInstance *******'''
    print DB.addBookInstance('isbn 2')
    print DB.addBookInstance('isbn 2')
    print DB.addBookInstance('isbn 2')
    print DB.addBookInstance('9780000000002')
    print DB.addBookInstance('9780000000002')
    print '''\n\n'''

# ******* deleteBookInstance *******
# {'status': 'success'}
# {'status': 'success'}
# {'status': 'success'} 同上一个删除函数，只是代表 sql 语句执行后不存在该书，而不代表删除该书。
def testDeleteBookInstance():
    print '''******* deleteBookInstance *******'''
    print DB.deleteBookInstance('04d4b719-c053-11e7-aaab-186590dcbd6f')
    print DB.deleteBookInstance('04da2540-c053-11e7-83bb-186590dcbd6f')
    print DB.deleteBookInstance('04da2540-c053-11e7-13bb-186590dcbd6f')
    print '''\n\n'''

# ******* modifyBookInstance *******
# {'status': 'success'}
# {'status': 'success'}
# {'status': 'success'}
def testModifyBookInstance():
    print '''******* modifyBookInstance *******'''
    info = {}
    info['uuid'] = '04d8e9a1-c053-11e7-8627-186590dcbd6f'
    info['optid'] = str(uuid.uuid1())
    print DB.modifyBookInstance(info)
    info['uuid'] = '04da0497-c053-11e7-a638-186590dcbd6f'
    info['optid'] = str(uuid.uuid1())
    print DB.modifyBookInstance(info)
    info['uuid'] = '04da0497-c053-11e7-a638-186590dcbd6f'
    info['optid'] = None
    print DB.modifyBookInstance(info)

# ******* searchBookInstance *******
# {'status': 'failure', 'errorInfo': 'This book not exist!'}
# {'status': 'success', 'data': {'isbn': 'isbn 2', 'uuids': [{'status': 'a---', 'optid': None, 'uuid': '04da0497-c053-11e7-a638-186590dcbd6f'}, {'status': 'a---', 'optid': None, 'uuid': '04da0497-c053-11e7-a638-186590dcbd6f'}]}}
# ------------------
# {'status': 'failure', 'errorInfo': 'This book not exist!'}
# {'status': 'success', 'data': {'isbn': 'isbn 2', 'uuids': [{'status': 'a---', 'optid': '5c1d324c-c054-11e7-838b-186590dcbd6f', 'uuid': '04d8e9a1-c053-11e7-8627-186590dcbd6f'}]}}
# ------------------
# {'status': 'failure', 'errorInfo': 'This book not exist!'}
# {'status': 'success', 'data': {'isbn': 'isbn 2', 'uuids': [{'status': 'a---', 'optid': '5c1d324c-c054-11e7-838b-186590dcbd6f', 'uuid': '04d8e9a1-c053-11e7-8627-186590dcbd6f'}]}}
# {'status': 'failure', 'errorInfo': 'kws error!'}
def testSearchBookInstance():
    print '''******* searchBookInstance *******'''
    print DB.searchBookInstance(isbn='isbn 1')
    print DB.searchBookInstance(isbn='isbn 2')
    print '''------------------'''
    print DB.searchBookInstance(uuid='00004761-b922-4efd-a766-de08c52a57da')
    print DB.searchBookInstance(uuid='04d8e9a1-c053-11e7-8627-186590dcbd6f')
    print '''------------------'''
    print DB.searchBookInstance(optid='')
    print DB.searchBookInstance(optid='5c1d324c-c054-11e7-838b-186590dcbd6f')
    print DB.searchBookInstance(opt_id='5c1d324c-c054-11e7-838b-186590dcbd6f')
    print '''\n\n'''

# ******* addOrder *******
# {'status': 'success', 'uuid': '21c90640-c059-11e7-bbde-186590dcbd6f'}
def testAddOrder():
    print '''******* addOrder *******'''
    info = {}
    info['userid'] = '718b789c-c041-11e7-aadc-186590dcbd6f'
    info['bookid'] = '04d8e9a1-c053-11e7-8627-186590dcbd6f'
    info['status'] = 'staussss'
    print DB.addOrder(info)
    print '''\n\n'''

def testDeleteOrder():
    print '''******* deleteOrder *******'''
    # print DB.deleteOrder(_uuid1)
    print '''\n\n'''

# ******* modifyOrderStatus *******
# {'status': 'success', 'uuid': '21c90640-c059-11e7-bbde-186590dcbd6f'}
def testModifyOrderStatus():
    print '''******* modifyOrderStatus *******'''
    info = {}
    info['uuid'] = '21c90640-c059-11e7-bbde-186590dcbd6f'
    info['status'] = 'sta---'
    print DB.modifyOrderStatus(info)
    print '''\n\n'''

# ******* searchOrder *******
# {'status': 'success', 'data': [{'orderid': '21c90640-c059-11e7-bbde-186590dcbd6f', 'timestamp': datetime.date(2017, 11, 3), 'userid': '718b789c-c041-11e7-aadc-186590dcbd6f', 'bookid': '04d8e9a1-c053-11e7-8627-186590dcbd6f'}]}
# {'status': 'success', 'data': [{'orderid': '21c90640-c059-11e7-bbde-186590dcbd6f', 'timestamp': datetime.date(2017, 11, 3), 'userid': '718b789c-c041-11e7-aadc-186590dcbd6f', 'bookid': '04d8e9a1-c053-11e7-8627-186590dcbd6f'}]}
# {'status': 'success', 'data': [{'orderid': '21c90640-c059-11e7-bbde-186590dcbd6f', 'timestamp': datetime.date(2017, 11, 3), 'userid': '718b789c-c041-11e7-aadc-186590dcbd6f', 'bookid': '04d8e9a1-c053-11e7-8627-186590dcbd6f'}]}
# {'status': 'success', 'data': [{'orderid': '21c90640-c059-11e7-bbde-186590dcbd6f', 'timestamp': datetime.date(2017, 11, 3), 'userid': '718b789c-c041-11e7-aadc-186590dcbd6f', 'bookid': '04d8e9a1-c053-11e7-8627-186590dcbd6f'}]}
# {'status': 'failure', 'errorInfo': 'This search condition not exist!'}
# {'status': 'failure', 'errorInfo': 'This search condition not exist!'}
def testSearchOrder():
    print '''******* searchOrder *******'''
    print DB.searchOrder(orderid='21c90640-c059-11e7-bbde-186590dcbd6f')
    print DB.searchOrder(orderid='21c90640-c059-11e7-bbde-186590dcbd6f', status='sta---')
    print DB.searchOrder(userid='718b789c-c041-11e7-aadc-186590dcbd6f')
    print DB.searchOrder(userid='718b789c-c041-11e7-aadc-186590dcbd6f', status='sta---')
    print DB.searchOrder(userid='718b789c-c041-11e7-aadc-186590dcbd62', status='sta---')
    print DB.searchOrder()
    print '''\n\n'''

# ******* addOperation *******
# {'status': 'success', 'uuid': '021d7738-c05c-11e7-befb-186590dcbd6f'}
# {'status': 'success', 'uuid': '0220aff0-c05c-11e7-9df1-186590dcbd6f'}
# {'status': 'success', 'uuid': '0221cd35-c05c-11e7-bfb9-186590dcbd6f'}
def testAddOperation():
    print '''******* addOperation *******'''
    data = []
    data.append(str(datetime.datetime.now()))
    data.append(str(datetime.datetime.now()))
    info = {}
    info['date'] = data
    info['status'] = 'staussss'
    print DB.addOperation(info)
    data.append(str(datetime.datetime.now()))
    print DB.addOperation(info)
    data.append(str(datetime.datetime.now()))
    print DB.addOperation(info)
    print '''\n\n'''

# ******* deleteOperation *******
# {'status': 'success'}
def testDeleteOperation():
    print '''******* deleteOperation *******'''
    print DB.deleteOperation('0221cd35-c05c-11e7-bfb9-186590dcbd6f')
    print '''\n\n'''

# ******* modifyOperationDate *******
# {'status': 'success'}
def testModifyOperationDate():
    print '''******* modifyOperationDate *******'''
    data = []
    data.append(str(datetime.datetime.now()))
    data.append(str(datetime.datetime.now()))
    data.append(str(datetime.datetime.now()))
    data.append(str(datetime.datetime.now()))
    info = {}
    info['uuid'] = '0220aff0-c05c-11e7-9df1-186590dcbd6f'
    info['date'] = data
    print DB.modifyOperationDate(info)
    print '''\n\n'''

# ******* modifyOperationStatus *******
# {'status': 'success'}
def testModifyOperationStatus():
    print '''******* modifyOperationStatus *******'''
    info = {}
    info['uuid'] = '021d7738-c05c-11e7-befb-186590dcbd6f'
    info['status'] = '-status-'
    print DB.modifyOperationStatus(info)
    print '''\n\n'''

# ******* searchOperation *******
# {'status': 'success', 'date': '[datetime.date(2017, 11, 3), datetime.date(2017, 11, 3), datetime.date(2017, 11, 3), datetime.date(2017, 11, 3)]', 'statuss': 'staussss'}
# 碰到 datetime.date(2017, 11, 3) 这种原生数据直接 str() 一下就好
def testSearchOperation():
    print '''******* searchOperation *******'''
    print DB.searchOperation('0220aff0-c05c-11e7-9df1-186590dcbd6f')
    print '''\n\n'''

# ******* addLocation *******
# {'status': 'success'}
def testAddLocation():
    print '''******* addLocation *******'''
    info = {}
    info['begin'] = 'bbb'
    info['end'] = 'eee'
    info['location'] = 'lololol'
    print DB.addLocation(info)
    print '''\n\n'''

def testDeleteLocation():
    print '''******* deleteLocation *******'''
    print '''\n\n'''

def testModifyLocation():
    print '''******* modifyLocation *******'''
    print '''\n\n'''

# ******* searchLocation *******
# {'status': 'success', 'location': '101-11'}
# {'status': 'success', 'location': '504-18'}
# {'status': 'success', 'location': '601-10'}
# {'status': 'failure', 'errorInfo': 'This location not exist!'}
# {'status': 'success', 'location': '301-14'}
# {'status': 'failure', 'errorInfo': 'This location not exist!'}
def testSearchLocation():
    print '''******* searchLocation *******'''
    print DB.searchLocation('AN1')
    print DB.searchLocation('VK5')
    print DB.searchLocation('Z9')
    print DB.searchLocation('Z123')
    print DB.searchLocation('KU/KUQ2')
    print DB.searchLocation('KU/K:d?')
    print '''\n\n'''

# ******* addHistory *******
# {'status': 'success'}
# {'status': 'success'}
# {'status': 'success'}
def testAddHistory():
    print '''******* addHistory *******'''
    info = {}
    info['bookid'] = 'book_id'
    info['userid'] = '718b789c-c041-11e7-aadc-186590dcbd6f'
    print DB.addHistory(info)
    print DB.addHistory(info)
    info['bookid'] = 'book_id1'
    print DB.addHistory(info)
    print '''\n\n'''

# ******* searchHistory *******
# {'status': 'success', 'date': [
#               {'userid': '718b789c-c041-11e7-aadc-186590dcbd6f', 'bookid': 'book_id', 'time': '17:59:28.565545'},
#               {'userid': '718b789c-c041-11e7-aadc-186590dcbd6f', 'bookid': 'book_id1', 'time': '17:59:28.597863'},
#               {'userid': '718b789c-c041-11e7-aadc-186590dcbd6f', 'bookid': 'book_id', 'time': '17:59:44.883426'},
#               {'userid': '718b789c-c041-11e7-aadc-186590dcbd6f', 'bookid': 'book_id', 'time': '17:59:44.885723'},
#               {'userid': '718b789c-c041-11e7-aadc-186590dcbd6f', 'bookid': 'book_id1', 'time': '17:59:44.886228'}]
# }
def testSearchHistory():
    print '''******* searchHistory *******'''
    print DB.searchHistory('718b789c-c041-11e7-aadc-186590dcbd6f')
    print '''\n\n'''

# ******* searchAllHistory *******
# {'status': 'success', 'date': [
#               {'userid': '718b789c-c041-11e7-aadc-186590dcbd6f', 'bookid': 'book_id', 'time': '17:59:28.565545'},
#               {'userid': '718b789c-c041-11e7-aadc-186590dcbd6f', 'bookid': 'book_id1', 'time': '17:59:28.597863'},
#               {'userid': '718b789c-c041-11e7-aadc-186590dcbd6f', 'bookid': 'book_id', 'time': '17:59:44.883426'},
#               {'userid': '718b789c-c041-11e7-aadc-186590dcbd6f', 'bookid': 'book_id', 'time': '17:59:44.885723'},
#               {'userid': '718b789c-c041-11e7-aadc-186590dcbd6f', 'bookid': 'book_id1', 'time': '17:59:44.886228'}]
# }
def testSearchAllHistory():
    print '''******* searchAllHistory *******'''
    print DB.searchAllHistory()
    print '''\n\n'''

# ******* addImage *******
# {'status': 'success', 'uuid': '38e50d1e-c215-11e7-9fe3-186590dcbd6f'}
# {'status': 'success', 'uuid': '38eba7dc-c215-11e7-881f-186590dcbd6f'}
# {'status': 'success', 'uuid': '38ec7963-c215-11e7-b486-186590dcbd6f'}
def testAddImage():
    print '''******* addImage *******'''
    info = {}
    info['mime'] = 'mime'
    info['data'] = 'dadadada'
    print DB.addImage(info)
    print DB.addImage(info)
    print DB.addImage(info)
    print '''\n\n'''

# ******* deleteImage *******
# {'status': 'success'}
def testDeleteImage():
    print '''******* deleteImage *******'''
    print DB.deleteImage('38ec7963-c215-11e7-b486-186590dcbd6f')
    print '''\n\n'''

# ******* modifyImage *******
# {'status': 'success'}
def testModifyImage():
    print '''******* modifyImage *******'''
    info = {}
    info['mime'] = 'mmmmime'
    info['data'] = 'dadadada'
    info['uuid'] = '38eba7dc-c215-11e7-881f-186590dcbd6f'
    print DB.modifyImage(info)

# ******* searchImage *******
# {'status': 'success', 'date': {'data': 'dadadada', 'mime': 'mmmmime'}}
# {'status': 'success', 'date': {'data': 'dadadada', 'mime': 'mime'}}
# {'status': 'failure', 'errorInfo': 'This uuid not exist!'}
def testSearchImage():
    print '''******* searchImage *******'''
    print DB.searchImage('38eba7dc-c215-11e7-881f-186590dcbd6f')
    print DB.searchImage('38e50d1e-c215-11e7-9fe3-186590dcbd6f')
    print DB.searchImage('38e50d1e-c215-11e7-9fe3-186590dcbd6e')
    print '''\n\n'''

def main():

    DB.setConnDefalt()

    # DB.createTable()
    DB.generateTestData()

    # testAddUser()
    #
    # testDeleteUser()
    #
    # testModifyUserPWD()
    #
    # testModifyUserBalance()
    #
    # testModifyUserRight()
    #
    # testGetUserUUID()
    #
    # testGetUserPWD()
    #
    # testGetUserInfo()
    #
    # testAddBookInfo()
    #
    # testDeleteBookInfo()
    #
    # testSearchISBN()
    #
    # testSearchBookInfo()
    #
    # testAddBookInstance()
    #
    # testDeleteBookInstance()
    #
    # testModifyBookInstance()
    #
    # testSearchBookInstance()
    #
    # testAddOrder()
    #
    # testDeleteOrder()
    #
    # testModifyOrderStatus()
    #
    # testSearchOrder()
    #
    # testAddOperation()
    #
    # testDeleteOperation()
    #
    # testModifyOperationDate()
    #
    # testModifyOperationStatus()
    #
    # testSearchOperation()
    #
    # testAddLocation()
    #
    # testDeleteLocation()
    #
    # testModifyLocation()
    #
    # testSearchLocation()
    #
    # testAddHistory()
    #
    # testSearchHistory()
    #
    # testSearchAllHistory()
    #
    # testAddImage()
    #
    # testDeleteImage()
    #
    # testModifyImage()
    #
    # testSearchImage()


    # TODO
    # testSearchPicture()

    # testAddBookPicture()

    # testModifyBookInfo()

    # testModifyBookPicture()


main()
