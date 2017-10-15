# -*- coding:utf-8 -*-
'''
Created on 2017年10月15日

@author: lenovo
'''
'''
POST:
    in:
        token
    out:
        no_token_input:
            {
                'status':'error',
                'msg':'need token',
                'status-code':''
            }
        system_error:
            {
                'status':'error',
                'msg':error,
                'status-code':''
            }
        online_no_token:
            {
                'status':'success',
                'nextExipre':'0'
            }
        success:
            {
                'status':'success',
                'right':,#1，2
                'nextExipre':'0'
            }
PUT:
    in:
        token
    out:
        no_token_input:
            {
                'status':'error',
                'msg':'need right',
                'status-code':''
            }
        token_right_wrong:
            {
                'status':'success',
                'nextExipre':'0'
            }
        success:
            {
                'status':'success',
                'token':,#1，2
                'nextExipre':'0',
                'status-code':''
            }
            
DELETE:
    in:
        token
    out:
        no_token_input:
            {
                'status':'error',
                'msg':'need token',
                'status-code':''
            }
        system_error:
            {
                'status':'error',
                'msg':error,
                'status-code':''
            }
        success:
            {
                'status':'success',
                'status-code':''
            }
'''



import httplib
body = {}
headers = {}
#conn.request('get', '/', body, headers)

def connectionJohn(url):
    conn = httplib.HTTPConnection()
    return