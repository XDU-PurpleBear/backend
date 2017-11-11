# -*- coding:utf-8 -*-
'''
Created on 2017年10月16日

@author: lenovo
'''
import logiclayer as X
import datetime
import uuid
        
def testSignup(token):
    info = {
        'token':token,
        'newUser':{
            "userName": "userName",
            "studentID": "14130120123",
            "balance": "20",
            "deposit": "300",
            "password": "password",
            "tel": "12312345678"
        }
    }
    fromX = X.signup(info)
    print fromX
    print '-------------------------------------------------'

def testLogin(right):
    blockInfos = {
        'librarian':{
            'type':'tel',
            'value':'15932881235',
            'password':'pw111'
        },
        'reader':{
            'type':'tel',
            'value':'15932881234',
            'password':'pw111'
        },
        'reader1':{
            'type':'stuid',
            'value':'14130120123',
            'password':'123456'
        }
    }
    fromX = X.login(blockInfos[right])
    # print fromX
    print '-------------------------------------------------'
    return fromX
    
def testLogout(token):
    logoutBlock = {'token':token}
    fromX = X.logout(logoutBlock)
    # print fromX

def testSearchUserInfo(token):
    info = {'token':token}
    fromX = X.searchUserInfo(info)
    print fromX
    
def testSearchUserInfoAdmin(token):
    info = {
        'token':token,
        'stuid':'14130120123'
    }
    fromX = X.searchUserInfoAdmin(info)
    print fromX
    
def testEditUserInfoAdmin(token):
    info = {
        'token':token,
        'balance':"500",
        'password':'123456',
        'uuid':'c3a3b5cf-c60d-11e7-a8ac-f0761c0b1ebc'
    }
    fromX = X.editUserInfo(info)
    print fromX
    
def testAddBookByDB():
    bookInfo = {}
    bookInfo['isbn'] = 'isbn 4'
    bookInfo['lc'] = 'ZA0000'
    bookInfo['name'] = 'Book Name'
    bookInfo['auth'] = ['auth1', 'auth2']
    bookInfo['publisher'] = 'p1'
    bookInfo['edition'] = 1
    bookInfo['imgs'] = str(uuid.uuid1())
    bookInfo['tags'] = ['japanese','italian','data science','arts']
    bookInfo['abstract'] = 'sp'
    print X.Z.addBookInfo(bookInfo)
    
def testSearchBook():
    info = {'type':'tags','value':['arts']}
    fromX = X.searchBook(info)
    print fromX
    
def testSearchBookInfo(token):
    info = {'token':token,'ISBN':'isbn 4'}
    fromX = X.searchBookByISBN(info)
    print fromX
    
def testRecomands():
    # info = {'token':token,'ISBN':'isbn 4'}
    info = {}
    fromX = X.recomends(info)
    print fromX
    
def testSearchHistory(token):
    info = {'token':token}
    fromX = X.searchHistory(info)
    print fromX
    

def testAddCopy(token):
    info = {
        'token':token,
        'ISBN':'isbn 4'
    }
    fromX = X.addBookCopy(info)
    print fromX
    
def testDeleteCopy(token):
    info = {
        'token':token,
        'uuid':'a2c29630-c6d3-11e7-9ea6-f0761c0b1ebc'
    }
    fromX = X.deleteBookCopy(info)
    print fromX
    
def testEditCopy(token):
    info = {
        'token':token,
        'uuid':'a3b64500-c6d3-11e7-974a-f0761c0b1ebc',
        'status':'a---'
    }
    fromX = X.editBookCopy(info)
    print fromX
    
def testAddBook(token):
    info = {
        'token':token,
        'bookInfo':{
            "name": "test 1 for add book",
            "auth": ["xxl", "ycj"],
            "ISBN": "isbn xxl",
            "publisher": "xxlx",
            "CLC": "AN500",
            "version": "0",
            "description": "this is test for add book",
            "language": ["chinese"],
            "theme": ["engineering", "language skills", "life science", "mathematics"],
            "amount": "2",
            "image": str(uuid.uuid1())
        }
    }
    fromX = X.addBook(info)
    print fromX
    
def testApply(token):
    info = {
        'token':token,
        'uuid':'a5fe0df0-c6da-11e7-885d-f0761c0b1ebc'
    }
    fromX = X.apply(info)
    print fromX
    return fromX
    
def testCheckBorrow(token):
    info = {
        'token':token,
        'studentID':'14130120111',
        'uuids':['203485e1-c6db-11e7-a1c4-f0761c0b1ebc']
    }
    fromX = X.checkBorrow(info)
    print fromX,'test'
    
def testCheckReturn(token):
    info = {
        'token':token,
        'studentID':'14130120123',
        'uuids':['b9c9cdb0-c6da-11e7-bf4c-f0761c0b1ebc']
    }
    fromX = X.checkReturn(info)
    print fromX,'test'
    
def testList(token,type):
    info = {
        'token':token
    }
    if type == 'a':
        fromX = X.applyList(info)
    elif type == 'b':
        fromX = X.borrowList(info)
    elif type == 'f':
        fromX = X.finishedList(info)
    elif type == 'o':
        fromX = X.overdueList(info)
    elif type == 'i':
        fromX = X.invalidList(info)
    else:
        fromX = 'test'
    print fromX
    
def testAgreeBorrow(token):
    info = {
        'token':token,
        'uuid':'757df0ee-c6f3-11e7-980f-f0761c0b1ebc'
    }
    fromX = X.agreeBorrow(info)
    print fromX
    
def testReturnBook(token):
    info = {
        'token':token,
        'uuid':'a32fb111-c6ed-11e7-8c3a-f0761c0b1ebc',
        'balance':'300'
    }
    fromX = X.returnBook(info)
    print fromX

def testRefuseBorrow(token):
    info = {
        'token':token,
        'uuid':'a400a030-c6ee-11e7-be5e-f0761c0b1ebc'
    }
    fromX = X.agreeBorrow(info)
    print fromX
    
def testGetOrder():
    info = 'dcfd8b9e-c6df-11e7-9623-f0761c0b1ebc'
    fromX = X.searchOrderInfo(info)
    print fromX
    
if __name__ == '__main__':
    
    # X.Z.initUsers()
    X.Z.setConnDefalt()
    token = testLogin('librarian')['token']
    # token = testLogin('reader')['token']
    # token = testLogin('reader1')['token']
    # testSignup(token)
    # testSearchUserInfoAdmin(token)
    # testEditUserInfoAdmin(token)
    # testAddBookByDB()
    # testSearchUserInfo(token)
    # testSearchBook()
    # testSearchBookInfo(token)
    # testRecomands()
    # testSearchHistory(token)
    # testAddBook(token)
    # testApply(token)
    # testAddCopy(token)
    # testDeleteCopy(token)
    # testEditCopy(token)
    # testAddBook()
    # testGetOrder()
    # testCheckBorrow(token)
    # testCheckReturn(token)
    # testList(token,'a')
    # testList(token,'b')
    # testList(token,'f')
    # testList(token,'o')
    # testList(token,'i')
    # testAgreeBorrow(token)
    # testRefuseBorrow(token)
    # testReturnBook(token)
    testLogout(token)
    
