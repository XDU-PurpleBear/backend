# -*- coding:utf-8 -*-
'''
Created on 2017��11��3��

@author: lenovo
'''
import datetime
import re
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
language = ['chinese','english','indian']
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
recomends = ['9780557798193','9781449319793','9780596007973','9789577296467']
lc = ['BD', 'BF', 'JX', 'JZ', 'BC', 'BL', 'BM', 'JV', 'BH', 'JQ', 'BJ', 'JS', 'BT', 'BV', 'BP', 'BQ', 'BR', 'BS', 'JF', 'BX', 'JA', 'JC', 'RT', 'RV', 'RS', 'RX', 'TL', 'RZ', 'RD', 'RE', 'RF', 'RG', 'RA', 'RB', 'RC', 'RL', 'RM', 'RJ', 'RK', 'GV', 'GT', 'D', 'H', 'L', 'GF', 'GE', 'GC', 'GB', 'GA', 'PK', 'JK', 'GN', 'DJK', 'PH', 'JL', 'JN', 'PL', 'PJ', 'HX', 'JJ', 'HS', 'HQ', 'HV', 'VB', 'HT', 'HJ', 'HN', 'HM', 'HB', 'HC', 'HA', 'HF', 'HG', 'HD', 'HE', 'PR', 'PS', 'PQ', 'VF', 'PT', 'KBM', 'PZ', 'PB', 'PC', 'PA', 'PF', 'PG', 'PD', 'PE', 'KBR', 'KBS', 'KBP', 'PN', 'KBT', 'KBU', 'G', 'M', 'K', 'ZA', 'S', 'SB', 'ML', 'MT', 'N', 'UH', 'UE', 'UD', 'UG', 'UF', 'UA', 'UC', 'UB', '\n', 'GR', 'NK', 'NA', 'NB', 'NC', 'ND', 'NE', 'NX', 'KDZ', 'CJ', 'B', 'CN', 'CC', 'CB', 'J', 'PM', 'CE', 'CD', 'TP', 'R', 'V', 'CS', 'CR', 'Z', 'CT', 'KB', 'KG', 'KF', 'KE', 'KH', 'VD', 'SK', 'SH', 'KZ', 'SF', 'KU/KUQ', 'SD', 'DL', 'DJ', 'DK', 'DH', 'DF', 'DG', 'DD', 'DE', 'DB', 'DC', 'DA', 'DX', 'DT', 'DU', 'DR', 'DS', 'DP', 'DQ', 'LF', 'LG', 'LD', 'LE', 'LB', 'LC', 'TX', 'LA', 'TT', 'LJ', 'TS', 'LH', 'TN', 'LT', 'DAW', 'TJ', 'TK', 'TH', 'TF', 'TG', 'TD', 'TE', 'TC', 'TA', 'VA', 'AC', 'VC', 'AE', 'VE', 'AG', 'VG', 'AI', 'VK', 'AM', 'VM', 'AN', 'Q', 'AP', 'AS', 'U', 'AY', 'AZ', 'QP', 'QR', 'P', 'TR', 'QA', 'QC', 'QB', 'QE', 'QD', 'QH', 'QK', 'QM', 'QL', 'T']

#location : '103-2'
def divideLocation(location):
    # print location
    data = location.split('-')
    # print data
    return {
        'room':data[0],
        'shelf':data[1]
    }

#tags : ['arts']
def divideTags(tags):
    the = []
    lan = []
    for tag in tags:
        if tag in theme:
            the.append(tag)
        elif tag in language:
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
    # ret = []
    # for i in range(count):
    #     book = getRecomend()
    #     if book in ret:
    #         i -= 1
    #     else:
    #         ret.append(book)
        # ret.pop(recommends[i])
    ret = recomends[0:count]
    return ret

def getRecomend():
    import random
    r = random.randint(0, len(recomends)-1)
    return recomends[r]

def getMinus(a,b):
    # print a,bif
    da = datetime.datetime.strptime(a,'%Y-%m-%d %H:%M:%S.%f')

    db = datetime.datetime.strptime(b,'%Y-%m-%d %H:%M:%S.%f')
    delta = da - db
    return delta

def checkLanguage(lanlist):
    for one in lanlist:
        if one not in language:
            return False
    return True

def checkTheme(thelist):
    for one in thelist:
        if one not in theme:
            return False
    return True

def checkCLC(clc):
    clc = re.sub('[0-9]|-', '', clc).split(' ')[0]
    if clc not in lc:
        return False
    return True

# if __name__ == '__main__':
#     print lc
