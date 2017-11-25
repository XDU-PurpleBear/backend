# -*- coding:utf-8 -*-
# '''
# Created on 2017年10月15日
#
# @author: lenovo
# '''
#
# import httplib
# import json
#
# def getBookInfo(isbn):
#     path = '/api/v1/isbn/' + isbn
#     # print isbn,'in third'
#     conn = httplib.HTTPConnection('127.0.0.1:3001')
#     conn.request('GET',path)
#     res = conn.getresponse()
#     print res.status,'in third'
#     if res.status == 200:
#         data = json.loads(res.read())
#         # print data
#         data['name'] = data.pop('title')
#         data['auth'] = data.pop('auths')
#         data['imgs'] = data.pop('img-uuid')
#         retinfo = {
#             'status':'success',
#             'data': data
#         }
#     elif res.status == 404:
#         retinfo = {
#             'status':'failure',
#             'errorInfo':'Can not get the book info from third database!'
#         }
#     else:
#         retinfo = {
#             'status':'failure',
#             'errorInfo':'unexpected result!'
#         }
#     return retinfo
#
# def getBookCover(imgid):
#     path = '/api/v1/cover/' + imgid
#     conn = httplib.HTTPConnection('127.0.0.1:3001')
#     conn.request('GET',path)
#     res = conn.getresponse()
#     if res.status == 200:
#         retinfo = {
#             'status':'success',
#             'mime':res.getheader('Content-Type'),
#             'data':res.read()
#         }
#     elif res.status == 404:
#         retinfo = {
#             'status':'failure',
#             'errorInfo':'Can not get the info from third database!'
#         }
#     else:
#         retinfo = {
#             'status':'failure',
#             'errorInfo':'unexpected result!'
#         }
#     return retinfo
#
# if __name__ == '__main__':
#     infos = ['978052169269']
#     print getBookInfo(infos[0])
import douban
def getBookInfo(isbn):
    third = douban.fetch_book_json(isbn)
    if third.has_key('msg') and third['msg'] == 'book_not_found':
        retinfo = {
            'status':'failure',
            'errorInfo':'Can not get the info from third database!'
        }
    else:
        bookinfo = douban.toBook(third).__dict__
        # bookinfo.pop('img')
        retinfo = {
            'status':'success',
            'data':bookinfo
        }
    return retinfo
    # print third,'third'
    # bookinfo = douban.toBook(third)
    # return bookinfo.__dict__

# def getBookCover(imgid):
#
#     if res.status == 200:
#         retinfo = {
#             'status':'success',
#             'mime':res.getheader('Content-Type'),
#             'data':res.read()
#         }
#     elif res.status == 404:
#         retinfo = {
#             'status':'failure',
#             'errorInfo':'Can not get the info from third database!'
#         }
#     else:
#         retinfo = {
#             'status':'failure',
#             'errorInfo':'unexpected result!'
#         }
#     return retinfo
