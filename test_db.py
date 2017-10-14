#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Database tese case
'''

__author__ = 'Fitzeng'

import datetime

import database
import user, book

_host, _port, _database, _user, _password = '127.0.0.1', '5432', 'purple', 'postgres', 'xxxx'

conn = database.Database.get_database_conn(_host, _port, _database, _user, _password)

cur = database.Database.get_cur(conn)

database.Database.generateTestData(cur)


''' test Regeister function '''
print database.Database.register(tel='10000000001', password='pwd')
print database.Database.register(tel='10000002001', password='pwd 0')
print database.Database.register(tel='10000002002', password='pwd 0')
print '\n\n'
# output
# False
# True
# True

''' test Login function '''
print database.Database.login(user_name='name 0', password='pwd 0')
print database.Database.login(user_name='name 1', password='pwd 0')
print database.Database.login(user_name='name 11', password='pwd 0')
print '\n\n'
# output:
# {'Result': True}
# {'Result': 'False', 'Log': 'Password is incorrect'}
# {'Result': 'False', 'Log': 'User Not Exits'}

''' test GetUserInfo function '''
print database.Database.getUserInfo(user_name='name 3')
print database.Database.getUserInfo(user_name='Name 3')
print database.Database.getUserInfo(tel='10000002002')
print database.Database.getUserInfo(tel='10000002003')
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
print database.Database.modifyUserInfo(_user, user_name='name 7')
print database.Database.modifyUserInfo(_user, user_name='name 8')
print '\n\n'
# output
# True
# False


''' test QueryBookKind function '''
print database.Database.queryBookKind(name='bookname 1')
print database.Database.queryBookKind(clc='ha')
print database.Database.queryBookKind(name='name12')
print '\n\n'
# output
# [<book.Book object at 0x110205390>]
# []
# []

''' test QueryBook function '''
print database.Database.queryBook('ISBN 0')
print database.Database.queryBook('ISBN')
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
print database.Database.addBook(_book)
print database.Database.addBook(_book)
print '\n\n'
# output
# True
# True

''' test AddBooks function '''
print database.Database.addBooks(_book, 3)
print '\n\n'
# output
# True

conn.commit()
conn.close()
