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
import urllib
import json

def addToJohn(data):
    info = {}
    retInfo = {}
    info['data'] = data
    info['method'] = 'PUT'
    John = connectionJohn(info)
    if John['status'] == 'error':
        retInfo['status'] = 'failure'
        if John['msg'] == 'need right':
            retInfo['errorInfo'] = 'need right'
        elif John['msg'] == 'need uuid':
            retInfo['errorInfo'] = 'need uuid'
        else:
            retInfo['errorInfo'] = 'Unexpect operation'
    elif John['status'] == 'success':
        if John.has_key('token'):
            retInfo['token'] = John['token']
            retInfo['tokenDate'] = John['nextExpire']
            retInfo['status'] = 'success'
        else:
            retInfo['errorInfo'] = 'wrong token'
            retInfo['status'] = 'failure'
    else:
        retInfo['status'] = 'failure'
        retInfo['errorInfo'] = 'Unexpect operation'
    return retInfo
    
def searchOnJohn(data):
    info = {}
    retInfo = {}
    info['data'] = data
    info['method'] = 'POST'
    John = connectionJohn(info)
    if John['status'] == 'error':
        retInfo['status'] = 'failure'
        if John['meg'] == 'need token':
            retInfo['errorInfo'] = 'need token'
        else:
            retInfo['errorInfo'] = 'John System Error'
    elif John['status'] == 'success':
        if John.has_key('uuid'):
            retInfo['uuid'] = John['uuid']
            retInfo['right'] = John['right']
            retInfo['tokenDate'] = John['newExpire']
            retInfo['status'] = 'success'
            
        else:
            retInfo['errorInfo'] = 'no user'
            retInfo['status'] = 'failure'
    else:
        retInfo['status'] = 'failure'
        retInfo['errorInfo'] = 'Unexpect operation'
    
    return retInfo
    
def deleteOnJohn(data):
    info = {}
    retInfo = {}
    info['data'] = data
    info['method'] = 'DELETE'
    John = connectionJohn(info)
    if John['status'] == 'error':
        retInfo['status'] = 'failure'
        if John['msg'] == 'need token':
            retInfo['errorInfo'] = 'need token'
        else:
            retInfo['errorInfo'] = 'John System Error'
    elif John['status'] == 'success':
        retInfo['status'] = 'success'
    else:
        retInfo['status'] = 'failure'
        retInfo['errorInfo'] = 'Unexpect operation'
    return retInfo

def connectionJohn(info):
    data = info['data']
    method = info['method']
    conn = httplib.HTTPConnection('127.0.0.1:3000')
    body = urllib.urlencode(data)
    conn.request(method,'/aii/v1/auth' , body, {'user-agent':'uuid-test','Content-Type':'application/x-www-form-urlencoded'})
    fromJohn = json.loads(conn.getresponse().read())
    #print fromJohn
    conn.close()
    return fromJohn
    
if __name__ == '__main__':
    infos = {
        'put':{
            '0':{
                'right':1
            },
            '1':{
                'uuid':'12345'
            },
            '2':{
                'right':1,'uuid':'12345'
            },
            '3':{
                
            }
        },
        'post':{
            '0':{
                'token':''
            },
            '1':{
                'token':'12345'
            },
            '2':{
                'token':'TG0JQ1o50fhEVvnlB4rTasmlyrY2gwNpIIUUtLHoBiNJcIVvDH2AycIYhhQV9oG'
            },
            '3':{
                
            },
        },
        'delete':{
            '0':{
                'token':''
            },
            '1':{
                'token':'12345'
            },
            '2':{
                'token':'TG0JQ1o50fhEVvnlB4rTasmlyrY2gwNpIIUUtLHoBiNJcIVvDH2AycIYhhQV9oG'
            }
        }
    }
    '''
    fromJohn = addToJohn(data)
    
    print fromJohn
    data['token'] = fromJohn['token']
    fromJohn = searchOnJohn(data)
    print fromJohn
    fromJohn = deleteOnJohn(data)
    print fromJohn
    '''