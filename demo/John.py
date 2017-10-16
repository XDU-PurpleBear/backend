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
        right
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
onlineUser = ['name 0']
putAuth = {
    'no_token_input':{
        'status':'error',
        'msg':'need right',
        'status-code':12
        },
    'token_right_wrong':{
        'status':'success',
        'nextExipre':0
        },
    'success':{
                'status':'success',
                'token':0,
                'nextExipre':1666,
                'status-code':0
            }
    }
postAuth = {
    'no_token_input':{
        'status':'error',
        'msg':'need token',
        'status-code':10
        },
    'online_no_token':{
        'status':'success',
        'nextExipre':0
        },
    'system_error':{
            'status':'error',
            'msg':'error',
            'status-code':11
        },
    'success':{
                'status':'success',
                'right':0,
                'nextExipre':1666
            }
    }
deleteAuth = {
    'no_token_input':{
        'status':'error',
        'msg':'need token',
        'status-code':10
        },
    'system_error':{
            'status':'error',
            'msg':'error',
            'status-code':11
        },
    'success':{
                'status':'success',
                'status-code':30
            }
    }
def deleteToken(username):
    if username in onlineUser:
        onlineUser.remove(username)
        retInfo = deleteAuth['success']
    else:
        retInfo = deleteAuth['success']
    return retInfo

def getToken(username):
    onlineUser.append(username)
    retInfo = putAuth['success']
    retInfo['token'] = 100000
    return retInfo

def searchToken(username):
    if username in onlineUser:
        retInfo = postAuth['success']
    else:
        retInfo = postAuth['online_no_token']
    return retInfo
