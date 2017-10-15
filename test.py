# -*- coding:utf-8 -*-
'''
Created on 2017年10月16日

@author: lenovo
'''
import func as X
global onlineUser
onlineUser = []

        
def testSignup():
    blockInfos = [{'tel':'17818102925','username':'tttt','password':'1111'},{'tel':'123','username':'zaixia','password':'2222'},{'tel':'1781','username':'u','password':'3'}]
    for blockInfo in blockInfos:
        print 'block->',blockInfo
        fromX = X.signup(blockInfo)
        print fromX
        print '-------------------------------------------------'

def testLogin():
    blockInfos = [{'userKey':'17818102925','password':'1111'},{'userKey':'17818102925','password':'laozitianxiadiyi!'},{'userKey':'1781','password':'3'}]
    for blockInfo in blockInfos:
        print 'block->',blockInfo
        fromX = X.login(blockInfo)
        print fromX
        
        if fromX['Status'] == 'Success':
            name = X.Z.getUserInfo(blockInfo['userKey'])['user_name']
            if name not in onlineUser:
                onlineUser.append(name)
            print onlineUser
        print '-------------------------------------------------'

if __name__ == '__main__':
    
    X.Z.initUsers()
    testLogin()
    #testSignup()
