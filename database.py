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
        _host, _port, _database, _user, _password = '127.0.0.1', '5432', 'purple', 'postgres', 'xxl'
        cls.setConn(_host, _port, _database, _user, _password)

    @classmethod
    def setConn(cls, _host, _port, _database, _user, _password):
        cls.__conn = psycopg2.connect(host=_host, port=_port, database=_database, user=_user, password=_password)
        cls.__cur = cls.__conn.cursor()
        # sql = 'INSERT INTO table_account (key_uuid, key_tel, key_user_name, key_password, key_register_date, key_right) ' \
        #       'VALUES (\'' + str(uuid.uuid1()) + '\', \'13772227777\',\'root\', \'root\', \'' + str(datetime.datetime.now()) + '\', 2);'
        # try:
        #     cls.__cur.execute(sql)
        # except Exception, e:
        #     print 'exist!'
        # finally:
        #     cls.__conn.commit()
        # print 'success!'

    @classmethod
    def addUser(cls, info):
        currentTime = str(datetime.datetime.now())
        sql = 'INSERT INTO table_account (key_uuid, key_tel, key_user_name, key_password, key_register_date, key_right, key_balance, key_pledge, key_stu_id) ' \
              'VALUES (\'' + str(uuid.uuid1()) + '\', \'' + info['tel'] + '\',\'' + info['username'] + '\', \'' \
              + info['password'] + '\', \'' + currentTime + '\', 1, ' + str(info['balance']) + ', ' + str(info['pledge']) + ', ' + str(info['stu_id']) + ');'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def deleteUser(cls, uuid):
        sql = 'DELETE FROM table_account WHERE key_uuid = \'' + uuid + '\';'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def modifyLogo(cls, info):
        pass

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
        elif info['type'] == 'stuid':
            sql = 'SELECT key_uuid FROM table_account WHERE key_stu_id = \'' + info['value'] + '\';'
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
        sql = 'SELECT key_user_name, key_stu_id, key_tel, key_logo, key_balance, key_right, key_pledge FROM table_account WHERE key_uuid = \'' + uuid + '\';'
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if (rows):
            data = {}
            data['username'] = rows[0][0]
            data['stuid'] = rows[0][1]
            data['tel'] = rows[0][2]
            data['logo'] = str(rows[0][3])
            data['balance'] = str(rows[0][4])
            data['right'] = rows[0][5]
            data['pledge'] = str(rows[0][6])
            data['uuid'] = uuid
            return {'status': 'success', 'data': data}
        else:
            return {'status': 'failure', 'errorInfo': 'this uuid not exist!'}

    @classmethod
    def addBookInfo(cls, info):
        info['auth'] = re.sub('\[|\]|\'|\"', '', str(info['auth']))
        info['tags'] = re.sub('\[|\]|\'|\"', '', str(info['tags']))
        # print info['auth']
        # print info['tags']
        sql = 'INSERT INTO table_book_kind (key_isbn, key_lc, key_name, key_auth, key_publisher, key_edition, key_imgs, key_tags, key_abstract) ' \
              'VALUES (\'' + info['isbn'] + '\', \'' + info['lc'] + '\', \'' + info['name'] + '\', \'{' + str(
            info['auth']) + '}\', \'' + info['publisher'] \
              + '\', ' + str(info['edition']) + ', \'' + str(info['imgs']) + '\', \'{' + str(
            info['tags']) + '}\', \'' + info['abstract'] + '\');'
        sql = re.sub('\'None\' | None', 'null', sql)
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def deleteBookInfo(cls, isbn):
        sql = 'DELETE FROM table_book_kind WHERE key_isbn = \'' + str(isbn) + '\';'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def modifyBookInfo(cls, info):
        pass

    @classmethod
    def searchISBN(cls, info):
        if info['type'] == 'name':
            sql = 'SELECT key_isbn FROM table_book_kind WHERE lower(key_name) like \'%' + info['value'].lower() + '%\';'
            cls.__cur.execute(sql)
            rows = cls.__cur.fetchall()
            if (rows):
                isbn = []
                for row in rows:
                    isbn.append(row[0])
                return {'status': 'success', 'isbn': isbn}
            else:
                return {'status': 'failure', 'errorInfo': 'this kind book not exist!'}
        elif info['type'] == 'tags':
            t_sql = 'SELECT key_isbn, key_tags FROM table_book_kind'
            cls.__cur.execute(t_sql)
            rows = cls.__cur.fetchall()
            isbn = []
            for row in rows:
                if set(info['value']).issubset(row[1]):
                    isbn.append(row[0])
            if len(isbn) > 0:
                return {'status': 'success', 'isbn': isbn}
            else:
                return {'status': 'failure', 'errorInfo': 'this kind book not exist!'}
        elif info['type'] == 'auth':
            auth = info['value']
            t_sql = 'SELECT key_isbn, key_auth FROM table_book_kind'
            cls.__cur.execute(t_sql)
            rows = cls.__cur.fetchall()
            isbn = []
            for row in rows:
                if set(info['value']).issubset(row[1]):
                    isbn.append(row[0])
            if len(isbn) > 0:
                return {'status': 'success', 'isbn': isbn}
            else:
                return {'status': 'failure', 'errorInfo': 'this kind book not exist!'}
        else:
            return {'status': 'failure', 'errorInfo': 'this kind book not exist!'}

    @classmethod
    def searchBookInfo(cls, isbn):
        sql = 'SELECT key_isbn, key_lc, key_name, key_auth, key_publisher, key_edition, key_imgs, key_tags, key_abstract ' \
              'FROM table_book_kind WHERE key_isbn = \'' + isbn + '\';'
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if (rows):
            data = {}
            data['isbn'] = rows[0][0]
            data['lc'] = rows[0][1]
            data['name'] = rows[0][2]
            data['auth'] = rows[0][3]
            data['publisher'] = rows[0][4]
            data['edition'] = rows[0][5]
            data['imgs'] = rows[0][6]
            data['tags'] = rows[0][7]
            data['abstract'] = rows[0][8]
            return {'status': 'success', 'data': data}
        else:
            return {'status': 'failure', 'errorInfo': 'this isbn not exist!'}

    @classmethod
    def addBookInstance(cls, isbn):
        # xu start
        bookid = str(uuid.uuid1())
        sql = 'INSERT INTO table_book_instance (key_uuid, key_isbn, key_status) ' \
              'VALUES (\'' + bookid + '\', \'' + isbn + '\', \'a---\');'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success','uuid':bookid}
        # xu end

    @classmethod
    def deleteBookInstance(cls, uuid):
        sql = 'DELETE FROM table_book_instance WHERE key_uuid = \'' + uuid + '\';'
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
                if info['optid']:
                    sql += 'key_opt_id = \'' + info['optid'] + '\' WHERE key_uuid = \'' + info['uuid'] + '\';'
                else:
                    sql += 'key_opt_id = null WHERE key_uuid = \'' + info['uuid'] + '\';'
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
    def searchBookInstance(cls, **kws):
        sql = 'SELECT key_uuid, key_isbn, key_opt_id, key_status FROM table_book_instance WHERE '
        if kws.has_key('isbn'):
            if kws['isbn']:
                sql += 'key_isbn = \'' + kws['isbn'] + '\';'
            else:
                sql += 'key_isbn = null;'
        elif kws.has_key('uuid'):
            if kws['uuid']:
                sql += 'key_uuid = \'' + kws['uuid'] + '\';'
            else:
                sql += 'key_uuid = null;'
        elif kws.has_key('optid'):
            if kws['optid']:
                sql += 'key_opt_id = \'' + kws['optid'] + '\';'
            else:
                sql += 'key_opt_id = null;'
        else:
            return {'status': 'failure', 'errorInfo': 'kws error!'}
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if (rows):
            data = {}
            # xu start
            uuids = []
            for row in rows:
                uuid = {}
                # xu end
                uuid['uuid'] = row[0]
                uuid['optid'] = row[2]
                uuid['status'] = row[3]
                uuids.append(uuid)
                isbn = row[1]
            data['isbn'] = isbn
            data['uuids'] = uuids
            return {'status': 'success', 'data': data}
        else:
            return {'status': 'failure', 'errorInfo': 'This book not exist!'}
    # for order_db xu has modify all
    @classmethod
    def addOrder(cls, info):
        _uuid = str(uuid.uuid1())
        _time = str(datetime.datetime.now())
        sql = 'INSERT INTO table_order_list (key_uuid, key_user, key_timestamp, key_bookid, key_status) ' \
              'VALUES (\'' + _uuid + '\', \'' + str(info['userid']) + '\', \'' + _time + '\', \'' + str(
            info['bookid']) + '\', \'' + info['status'] + '\');'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success', 'uuid': _uuid}

    @classmethod
    def deleteOrder(cls, uuid):
        sql = 'DELETE FROM table_order_list WHERE key_uuid = \'' + uuid + '\';'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def modifyOrderStatus(cls, info):
        sql = 'UPDATE table_order_list SET ' \
              'key_status = \'' + str(info['status']) + '\' WHERE key_uuid = \'' + info['uuid'] + '\';'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success', 'uuid': info['uuid']}
        
    @classmethod
    def modifyOrderOptid(cls, info):
        sql = 'UPDATE table_order_list SET ' \
              'key_book_opt = \'' + str(info['optid']) + '\' WHERE key_uuid = \'' + info['uuid'] + '\';'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success', 'uuid': info['uuid']}

    @classmethod
    def searchOrder(cls, **kws):
        if kws.has_key('orderid'):
            if kws.has_key('status'):
                sql = 'SELECT key_uuid, key_user, key_timestamp, key_book_opt, key_bookid, key_status FROM table_order_list ' \
                      'WHERE key_uuid = \'' + str(kws['orderid']) + '\' AND key_status = \'' + kws['status'] + '\';'
            else:
                sql = 'SELECT key_uuid, key_user, key_timestamp, key_book_opt, key_bookid, key_status  FROM table_order_list ' \
                      'WHERE key_uuid = \'' + str(kws['orderid']) + '\';'
        elif kws.has_key('bookid'):
            if kws.has_key('status'):
                sql = 'SELECT key_uuid, key_user, key_timestamp, key_book_opt, key_bookid, key_status FROM table_order_list ' \
                      'WHERE key_bookid = \'' + str(kws['bookid']) + '\' AND key_status = \'' + kws['status'] + '\';'
            else:
                sql = 'SELECT key_uuid, key_user, key_timestamp, key_book_opt, key_bookid, key_status  FROM table_order_list ' \
                      'WHERE key_uuid = \'' + str(kws['orderid']) + '\';'
        elif kws.has_key('userid'):
            if kws.has_key('status'):
                sql = 'SELECT key_uuid, key_user, key_timestamp, key_book_opt, key_bookid, key_status  FROM table_order_list ' \
                      'WHERE key_user = \'' + str(kws['userid']) + '\' AND key_status = \'' + kws['status'] + '\';'
            else:
                sql = 'SELECT key_uuid, key_user, key_timestamp, key_book_opt, key_bookid, key_status  FROM table_order_list ' \
                      'WHERE key_user = \'' + str(kws['userid']) + '\';'
        elif kws.has_key('status'):
            sql = 'SELECT key_uuid, key_user, key_timestamp, key_book_opt, key_bookid, key_status  FROM table_order_list ' \
                      'WHERE key_status = \'' + str(kws['status']) + '\';'
        else:
            return {'status': 'failure', 'errorInfo': 'This search condition not exist!'}
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if rows:
            datas = []
            for row in rows:
                data = {}
                data['orderid'] = row[0]
                data['userid'] = row[1]
                data['bookid'] = row[4]
                data['optid'] = row[3]
                data['timestamp'] = row[2]
                data['status'] = row[5]
                datas.append(data)
            return {'status': 'success', 'data': datas}
        else:
            return {'status': 'success', 'data':[]}

    @classmethod
    def addOperation(cls, info):
        info['date'] = re.sub('\[|\]|\'|\"', '', str(info['date']))
        _uuid = str(uuid.uuid1())
        sql = 'INSERT INTO table_book_operation (key_uuid, key_date, key_status) ' \
              'VALUES (\'' + _uuid + '\', \'{' + str(info['date']) + '}\', \'' + info['status'] + '\');'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success', 'uuid': _uuid}

    @classmethod
    def deleteOperation(cls, uuid):
        sql = 'DELETE FROM table_book_operation WHERE key_uuid = \'' + uuid + '\';'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def modifyOperationDate(cls, info):
        info['date'] = re.sub('\[|\]|\'|\"', '', str(info['date']))
        sql = 'UPDATE table_book_operation SET ' \
              'key_date = \'{' + str(info['date']) + '}\' WHERE key_uuid = \'' + info['uuid'] + '\';'
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
    def searchOperation(cls, uuid):
        sql = 'SELECT key_date, key_status FROM table_book_operation WHERE key_uuid = \'' + uuid + '\';'
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if (rows):
            return {'status': 'success', 'date': str(rows[0][0]), 'statuss': rows[0][1]}
        else:
            return {'status': 'failure', 'errorInfo': 'This uuid not exist!'}

    @classmethod
    def addLocation(cls, info):
        sql = 'INSERT INTO table_location (key_begin, key_end, key_location) ' \
              'VALUES (\'' + info['begin'] + '\', \'' + info['end'] + '\', \'' + info['location'] + '\');'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def deleteLocation(cls):
        pass

    @classmethod
    def modifyLocation(cls):
        pass

    @classmethod
    def searchLocation(cls, lc):
        sql = 'SELECT * FROM table_location;'
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if (rows):
            for row in rows:
                lc = lc.upper()
                # xu start
                temp = lc[0:len(row[0])]
                if cmp(row[0], temp) <= 0 and cmp(temp, row[1]) <= 0:
                    return {'status': 'success', 'location': row[2]}
                # xu end
        return {'status': 'failure', 'errorInfo': 'This location not exist!'}

        # import random
        # r = random.randint(101, 400)
        # if r%10 == 0:
        #     r += 1
        # if r%100 > 70:
        #     r = (r / 100) * 100 + 20 + r % 10
        # elif r%100 > 50:
        #     r = (r / 100) * 100 + 10 + r % 10
        # elif r%100 > 20:
        #     r = (r / 100) * 100 + 0 + r % 10
        # return str(r) + '-' + str(random.randint(1, 8))

    @classmethod
    def addHistory(cls, info):
        sql = 'INSERT INTO table_search_history (key_book, key_user, key_time) ' \
              'VALUES (\'' + info['bookid'] + '\', \'' + str(info['userid']) + '\', \'' + str(datetime.datetime.now()) + '\');'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def deleteHistory(cls):
        pass

    @classmethod
    def modifyHistory(cls):
        pass

    @classmethod
    def searchHistory(cls, uuid):
        if (uuid):
            sql = 'SELECT * FROM table_search_history WHERE key_user = \'' + uuid + '\';'
        else:
            sql = 'SELECT * FROM table_search_history ;'
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if (rows):
            datas = []
            for row in rows:
                data = {}
                data['bookid'] = row[0]
                data['userid'] = row[1]
                data['time'] = str(row[2])
                datas.append(data)
            return {'status': 'success', 'date': datas}
        else:
            return {'status': 'failure', 'errorInfo': 'This uuid not exist!'}

    @classmethod
    def searchAllHistory(cls):
        return cls.searchHistory(None)

    @classmethod
    def addImage(cls, info):
        _uuid = str(uuid.uuid1())
        sql = 'INSERT INTO table_image (key_uuid, key_mime, key_data) ' \
              'VALUES (\'' + _uuid + '\', \'' + str(info['mime']) + '\', \'' + str(info['data']) + '\');'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success', 'uuid': _uuid}

    @classmethod
    def deleteImage(cls, uuid):
        sql = 'DELETE FROM table_image WHERE key_uuid = \'' + uuid + '\';'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def modifyImage(cls, info):
        sql = 'UPDATE table_image SET key_mime = \'' + info['mime'] + '\', key_data = \'' + info['data'] + '\' WHERE key_uuid = \'' + str(info['uuid']) + '\';'
        try:
            cls.__cur.execute(sql)
        except Exception, e:
            return {'status': 'failure', 'errorInfo': str(e)}
        finally:
            cls.__conn.commit()
        return {'status': 'success'}

    @classmethod
    def searchImage(cls, uuid):
        sql = 'SELECT key_mime, key_data FROM table_image WHERE key_uuid = \'' + uuid + '\';'
        cls.__cur.execute(sql)
        rows = cls.__cur.fetchall()
        if (rows):
            data = {}
            data['mime'] = rows[0][0]
            data['data'] = str(rows[0][1])
            return {'status': 'success', 'date': data}
        else:
            return {'status': 'failure', 'errorInfo': 'This uuid not exist!'}


    '''
    创建表
    '''
    @classmethod
    def createTable(cls):
        # cur = cls.__cur
        #
        # cur.execute('''DROP TABLE IF EXISTS table_account''')
        # cur.execute('''CREATE TABLE table_account
        #                   ( key_uuid          UUID          PRIMARY KEY
        #                   , key_password      VARCHAR(512)
        #                   , key_user_name     VARCHAR(64)   UNIQUE
        #                   , key_first_name    VARCHAR(64)
        #                   , key_last_name     VARCHAR(64)
        #                   , key_birthday      DATE
        #                   , key_register_date DATE
        #                   , key_balance       NUMERIC(10,2)
        #                   , key_sex           BOOLEAN
        #                   , key_tel           BIGINT        UNIQUE NOT NULL CHECK(key_tel > 10000000000 AND key_tel < 20000000000)
        #                   , key_right         REAL
        #                   , key_logo          UUID
        #                   , key_pledge        NUMERIC(10,2)
        #                   , key_stu_id        BIGINT       UNIQUE NOT NULL CHECK(key_tel > 10000000000 AND key_tel < 20000000000)
        #                   ); ''')
        #
        # cur.execute('''DROP TABLE IF EXISTS table_book_kind''')
        # cur.execute('''CREATE TABLE table_book_kind
        #                   ( key_isbn         VARCHAR(20) PRIMARY KEY
        #                   , key_lc           VARCHAR(20)
        #                   , key_name         TEXT
        #                   , key_auth         TEXT[]
        #                   , key_publisher    VARCHAR(64)
        #                   , key_edition      INTEGER
        #                   , key_publish_date DATE
        #                   , key_imgs         UUID
        #                   , key_tags         TEXT[]
        #                   , key_abstract     TEXT
        #                   ); ''')
        #
        # cur.execute('''DROP TABLE IF EXISTS table_book_instance''')
        # cur.execute('''CREATE TABLE table_book_instance
        #                   ( key_uuid   UUID PRIMARY KEY
        #                   , key_isbn   VARCHAR(20) -- without the limitation of foreign key
        #                   , key_status VARCHAR(8)  -- aubr
        #                   , key_opt_id UUID NULL  -- without the limitation of foreign key
        #                   ); ''')
        #
        # cur.execute('''DROP TABLE IF EXISTS table_book_operation''')
        # cur.execute('''CREATE TABLE table_book_operation
        #                   ( key_uuid UUID PRIMARY KEY
        #                   , key_date DATE[]
        #                   , key_status VARCHAR(8) -- same to book instance's
        #                   ) ''')
        #
        # cur.execute('''DROP TABLE IF EXISTS table_order_list''')
        # cur.execute('''CREATE TABLE table_order_list
        #                   ( key_uuid UUID PRIMARY KEY
        #                   , key_user UUID NOT NULL
        #                   , key_timestamp DATE NOT NULL
        #                   , key_book_opt  UUID
        #                   , key_status VARCHAR(8)
        #                   ); ''')
        #
        # cur.execute('''DROP TABLE IF EXISTS table_image''')
        # cur.execute('''CREATE TABLE table_image
        #                   ( key_uuid UUID PRIMARY KEY
        #                   , key_mime TEXT NOT NULL
        #                   , key_data BYTEA
        #                   ); ''')
        #
        # cur.execute('''DROP TABLE IF EXISTS table_location''')
        # cur.execute('''CREATE TABLE table_location
        #                   ( key_begin TEXT NOT NULL
        #                   , key_end TEXT NOT NULL
        #                   , key_location TEXT PRIMARY KEY
        #                   ); ''')
        #
        # cur.execute('''DROP TABLE IF EXISTS table_search_history''')
        # cur.execute('''CREATE TABLE table_search_history
        #                   ( key_book VARCHAR(20) NOT NULL
        #                   , key_user UUID NOT NULL
        #                   , key_time TIME NOT NULL
        #                   , PRIMARY KEY (key_book,key_user,key_time)
        #                   ); ''')

        cls.__conn.commit()

    '''
    测试创建临时数据
    '''
    @classmethod
    def generateTestData(cls):
        cls.__cur.execute('''DROP TABLE IF EXISTS table_location''')
        cls.__cur.execute('''CREATE TABLE table_location
                          ( key_begin TEXT NOT NULL
                          , key_end TEXT NOT NULL
                          , key_location TEXT PRIMARY KEY
                          ); ''')

        for line in open("locationdb.txt"):
            if line:
                lst = line.strip('\r\n').split(' ')
                sql = 'INSERT INTO table_location (key_begin, key_end, key_location) ' \
                      'VALUES (\'' + lst[0] +'\', \'' + lst[1] +'\' , \'' + lst[2] + '\');'
                try:
                    cls.__cur.execute(sql)
                except Exception, e:
                    return str(e)
                finally:
                    cls.__conn.commit()




