#!/usr/bin/env python
# -*- coding: utf-8 -*-


'''
Database operation module.
'''

__author__ = 'Fitzeng'

import datetime
import psycopg2
import re
import uuid


class Database(object):

    @classmethod
    def __init__(cls):
        pass

    @classmethod
    def setConnDefalt(cls):
        _host, _port, _database, _user, _password = '127.0.0.1', '5432', 'purple', 'postgres', 'zzj123'
        cls.setConn(_host, _port, _database, _user, _password)

    @classmethod
    def setConn(cls, _host, _port, _database, _user, _password):
        cls.__conn = psycopg2.connect(host=_host, port=_port, database=_database, user=_user, password=_password)
        cls.__cur = cls.__conn.cursor()

    @classmethod
    def addUser(cls, info):
        currentTime = str(datetime.datetime.now())
        sql = 'INSERT INTO table_account (key_uuid, key_tel, key_user_name, key_password, key_register_date, key_right) ' \
              'VALUES (\'' + str(uuid.uuid1()) + '\', \'' + info['tel'] + '\',\'' + info['username'] + '\', \'' \
              + info['password'] + '\', \'' + currentTime + '\', 1);'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def modifyUserInfo(cls, info):
        sql = 'UPDATE table_account SET ' \
              'key_user_name = \'' + info['username'] + '\', ' \
              'key_first_name = \'' + info['firstname'] + '\', ' \
              'key_last_name = \'' + info['lastname'] + '\', ' \
              'key_birthday = \'' + info['birthday'] + '\', ' \
              'key_sex = ' + info['sex'] + ', ' \
              'key_tel = ' + info['tel'] + ' WHERE key_uuid = \'' + info['uuid']+ '\';'
        sql = re.sub('\'None\' | None', 'null', sql)
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def modifyUserPWD(cls, info):
        sql = 'UPDATE table_account SET ' \
              'key_password = \'' + info['password'] + '\' WHERE key_uuid = \'' + info['uuid']+ '\';'
        sql = re.sub('\'None\' | None', 'null', sql)
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def modifyUserBalance(cls, info):
        sql = 'UPDATE table_account SET ' \
              'key_balance = ' + str(info['balance']) + ' WHERE key_uuid = \'' + info['uuid'] + '\';'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def modifyUserRight(cls, info):
        sql = 'UPDATE table_account SET ' \
              'key_right = ' + str(info['right']) + ' WHERE key_uuid = \'' + info['uuid'] + '\';'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def getUserUUID(cls, info):
        if info['type'] == 'tel':
            sql = 'SELECT key_uuid FROM table_account WHERE key_tel = ' + info['value'] + ';'
        elif info['type'] == 'username':
            sql = 'SELECT key_uuid FROM table_account WHERE key_user_name = \'' + info['value'] + '\';'
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if rows:
           return {'status': 'success', 'uuid': rows[0][0]}
        else:
           return {'status': 'failure', 'errorInfo': 'uuid not exist!'}

    @classmethod
    def getUserPWD(cls, uuid):
        sql = 'SELECT key_password FROM table_account WHERE key_uuid = \'' + uuid+ '\';'
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if (rows):
            return {'status': 'success', 'password': rows[0][0]}
        else:
            return {'status':'failure', 'errorInfo': 'this uuid not exist!'}


    @classmethod
    def getUserInfo(cls, uuid):
        sql = 'SELECT key_user_name, key_first_name, key_last_name, key_birthday, key_balance, key_sex, key_tel, key_right FROM table_account WHERE key_uuid = \'' + uuid + '\';'
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if (rows):
            data = {}
            data['username'] = rows[0][0]
            data['firstname'] = rows[0][1]
            data['lastname'] = rows[0][2]
            data['birthday'] = str(rows[0][3])
            data['balance'] = str(rows[0][4])
            data['sex'] = rows[0][5]
            data['tel'] = str(rows[0][6])
            data['right'] = rows[0][7]
            return {'status': 'success', 'data': data}
        else:
            return {'status': 'failure', 'errorInfo': 'this uuid not exist!'}

    @classmethod
    def searchISBN(cls, info):
        sql = 'SELECT key_isbn FROM table_book_kind '
        if info['type'] == 'clc':
            sql += 'WHERE key_clc = \'' + info['value'] + '\';'
        elif info['type'] == 'name':
            sql += 'WHERE lower(key_name) like \'%' + info['value'].lower() + ' %\';'
        elif info['type'] == 'auth':
            auth = info['value']
            s = ''
            for l in auth:
                s += '.*' + l
            s += '.*'
            t_sql = 'SELECT key_isbn, key_auth FROM table_book_kind'
            cls.__cur.execute(t_sql)
            rows = cls.__cur.fetchall()
            if (rows):
                isbn = []
                for row in rows:
                    if re.compile(s).match(str(row[1])):
                        isbn.append(row[0])
                return {'status': 'success', 'isbn': isbn}
            else:
                return {'status': 'failure', 'errorInfo': 'this kind book not exist!'}
        elif info['type'] == 'publisher':
            sql += 'WHERE lower(key_publisher) like \'%' + info['value'].lower() + '%\';'
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if (rows):
            isbn = []
            for row in rows:
                isbn.append(row[0])
            return {'status': 'success', 'isbn': isbn}
        else:
            return {'status': 'failure', 'errorInfo': 'this kind book not exist!'}

    @classmethod
    def searchBookInfo(cls, isbn):
        sql = 'SELECT key_isbn, key_clc, key_name, key_auth, key_publisher, key_edition, key_publish_date, key_tags, key_snapshot ' \
              'FROM table_book_kind WHERE key_isbn = \'' + isbn + '\';'
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if (rows):
            data = {}
            data['isbn'] = rows[0][0]
            data['clc'] = rows[0][1]
            data['name'] = rows[0][2]
            data['auth'] = rows[0][3]
            data['publisher'] = rows[0][4]
            data['edition'] = rows[0][5]
            data['publish_date'] = str(rows[0][6])
            data['tags'] = rows[0][7]
            data['snapshot'] = rows[0][8]
            return {'status': 'success', 'data': data}
        else:
            return {'status': 'failure', 'errorInfo': 'this isbn not exist!'}

    @classmethod
    def searchPicture(cls, isbn):
        sql = 'SELECT key_imgs FROM table_book_kind WHERE key_isbn = \'' + isbn + '\';'
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if (rows):
            return rows[0][0]
        else:
            return 'this isbn not exist!'

    @classmethod
    def addBookInfo(cls, info):
        info['auth'] = re.sub('\[|\]|\'|\"', '', str(info['auth']))
        info['tags'] = re.sub('\[|\]|\'|\"', '', str(info['tags']))
        # print info['auth']
        # print info['tags']
        sql = 'INSERT INTO table_book_kind (key_isbn, key_clc, key_name, key_auth, key_publisher, key_edition, key_publish_date, key_tags, key_snapshot) ' \
              'VALUES (\'' + info['isbn'] + '\', \'' + info['clc'] + '\', \'' + info['name'] + '\', \'{' + str(info['auth']) + '}\', \'' + info['publisher'] \
              + '\', ' + str(info['edition']) + ', \'' + str(info['publish_date']) + '\', \'{' + str(info['tags']) + '}\', \'' + info['snapshot'] + '\');'
        sql = re.sub('\'None\' | None', 'null', sql)
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def addBookPicture(cls, info):
        sql = 'UPDATE table_book_kind SET ' \
              'key_imgs = \'' + str(info['data']) + '\' WHERE key_isbn = \'' + info['isbn'] + '\';'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def modifyBookInfo(cls, info):
        info['auth'] = re.sub('\[|\]|\'|\"', '', str(info['auth']))
        info['tags'] = re.sub('\[|\]|\'|\"', '', str(info['tags']))
        sql = 'UPDATE table_book_kind SET key_clc = \'' + info['clc'] + '\', key_name = \'' + info['name'] + \
              '\', key_auth = \'{' + str(info['auth']) + '}\', key_publisher = \'' + info['publisher'] + \
              '\', key_edition = ' + str(info['edition']) + ', key_publish_date = \'' + str(info['publish_date']) + \
              '\', key_tags = \'{' + str(info['tags']) + '}\', key_snapshot = \'' + info['snapshot'] + '\' WHERE key_isbn = \'' + info['isbn'] + '\';'

        sql = re.sub('\'None\' | None', 'null', sql)
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def modifyBookPicture(cls, info):
        cls.addBookPicture(info)

    @classmethod
    def searchBookInstance(cls, status, **kws):
        sql = 'SELECT key_uuid, key_isbn, key_opt_id FROM table_book_instance WHERE key_status = \'' + status + '\' AND '
        if kws.has_key('isbn'):
            sql += 'key_isbn = \'' + kws['isbn'] + '\';'
        elif kws.has_key('uuid'):
            sql += 'key_uuid = \'' + kws['uuid'] + '\';'
        elif kws.has_key('optid'):
            sql += 'key_opt_id = \'' + kws['optid'] + '\';'
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if (rows):
            uuid = {}
            for row in rows:
                row_uuid = row[0]
                row_isbn = row[1]
                row_opt_id = row[2]
                uuid[row_uuid] = row_opt_id
                isbn = row_isbn
            return {'status': 'success', 'uuid': uuid, 'isbn': isbn}
        else:
            return {'status': 'failure', 'errorInfo': 'This book not exist!'}

    @classmethod
    def addBookInstance(cls, isbn):
        sql = 'INSERT INTO table_book_instance (key_uuid, key_isbn, key_status) ' \
              'VALUES (\'' + str(uuid.uuid1()) + '\', \'' + isbn + '\', \'a---\');'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def modifyBookInstance(cls, info):
        sql = 'UPDATE table_book_instance SET '
        if info.has_key('uuid'):
            if info.has_key('optid'):
                sql += 'key_opt_id = \'' + info['optid'] + '\' WHERE key_uuid = \'' + info['uuid'] + '\';'
            elif info.has_key('status'):
                sql += 'key_status = \'' + info['status'] + '\' WHERE key_uuid = \'' + info['uuid'] + '\';'
        elif info.has_key('optid'):
            if info.has_key('status'):
                sql += 'key_status = \'' + info['status'] + '\' WHERE key_opt_id = \'' + info['optid'] + '\';'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def searchOperation(cls, uuid):
        sql = 'SELECT key_return_date, key_status FROM table_book_operation WHERE key_uuid = \'' + uuid + '\';'
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if (rows):
            return {'status': 'success', 'returnDate': str(rows[0][0]), 'statuss': rows[0][1]}
        else:
            return {'status': 'failure', 'errorInfo': 'This uuid not exist!'}

    @classmethod
    def addOperation(cls, info):
        info['returnDate'] = re.sub('\[|\]|\'|\"', '', str(info['returnDate']))
        _uuid = str(uuid.uuid1())
        sql = 'INSERT INTO table_book_operation (key_uuid, key_return_date, key_status) ' \
              'VALUES (\'' + _uuid + '\', \'{' + str(info['returnDate']) + '}\', \'' + info['status'] + '\');'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success', 'uuid': _uuid}

    @classmethod
    def modifyOperationDate(cls, info):
        info['returnDate'] = re.sub('\[|\]|\'|\"', '', str(info['returnDate']))
        sql = 'UPDATE table_book_operation SET ' \
              'key_return_date = \'{' + str(info['returnDate']) + '}\' WHERE key_uuid = \'' + info['uuid'] + '\';'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def modifyOperationStatus(cls, info):
        sql = 'UPDATE table_book_operation SET ' \
              'key_status = \'' + info['status'] + '\' WHERE key_uuid = \'' + info['uuid'] + '\';'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def searchOrder(cls, status, **kws):
        t_sql = 'SELECT key_uuid, key_user, key_timestamp, key_book_opt, key_status FROM table_order_list'
        cls.__cur.execute(t_sql)
        rows = cls.__cur.fetchall()
        if (rows):
            uuid = {}
            for row in rows:
                if row[4] == status:
                    t_uuid = {}
                    row_uuid = row[0]
                    row_user_uuid = row[1]
                    row_timestamp = row[2]
                    row_book_opt = row[3]
                    if kws.has_key('uuid'):
                        if kws['uuid'] == row_user_uuid:
                            t_uuid['userUUID'] = row_user_uuid
                            t_uuid['timestamp'] = row_timestamp
                            t_uuid['opt'] = row_book_opt
                    else:
                        t_uuid['userUUID'] = row_user_uuid
                        t_uuid['timestamp'] = row_timestamp
                        t_uuid['opt'] = row_book_opt
                    uuid[row_uuid] = t_uuid
            return {'status': 'success', 'uuid': uuid }
        return {'status': 'failure', 'errorInfo': 'This search condition not exist!'}

    @classmethod
    def addOrder(cls, info):
        info['optid'] = re.sub('\[|\]|\'|\"', '', str(info['optid']))
        info['status'] = re.sub('\[|\]|\'|\"', '', str(info['status']))
        _uuid = str(uuid.uuid1())
        _time = str(datetime.datetime.now())
        sql = 'INSERT INTO table_order_list (key_uuid, key_user, key_timestamp, key_book_opt, key_status) ' \
              'VALUES (\'' + _uuid + '\', \'' + info['userUUID'] + '\', \'' + _time + '\', \'{' + str(info['optid']) + '}\', \'{' + str(info['status']) + '}\');'
        print sql
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success', 'uuid': _uuid}

    @classmethod
    def modifyOrderStatus(cls, info):
        info['status'] = re.sub('\[|\]|\'|\"', '', str(info['status']))
        sql = 'UPDATE table_order_list SET ' \
              'key_status = \'{' + str(info['status']) + '}\' WHERE key_uuid = \'' + info['uuid'] + '\';'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    '''
    创建表
    '''
    @classmethod
    def createTable(cls):
        cur = cls.__cur

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

        # cur.execute('''DROP TABLE IF EXISTS table_book_kind''')
        # cur.execute('''CREATE TABLE table_book_kind
        #                     ( key_isbn         VARCHAR(20) PRIMARY KEY
        #                     , key_clc          VARCHAR(20)
        #                     , key_name         TEXT
        #                     , key_auth         TEXT[]
        #                     , key_publisher    VARCHAR(64)
        #                     , key_edition      INTEGER
        #                     , key_publish_date DATE
        #                     , key_imgs         BYTEA
        #                     , key_tags         TEXT[]
        #                     , key_snapshot     TEXT );''')
        #
        # cur.execute('''DROP TABLE IF EXISTS table_book_instance''')
        # cur.execute('''CREATE TABLE table_book_instance
        #             ( key_uuid   UUID PRIMARY KEY
        #             , key_isbn   VARCHAR(20)
        #             , key_status VARCHAR(4)  -- aubr
        #             , key_opt_id UUID NULL ); ''')
        #
        # cur.execute('''DROP TABLE IF EXISTS table_book_operation''')
        # cur.execute('''CREATE TABLE table_book_operation
        #             ( key_uuid UUID PRIMARY KEY
        #             , key_return_date DATE[]
        #             , key_status VARCHAR(4) ); ''')
        #
        # cur.execute('''DROP TABLE IF EXISTS table_order_list''')
        # cur.execute('''CREATE TABLE table_order_list
        #              ( key_uuid UUID PRIMARY KEY
        #              , key_user UUID NOT NULL
        #              , key_timestamp DATE NOT NULL
        #              , key_book_opt  UUID[]
        #              , key_status VARCHAR[6] ); ''')

        cls.__conn.commit()


    '''
    测试创建临时数据
    '''
    @classmethod
    def generateTestData(cls):
        pass