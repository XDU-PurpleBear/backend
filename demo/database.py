# -*- coding: utf-8 -*-



__author__ = 'Fitzeng'

import datetime
import psycopg2
import re
import user
import uuid
import book



class Database(object):

    def __init__(self):
        pass


    @classmethod
    def get_database_conn(cls, _host, _port, _database, _user, _password):
        cls.__conn = psycopg2.connect(host=_host, port=_port, database=_database, user=_user, password=_password)
        cls.__cur = cls.__conn.cursor()
        return cls.__conn


    '''
    获取 cursor
    '''
    @classmethod
    def get_cur(cls, conn):

        return cls.__cur


    '''
    功能：添加用户
    输入：addUser(cls, tel, password):
    输出： {'status': 'failure', 'errorInfo': str(e)}
    '''
    @classmethod
    def addUser(cls, tel, user_name, password):
        # get insert sql string
        sql = 'INSERT INTO table_account (key_uuid, key_tel, key_user_name, key_password, key_right) ' \
              'VALUES (\'' + str(uuid.uuid1()) +'\', \'' + tel + '\',\'' + user_name + '\', \'' + password + '\', 1);'
        # execute sql
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'Status': 'Failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'Status': 'Success'}


    '''
    功能：登录
    输入：getPWD(user_name/tel = 'XXX')
    输出：{'password': '###'}
    '''
    @classmethod
    def getPWD(cls, **kws):
        # get password if user exist

        # get password by user_name
        if kws.has_key('user_name'):
            sql = 'SELECT key_password FROM table_account WHERE key_user_name = \'' + kws['user_name'] + '\';'
        # get password by tel
        elif kws.has_key('tel'):
            sql = 'SELECT key_password FROM table_account WHERE key_tel = \'' + kws['tel'] + '\';'

        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if (rows):
            return {'password':rows[0][0]}
        else:
            return {'password': ''}


    '''
    功能：获取用户信息
    输入：getUserInfo(user_name/tel = 'XXX')
    输出：{**kws: user_name, first_name, last_name, birthday, register_date, balance, sex, tel, right}
    '''
    @classmethod
    def getUserInfo(cls, **kws):
        _user = user.User()
        if kws.has_key('user_name'):
            sql = 'SELECT key_user_name, key_first_name, key_last_name, key_birthday, key_register_date, ' \
                  'key_balance, key_sex, key_tel, key_right FROM table_account WHERE key_user_name = \'' + kws['user_name'] + '\';'
        elif kws.has_key('tel'):
            sql = 'SELECT key_user_name, key_first_name, key_last_name, key_birthday, key_register_date, ' \
                  'key_balance, key_sex, key_tel, key_right FROM table_account WHERE key_tel = \'' + kws['tel'] + '\';'
        else:
            return None

        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if (rows):
            _user.user_name = rows[0][0]
            _user.first_name = rows[0][1]
            _user.last_name = rows[0][2]
            _user.birthday = rows[0][3]
            _user.register_date = rows[0][4]
            _user.birthday = rows[0][5]
            _user.sex = rows[0][6]
            _user.tel = rows[0][7]
            _user.right = rows[0][8]
            return _user
        else:
            return None


    '''
    功能：修改用户信息
    输入：modifyUserInfo(_user, old_username/tel)
    输出：True/False
    '''
    @classmethod
    def modifyUserInfo(cls, _user, **kws):
        sql = 'UPDATE table_account SET ' \
              'key_user_name = \'' + _user.user_name + '\', ' \
              'key_first_name = \'' + _user.first_name + '\', ' \
              'key_last_name = \'' + _user.last_name + '\', ' \
              'key_birthday = \'' + _user.birthday + '\', ' \
              'key_balance = ' + str(_user.balance) + ', ' \
              'key_sex = ' + str(_user.sex) + ', ' \
              'key_tel = ' + str(_user.tel) + ', ' \
              'key_right = ' + str(_user.right) + ' '
        if kws.has_key('user_name'):
            sql += 'WHERE key_user_name = \'' + kws['user_name'] + '\';'
        elif kws.has_key('tel'):
            sql += 'WHERE key_tel = \'' + kws['tel'] + '\';'
        else:
            return False
        sql = re.sub('\'None\' | None', 'null', sql)
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return str(e)
        finally:
            cls.__conn.commit()
        return '{}'


    '''
    功能：获取用户 UUID
    输入：getUUIDByUsername(user_name)
    输出：UUID
    '''
    @classmethod
    def getUUIDByUsername(cls, _user_name):
        sql = 'SELECT key_uuid FROM table_account WHERE key_user_name = \'' + _user_name + '\';'
        cls.__cur.execute(sql)
        return cls.__cur.fetchall()[0][0]


    '''
    功能：获取用户名
    输入：getUsernameByUUID(uuid)
    输出：User_name
    '''
    @classmethod
    def getUsernameByUUID(cls, _uuid):
        sql = 'SELECT key_user_name FROM table_account WHERE key_uuid = \'' + _uuid + '\';'
        cls.__cur.execute(sql)
        return cls.__cur.fetchall()[0][0]


    '''
    功能：查询书的种类
    输入：queryBookKind(name/clc)
    输出：BOOK INFORMATION LIST
    '''
    @classmethod
    def queryBookKind(cls, **kws):
        if kws.has_key('name'):
            sql = 'SELECT * FROM table_book_kind WHERE key_name = \'' + kws['name'] + '\';'
        elif kws.has_key('clc'):
            sql = 'SELECT * FROM table_book_kind WHERE key_clc = \'' + kws['clc'] + '\';'
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        book_list = []
        for row in rows:
            _book = book.Book()
            _book.isbn = row[0]
            _book.clc = row[1]
            _book.name = row[2]
            _book.auth = row[3]
            _book.publisher = row[4]
            _book.edition = row[5]
            _book.publish_date = row[6]
            _book.imgs = row[7]
            book_list.append(_book)
        return book_list

    '''
    功能：查询可用书
    输入：queryBook(ISBN)
    输出：BOOK INSTANCE LIST
    '''
    @classmethod
    def queryBook(cls, isbn):
        sql = 'SELECT * FROM table_book_instance WHERE key_isbn = \'' + isbn + '\';'
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        book_list = []
        for row in rows:
            _book_instance = book.BookInstance()
            _book_instance.uuid = row[0]
            _book_instance.isbn = row[1]
            _book_instance.status = row[2]
            _book_instance.opt_id = row[3]
            book_list.append(_book_instance)

        return book_list


    '''
    功能：添加书
    输入：addBook(_book)
    输出：True/False
    '''
    @classmethod
    def addBook(cls, _book):
        sql = 'SELECT key_name FROM table_book_kind WHERE key_isbn = \'' + _book.isbn + '\';'
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        # if this kind book not in records, record it
        if (rows):
            pass
        else:
            sql = 'INSERT INTO table_book_kind (key_isbn, key_clc, key_name, key_auth, key_publisher, key_edition, key_publish_date, key_imgs) ' \
                  'VALUES (\'' + _book.isbn + '\', \'' + str(_book.clc) + '\', \'' + _book.name + '\', \'{' + str(_book.auth) + '}\', \'' + str(_book.publisher) + '\', ' + str(_book.edition) + ', \'' + str(_book.publish_date) + '\', \'' + str(_book.imgs) + '\');'
            sql = re.sub('\'None\' | None', 'null', sql)
            try:
                cls.__cur.execute(sql)
            except Exception:
                return False
            finally:
                cls.__conn.commit()

        _uuid1 = str(uuid.uuid1())
        _uuid2 = str(uuid.uuid1())
        sql = 'INSERT INTO table_book_instance (key_uuid, key_isbn, key_status, key_opt_id) ' \
              'VALUES (\'' + _uuid1 + '\', \'' + _book.isbn + '\', \'a---\', \'' + _uuid2 + '\');'
        try:
            cls.__cur.execute(sql)
        except Exception:
            return False
        finally:
            cls.__conn.commit()
        return True

    '''
    功能：添加多本书
    输入：addBooks(_book, nums)
    输出：True/False
    '''
    @classmethod
    def addBooks(cls, _book, nums):
        for i in range(nums):
            if (cls.addBook(_book)):
                pass
            else:
                return False
        return True


    '''
    测试创建临时数据
    '''
    @classmethod
    def generateTestData(cls, cur):

        # cur.execute('''CREATE EXTENSION "uuid-ossp"; ''')

        # 存储 UUID
        _uuid = []
        for i in range(10):
            _uuid.append(str(uuid.uuid1()))

        # 初始化表 table_account
        cur.execute('''DROP TABLE IF EXISTS table_account''')
        cur.execute('''CREATE TABLE table_account
                    ( key_uuid          UUID          PRIMARY KEY
                    , key_password      VARCHAR(512)
                    , key_user_name     VARCHAR(64)   UNIQUE
                    , key_first_name    VARCHAR(64)
                    , key_last_name     VARCHAR(64)
                    , key_birthday      DATE
                    , key_register_date DATE
                    , key_balance       NUMERIC(10,2)
                    , key_sex           BOOLEAN
                    , key_tel           BIGINT        UNIQUE NOT NULL CHECK(key_tel > 10000000000 AND key_tel < 20000000000)
                    , key_right         REAL ); ''')
        for i in range(10):

            sql = 'INSERT INTO table_account (key_uuid, key_password, key_user_name, key_tel, key_right) ' \
                  'VALUES (' + '\'' + _uuid[i]  + '\', \'pwd '  + str(i) + '\', \'name ' + str(i) + '\', ' + str(10000000001 + i) + ', ' + str(i%2 + 1) +');'
            cur.execute(sql)

        # 初始化表 table_book_kind
        cur.execute('''DROP TABLE IF EXISTS table_book_kind''')
        cur.execute('''CREATE TABLE table_book_kind
                    ( key_isbn         VARCHAR(20) PRIMARY KEY
                    , key_clc          VARCHAR(20)
                    , key_name         TEXT
                    , key_auth         TEXT[]
                    , key_publisher    VARCHAR(64)
                    , key_edition      INTEGER
                    , key_publish_date DATE
                    , key_imgs         BYTEA); ''')
        for i in range(20):
            sql = 'INSERT INTO table_book_kind (key_isbn, key_name, key_auth, key_publisher, key_edition) ' \
                  'VALUES (' + '\'ISBN ' + str(i) + '\', \'bookname ' + str(i%4) + '\', \'{auth ' + str(i) + '}\', \'publisher ' + str(i) + '\',' + str(i%7) + ');'
            cur.execute(sql)
            # cls.__conn.commit()

        # for i in range(10):
        #     sql = 'INSERT INTO table_book_kind (key_isbn, key_name, key_auth, key_publisher, key_edition) ' \
        #           'VALUES (' + '\'ISBN ' + str(i) + '\', \'bookname ' + str(i) + '\', \'{auth ' + str(i) + '}\', \'publisher ' + str(i) + '\',' + str(i*20) + ');'
        #     cur.execute(sql)
        #     cls.__conn.commit()



        # 初始化表 table_book_instance
        cur.execute('''DROP TABLE IF EXISTS table_book_instance''')
        cur.execute('''CREATE TABLE table_book_instance
                    ( key_uuid   UUID PRIMARY KEY
                    , key_isbn   VARCHAR(20)
                    , key_status VARCHAR(4)  -- aubr
                    , key_opt_id UUID NULL); ''')
        for i in range(8):
            temp_uuid = str(uuid.uuid1())
            sql = 'INSERT INTO table_book_instance (key_uuid, key_isbn, key_status, key_opt_id) ' \
                  'VALUES (\'' + _uuid[i] + '\', \'ISBN ' + str(i) + '\', \'a---\', \'' + temp_uuid + '\');'
            cur.execute(sql)

        # 初始化表 table_book_operation
        cur.execute('''DROP TABLE IF EXISTS table_book_operation''')
        cur.execute('''CREATE TABLE table_book_operation
                    ( key_uuid UUID PRIMARY KEY
                    , key_return_date DATE[]
                    , key_status VARCHAR(4) ); ''')
        for i in range(5):
            temp_time = str(datetime.datetime.now())
            sql = 'INSERT INTO table_book_operation (key_uuid, key_return_date, key_status) ' \
                  'VALUES (\'' + _uuid[i] + '\', \'{' + temp_time + '}\', \'a---\');'
            cur.execute(sql)

        cls.__conn.commit()
