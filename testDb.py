#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Database tese case
'''

__author__ = 'Fitzeng'


from database import Database as DB
import datetime
import uuid

_uuid = '527899c7-ba52-11e7-b900-186590dcbd6f'

# ******* addUser *******
# {'username': 'Tony', 'password': 'pw1', 'tel': '15932881234'}
# {'status': 'success'}
# {'status': 'failure', 'errorInfo': 'duplicate key value violates unique constraint "table_account_key_user_name_key"\nDETAIL:  Key (key_user_name)=(Tony) already exists.\n'}
# {'status': 'success'}
def testAddUser():
    print '''******* addUser *******'''
    user = {}
    user['tel'] = '15932881234'
    user['username'] = 'Tony'
    user['password'] = 'pwd1'
    print user
    print DB.addUser(user)
    user['tel'] = '15932881235'
    print DB.addUser(user)
    user['username'] = 'Stark'
    print DB.addUser(user)
    print '''\n\n'''


# ******* modifyUserInfo *******
# {'status': 'failure', 'errorInfo': 'duplicate key value violates unique constraint "table_account_key_user_name_key"\nDETAIL:  Key (key_user_name)=(Stark) already exists.\n'}
# {'status': 'success'}
def testModifyUserInfo():
    print '''******* modifyUserInfo *******'''
    userInfo = {}
    userInfo['uuid'] = _uuid
    userInfo['username'] = 'Stark'
    userInfo['firstname'] = 'Elon'
    userInfo['lastname'] = 'Musk'
    userInfo['birthday'] = str(datetime.datetime.now())
    userInfo['sex'] = 'True'
    userInfo['tel'] = '15932881236'
    print DB.modifyUserInfo(userInfo)
    userInfo['username'] = 'Stark2'
    print DB.modifyUserInfo(userInfo)
    print '''\n\n'''


# {'status': 'failure', 'errorInfo': 'invalid input syntax for type uuid: ""\nLINE 1: ...table_account SET key_password = \'pwd2\' WHERE key_uuid = \'\';\n                                                                    ^\n'}
# {'status': 'success'}
def testModifyUserPWD():
    print '''******* modifyUserPWD *******'''
    userInfo = {}
    userInfo['uuid'] = ''
    userInfo['password'] = 'pwd2'
    print DB.modifyUserPWD(userInfo)
    userInfo['uuid'] = _uuid
    print DB.modifyUserPWD(userInfo)
    print '''\n\n'''


# ******* modifyUserBalance *******
# {'status': 'failure', 'errorInfo': 'column "a1" does not exist\nLINE 1: UPDATE table_account SET key_balance = a1 WHERE key_uuid = \'...\n                                               ^\n'}
# {'status': 'success'}
def testModifyUserBalance():
    print '''******* modifyUserBalance *******'''
    userBalance = {}
    userBalance['uuid'] = _uuid
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
    userRight['uuid'] = _uuid
    userRight['right'] = 2
    print DB.modifyUserRight(userRight)


# ******* getUserUUID *******
# {'status': 'success', 'uuid': '527b4591-ba52-11e7-a659-186590dcbd6f'}
# {'status': 'success', 'uuid': '527899c7-ba52-11e7-b900-186590dcbd6f'}
def testGetUserUUID():
    print '''******* getUserUUID *******'''
    getUserUuid = {}
    getUserUuid['type'] = 'tel'
    getUserUuid['value'] = '15932881235'
    print DB.getUserUUID(getUserUuid)
    getUserUuid['type'] = 'username'
    getUserUuid['value'] = 'Stark2'
    print DB.getUserUUID(getUserUuid)
    print '''\n\n'''


# ******* getUserPWD *******
# {'status': 'success', 'password': 'pwd1'}
# {'status': 'success', 'password': 'pwd2'}
# {'status': 'failure', 'errorInfo': 'this uuid not exist!'}
def testGetUserPWD():
    print '''******* getUserPWD *******'''
    print DB.getUserPWD('527b4591-ba52-11e7-a659-186590dcbd6f')
    print DB.getUserPWD('527899c7-ba52-11e7-b900-186590dcbd6f')
    print DB.getUserPWD('527899c7-ba52-11e7-b900-186590dcbd60')
    print '''\n\n'''


# ******* getUserInfo *******
# {'status': 'success', 'data': {'username': 'Stark', 'right': 1.0, 'tel': '15932881235', 'firstname': None, 'lastname': None, 'sex': None, 'birthday': 'None', 'balance': 'None'}}
# {'status': 'success', 'data': {'username': 'Stark2', 'right': 2.0, 'tel': '15932881236', 'firstname': 'Elon', 'lastname': 'Musk', 'sex': True, 'birthday': '2017-10-26', 'balance': '999.00'}}
# {'status': 'failure', 'errorInfo': 'this uuid not exist!'}
def testGetUserInfo():
    print '''******* getUserInfo *******'''
    print DB.getUserInfo('527b4591-ba52-11e7-a659-186590dcbd6f')
    print DB.getUserInfo('527899c7-ba52-11e7-b900-186590dcbd6f')
    print DB.getUserInfo('527899c7-ba52-11e7-b900-186590dcbd60')
    print '''\n\n'''


# ******* searchISBN *******
# {'status': 'success', 'isbn': ['9780000000262', '9780000000279', '9780000000286', '9780000012340']}
# --------------
# {'status': 'success', 'isbn': ['9780000000262', '9780000000279', '9780000000286', '9780000000293',
# '9780000001849', '9780000005502', '9780000005526']}
# --------------
# {'status': 'success', 'isbn': ['9780000000910']}
# --------------
# {'status': 'success', 'isbn': ['9780000000361', '9780000000798', '9780000000804', '9780000000811',
# '9780000000385', '9780000000392', '9780000000415', '9780000000422', '9780000000439', '9780000000453',
# '9780000000460', '9780000000477', '9780000000484', '9780000000491', '9780000000507', '9780000000514',
# '9780000000521', '9780000000538', '9780000000552', '9780000000583', '9780000000590', '9780000000613',
# '9780000000620', '9780000000644', '9780000000651', '9780000000675', '9780000000699', '9780000000736',
# '9780000000774', '9780000000781', '9780000000828', '9780000000835', '9780000000866', '9780000000880',
# '9780000000897', '9780000000903', '9780000000910', '9780000000927', '9780000000958', '9780000000965',
# '9780000021748', '9780000021885', '9780000025524', '9780000026361']}
def testSearchISBN():
    print '''******* searchISBN *******'''
    info = {}
    info['type'] = 'name'
    info['value'] = 'Govt Supply'
    print DB.searchISBN(info)
    print '''--------------'''
    info['type'] = 'auth'
    info['value'] = ['Macmillan']
    print DB.searchISBN(info)
    print '''--------------'''
    info['value'] = ['Jonas Gustafsson', 'Vello Pekomae']
    print DB.searchISBN(info)
    print '''--------------'''
    info['type'] = 'publisher'
    info['value'] = 'CABI'
    print DB.searchISBN(info)
    print '''\n\n'''







# ******* searchBookInfo *******
# {'status': 'success', 'data': {'publisher': 'Victor Gollancz Ltd', 'isbn': '9780000000002', 'name': 'On The Top Of The World;: The Soviet Expedition To The North Pole, 1937', 'tags': None, 'auth': ['Lazar Konstantinovich Brontman'], 'clc': 'NaN', 'edition': 1, 'publish_date': '2017-10-19', 'snapshot': None}}
# {'status': 'failure', 'errorInfo': 'this isbn not exist!'}
# {'status': 'success', 'data': {'publisher': 'Medical Economics Data,U.S.', 'isbn': '9780000000057', 'name': 'Physicians Desk Reference', 'tags': None, 'auth': [], 'clc': 'NaN', 'edition': 1, 'publish_date': '2017-10-19', 'snapshot': None}}
def testSearchBookInfo():
    print '''******* searchBookInfo *******'''
    print DB.searchBookInfo('9780000000002')
    print DB.searchBookInfo('9780000000003')
    print DB.searchBookInfo('9780000000057')
    print '''\n\n'''

# ******* searchPicture *******
# GIF89a  �    ���!�   ,       L ;
# this isbn not exist!
def testSearchPicture():
    print '''******* searchPicture *******'''
    print DB.searchPicture('9780000000002')
    print DB.searchPicture('9780000000003')
    print '''\n\n'''

# ******* addBookInfo *******
# {'status': 'success'}
# {'status': 'failure', 'errorInfo': 'duplicate key value violates unique constraint "table_book_kind_pkey"\nDETAIL:  Key (key_isbn)=(9780000000002) already exists.\n'}
def testAddBookInfo():
    print '''******* addBookInfo *******'''
    bookInfo = {}
    bookInfo['isbn'] = 'isbn 2'
    bookInfo['clc'] = 'clclclc'
    bookInfo['name'] = 'Book Name'
    bookInfo['auth'] = ['auth1', 'auth2']
    bookInfo['publisher'] = 'p1'
    bookInfo['edition'] = 1
    bookInfo['publish_date'] = datetime.datetime.now()
    bookInfo['tags'] = ['tag1', "tag2"]
    bookInfo['snapshot'] = 'sp'
    print DB.addBookInfo(bookInfo)
    bookInfo['isbn'] = '9780000000002'
    print DB.addBookInfo(bookInfo)
    print '''\n\n'''


# ******* addBookPicture *******
# {'status': 'success'}
# {'status': 'success'}
def testAddBookPicture():
    print '''******* addBookPicture *******'''
    infoP = {}
    infoP['isbn'] = 'isbn 0'
    infoP['data'] = 'bigdata'
    print DB.addBookPicture(infoP)
    infoP['isbn'] = 'isbn 1'
    print DB.addBookPicture(infoP)

# ******* modifyBookInfo *******
# {'status': 'success'}
# {'status': 'success'}
def testModifyBookInfo():
    print '''******* modifyBookInfo *******'''
    bookInfo = {}
    bookInfo['isbn'] = 'isbn 2'
    bookInfo['clc'] = 'clcl'
    bookInfo['name'] = 'Book Name'
    bookInfo['auth'] = ['auth1', 'auth2', "auth 3"]
    bookInfo['publisher'] = 'p1'
    bookInfo['edition'] = 1
    bookInfo['publish_date'] = datetime.datetime.now()
    bookInfo['tags'] = ['tag1', "tag2"]
    bookInfo['snapshot'] = 'sp'
    print DB.modifyBookInfo(bookInfo)
    print '''\n\n'''


# ****** modifyBookPicture *******
# {'status': 'success'}
def testModifyBookPicture():
    print '''****** modifyBookPicture *******'''
    infoP = {}
    infoP['isbn'] = 'isbn 2'
    infoP['data'] = 'bigdataaa'
    print DB.addBookPicture(infoP)

# ******* searchBookInstance *******
# {'status': 'success', 'isbn': 'isbn 1', 'uuid': {'783d76f0-baf8-11e7-9293-186590dcbd6f': None, 'de1b8f6b-baf7-11e7-8c60-186590dcbd6f': None}}
# {'status': 'success', 'isbn': '9780000027665', 'uuid': {'00004761-b922-4efd-a766-de08c52a57da': None}}
def testSearchBookInstance():
    print '''******* searchBookInstance *******'''
    print DB.searchBookInstance('a---', isbn='isbn 1')
    print DB.searchBookInstance('a---', uuid='00004761-b922-4efd-a766-de08c52a57da')
    print '''\n\n'''

# ******* addBookInstance *******
# {'status': 'success'}
# {'status': 'success'}
# {'status': 'success'}
# {'status': 'success'}
# {'status': 'success'}
def testAddBookInstance():
    print '''******* addBookInstance *******'''
    print DB.addBookInstance('isbn 0')
    print DB.addBookInstance('isbn 0')
    print DB.addBookInstance('isbn 0')
    print DB.addBookInstance('isbn 1')
    print DB.addBookInstance('isbn 2')
    print '''\n\n'''

# ******* modifyBookInstance *******
# {'status': 'success'}
def testModifyBookInstance():
    print '''******* modifyBookInstance *******'''
    info = {}
    info['uuid'] = '00004761-b922-4efd-a766-de08c52a57da'
    info['optid'] = str(uuid.uuid1())
    print DB.modifyBookInstance(info)

# ******* searchOperation *******
# {'status': 'success', 'returnDate': '[datetime.date(2017, 10, 28), datetime.date(2017, 10, 28), datetime.date(2017, 10, 28)]', 'statuss': 'a---'}
def testSearchOperation():
    print '''******* searchOperation *******'''
    print DB.searchOperation('4c259187-bbd4-11e7-bdf5-186590dcbd6f')

# ******* addOperation *******
# {'status': 'success', 'uuid': '4c259187-bbd4-11e7-bdf5-186590dcbd6f'}
def testAddOperation():
    print '''******* addOperation *******'''
    data = []
    data.append(str(datetime.datetime.now()))
    data.append(str(datetime.datetime.now()))
    data.append(str(datetime.datetime.now()))
    info = {}
    info['returnDate'] = data
    info['status'] = 'a---'
    print DB.addOperation(info)
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
    info['uuid'] = '4c259187-bbd4-11e7-bdf5-186590dcbd6f'
    info['returnDate'] = data
    print DB.modifyOperationDate(info)
    print '''\n\n'''

# ******* modifyOperationStatus *******
# {'status': 'success'}
def testModifyOperationStatus():
    print '''******* modifyOperationStatus *******'''
    info = {}
    info['uuid'] = '4c259187-bbd4-11e7-bdf5-186590dcbd6f'
    info['status'] = '-a--'
    print DB.modifyOperationStatus(info)
    print '''\n\n'''

# ******* searchOrder *******
# {'status': 'success', 'uuid': {'b400eed4-bbd8-11e7-9174-186590dcbd6f': {'userUUID': '527899c7-ba52-11e7-b900-186590dcbd6f', 'timestamp': datetime.date(2017, 10, 28), 'opt': '{b3fea2a1-bbd8-11e7-ba6e-186590dcbd6f,b400e4d4-bbd8-11e7-982e-186590dcbd6f,b400e5d7-bbd8-11e7-a6d2-186590dcbd6f}'}, '6b68571c-bbd7-11e7-8ef4-186590dcbd6f': {'userUUID': '527899c7-ba52-11e7-b900-186590dcbd6f', 'timestamp': datetime.date(2017, 10, 28), 'opt': '{6b66aecf-bbd7-11e7-aebc-186590dcbd6f,6b684cb8-bbd7-11e7-b669-186590dcbd6f,6b684dcf-bbd7-11e7-a3e8-186590dcbd6f}'}, 'b59a6e42-bbd7-11e7-bc29-186590dcbd6f': {'userUUID': '527899c7-ba52-11e7-b900-186590dcbd6f', 'timestamp': datetime.date(2017, 10, 28), 'opt': '{b598b654-bbd7-11e7-a0d2-186590dcbd6f,b59a6382-bbd7-11e7-b11c-186590dcbd6f,b59a64b0-bbd7-11e7-b538-186590dcbd6f}'}, '71fc6168-bbd7-11e7-a1a8-186590dcbd6f': {'userUUID': '527899c7-ba52-11e7-b900-186590dcbd6f', 'timestamp': datetime.date(2017, 10, 28), 'opt': '{71faae54-bbd7-11e7-b578-186590dcbd6f,71fc574a-bbd7-11e7-9838-186590dcbd6f,71fc584f-bbd7-11e7-90ae-186590dcbd6f}'}}}
# {
# 'status': 'success', 'uuid': {
#                       '64b289b8-bbd7-11e7-bbae-186590dcbd6f': {
#                               'userUUID': '527899c7-ba52-11e7-b900-186590dcbd6f',
#                               'timestamp': datetime.date(2017, 10, 28),
#                               'opt': '{
#                                           64b09087-bbd7-11e7-b5ca-186590dcbd6f,
#                                           64b27e70-bbd7-11e7-b3d9-186590dcbd6f,
#                                           64b27fba-bbd7-11e7-95c4-186590dcbd6f
#                                       }'
#                                                                }
#                               }
# }
def testSearchOrder():
    print '''******* searchOrder *******'''
    print DB.searchOrder(['---a', '--a-'])
    print DB.searchOrder(['---a', '--a-', '-a--', 'a---'], uuid='527899c7-ba52-11e7-b900-186590dcbd6f')
    print '''\n\n'''


# ******* addOrder *******
# {'status': 'success', 'uuid': '71fc6168-bbd7-11e7-a1a8-186590dcbd6f'}
def testAddOrder():
    print '''******* addOrder *******'''
    info = {}
    info['userUUID'] = '527899c7-ba52-11e7-b900-186590dcbd6f'
    info['optid'] = [str(uuid.uuid1()), str(uuid.uuid1()), str(uuid.uuid1())]
    info['status'] = ['---a', '--a-']
    print DB.addOrder(info)
    print '''\n\n'''

# ******* modifyOrderStatus *******
# {'status': 'success'}
def testModifyOrderStatus():
    print '''******* modifyOrderStatus *******'''
    info = {}
    info['uuid'] = '64b289b8-bbd7-11e7-bbae-186590dcbd6f'
    info['status'] = ['---a', '--a-', '-a--', 'a---']
    print DB.modifyOrderStatus(info)
    print '''\n\n'''

def main():
    DB.setConnDefalt()

    # DB.createTable()
    # DB.generateTestData()

    # testAddUser()

    # testModifyUserInfo()

    # testModifyUserPWD()

    # testModifyUserBalance()

    # testModifyUserRight()

    # testGetUserUUID()

    # testGetUserPWD()

    # testGetUserInfo()

    # testSearchISBN()

    # testSearchBookInfo()

    # testSearchPicture()

    # testAddBookInfo()

    # testAddBookPicture()

    # testModifyBookInfo()

    # testModifyBookPicture()

    # testSearchBookInstance()

    # testAddBookInstance()

    # testModifyBookInstance()

    # testSearchOperation()

    # testAddOperation()

    # testModifyOperationDate()

    # testModifyOperationStatus()

    # testSearchOrder()

    # testAddOrder()

    # testModifyOrderStatus()

main()
