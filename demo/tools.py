# -*- coding:utf-8 -*-
'''
Created on 2017Äê11ÔÂ3ÈÕ

@author: lenovo
'''
import datetime
orderStatus = ["Applying", "Borrowing ", "Finished", "Overdue", "Invalid"];
orderStatus = {
    'Applying':'a----',
    'Borrowing':'-b---',
    'Finished':'--f--',
    'Overdue':'---o-',
    'Invalid':'----i',
    'a----':'Applying',
    '-b---':'Borrowing',
    '--f--':'Finished',
    '---o-':'Overdue',
    '----i':'Invalid'
}
theme = ["arts","business", "computer science", "data science", "engineering", "language skills", "life science", "mathematics", "personal development", "physics", "social science"]
language = ['chinese','english','japanese','italian']
bookStatus = {
    'a---':'Available',
    '-u--':'Unavailable',
    '--b-':'Borrowed',
    '---r':'Reserved',
    'Available':'a---',
    'Unavailable':'-u--',
    'Borrowed':'--b-',
    'Reserved':'---r'
}
recomends = ['1','2','3','4','5','6','7','8','9','10']

#location : '103-2'
def divideLocation(location):
    data = location.split('-')
    return {
        'room':data[0],
        'shelf':data[1]
    }

#tags : ['arts']
def divideTags(tags):
    the = []
    lan = []
    for tag in tags:
        if tag in the:
            the.append(tag)
        elif tag in lan:
            lan.append(tag)
        else:
            pass
    return {
        'language':lan,
        'theme':the
    }

def changeBookStatus(status):
    return bookStatus[status]
  
def getRecomends(count):
    ret = []
    for i in range(count):
        if recomends[i] in ret:
            i -= 1
        ret.append(recomends[i])
  
def getRecomend():
    import random
    r = random.randint(0, len(recomends)-1)
    return recomends[r]
    
def getMinus(a,b):
    da = datetime.datetime.strptime(a,'%Y-%m-%d %H:%M:%S %f')
    db = datetime.datetime.strptime(b,'%Y-%m-%d %H:%M:%S %f')
    delta = da - db
    return delta.days