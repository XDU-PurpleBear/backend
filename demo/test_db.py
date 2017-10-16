#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Database tese case
'''

__author__ = 'Fitzeng'

import datetime

from database import Database as Db
import user, book

_host, _port, _database, _user, _password = '127.0.0.1', '5432', 'purple', 'postgres', 'kgp168668'

conn = Db.get_database_conn(_host, _port, _database, _user, _password)

cur = Db.get_cur(conn)
#
Db.generateTestData(cur)


''' test Regeister function '''
print Db.addUser('10000000001', 'name 12', 'pwd')
print Db.addUser('10000030001', 'name 2', 'pwd')
print Db.addUser('10000020001', 'name 13', 'pwd')
print '\n\n'
# output
# False
# True
# True

''' test GetPWD function '''
print Db.getPWD(user_name='name 0', password='pwd 0')
print Db.getPWD(user_name='name 1', password='pwd 0')
print Db.getPWD(user_name='name 11', password='pwd 0')
print '\n\n'
# output:
# {'Result': True}
# {'Result': 'False', 'Log': 'Password is incorrect'}
# {'Result': 'False', 'Log': 'User Not Exits'}

''' test GetUserInfo function '''
print Db.getUserInfo(user_name='name 3')
print Db.getUserInfo(user_name='Name 3')
print Db.getUserInfo(tel='10000002002')
print Db.getUserInfo(tel='10000002003')
print '\n\n'
# output
# <user.User object at 0x10b4f6310>
# None
# <user.User object at 0x10b4f6310>
# None

''' test ModifyUserInfo function '''
_user = user.User()
_user.user_name = 'name 12'
_user.first_name = 'zeng'
_user.last_name = 'zhijian'
_user.balance = '10'
_user.tel = '10000000008'
_user.birthday = str(datetime.datetime.now())
print Db.modifyUserInfo(_user, user_name='name 7')
print Db.modifyUserInfo(_user, user_name='name 8')
print '\n\n'
# output
# True
# False


''' test QueryBookKind function '''
print Db.queryBookKind(name='bookname 1')
print Db.queryBookKind(clc='ha')
print Db.queryBookKind(name='name12')
_book = Db.queryBookKind(name='bookname 1')
print _book[0].name
print '\n\n'
# output
# [<book.Book object at 0x110205390>]
# []
# []

''' test QueryBook function '''
print Db.queryBook('ISBN 0')
print Db.queryBook('ISBN')
print '\n\n'
# output
# [<book.BookInstance object at 0x1056963d0>]
# []

''' test AddBook function '''
_book = book.Book()
_book.isbn = 'ISBN 10'
_book.publish_date = str(datetime.datetime.now())
_book.auth = '{auth 1}'
_book.name = 'add-name'
print Db.addBook(_book)
print Db.addBook(_book)
print '\n\n'
# output
# True
# True

''' test AddBooks function '''
print Db.addBooks(_book, 3)
print '\n\n'
# output
# True


''' test Username And UUID function '''
_uuid = Db.getUUIDByUsername('name 2')
_user_name = Db.getUsernameByUUID(_uuid)
print _uuid, '\n', _user_name

conn.commit()
conn.close()
