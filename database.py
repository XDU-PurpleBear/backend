# -*- coding:utf-8 -*-
'''
Created on 2017年10月12日

@author: lenovo
'''
from Module import User as U
from Module import Book as B

users = []
books = []

signupNum = 1

def init():
    return
    
def initUsers():
    Sakura = U.User(user_name='Kawaii', first_name='Sakura', last_name='Kinomoto', birthday='2001-4-1',register_date='2009-2-1', balance='100.00', sex='female', tel='04011012', right='1',password='watashiwasakura')
    Xiu = U.User(user_name='Number1', first_name='Xiu', last_name='Ye', birthday='1988-5-29',register_date='2000-1-1', balance='30.00', sex='male', tel='17818102925', right='2',password='laozitianxiadiyi!')
    Chen = U.User(user_name='zaixia', first_name='Liangchen', last_name='Ye', birthday='1996-11-24',register_date='2000-1-1', balance='0.00', sex='male', tel='15919961124', right='2',password='zaixiayeliangchen')
    Nana = U.User(user_name='MissMalanMountain', first_name='Nana', last_name='Xie', birthday='1981-5-6',register_date='1996-11-28', balance='134.00', sex='female', tel='16619810506', right='1',password='wolaogongjiaozhangjie')
    Jie = U.User(user_name='JieMeNa', first_name='Jason', last_name='Zhang', birthday='1982-12-20',register_date='1996-11-28', balance='1000.00', sex='male', tel='18019821220', right='2',password='wodehaizijiaozhangnai')
    Jasper = U.User(user_name='XiaoxiaoChun', first_name='Jasper', last_name='Chen', birthday='2013-7-1',register_date='2013-7-1', balance='888.00', sex='male', tel='13220130701', right='1',password='whereismydaddy')
    Holmes = U.User(user_name='ICanReadYourMind', first_name='Sherlock', last_name='Holmes', birthday='1994-1-6',register_date='2000-1-3', balance='0.00', sex='male', tel='18318540106', right='1',password='doyouknowhowithink?')
    Java = U.User(user_name='test', first_name='Okay', last_name='JS', birthday='1995-5-1',register_date='1995-5-1', balance='10.00', sex='male', tel='18319950501', right='1',password='firstiamthenameofcoffee')
    users.append(Sakura)
    users.append(Xiu)
    users.append(Chen)
    users.append(Nana)
    users.append(Jie)
    users.append(Jasper)
    users.append(Holmes)
    users.append(Java)
    
def initBooks():
    return ''

def modifyUserInfo(user,UUID):
    return {'test':'test'}

def queryBookKind(clc):
    return {'test':'test'}

def queryBook(isbn):
    return {'test':'test'}

def addUser(tel,username,password):
    one = {'Status':'Success'}
    two = {'Status':'Failure','errorInfo':'System error'}
    
    if True:
        retInfo = one
        user = U.User(user_name=username,tel=tel,password=password)
        users.append(user)
    else :
        retInfo = two
    #signupNum = signupNum + 1
    return retInfo

def getPWD(userinput):
    retInfo = {'password':''}
    for user in users:
        u = user.turnDict()
        if u['user_name'] == userinput:
            retInfo['password'] = u['password']
            break
        elif u['tel'] == userinput:
            retInfo['password'] = u['password']
            break
        else:
            pass
    return retInfo

def getPWDByUsername(userinput):
    retInfo = {'password':''}
    for user in users:
        u = user.turnDict()
        
        if u['user_name'] == userinput:
            
            retInfo['password'] = u['password']
            break
    return retInfo

def getPWDByTel(userinput):
    retInfo = {'password':''}
    for user in users:
        u = user.turnDict()
        
        if u['tel'] == userinput:
            retInfo['password'] = u['password']
            break
    return retInfo
 
def getUserUUID(str):
    return {'UUID':'1234556789'}
    
def getUserInfo(userinput): 
    retInfo = {}
    for user in users:
        u = user.turnDict()
        if u['user_name'] == userinput:
            retInfo = u
            break
        elif u['tel'] == userinput:
            retInfo = u
            break
        else:
            pass
    return retInfo
            

