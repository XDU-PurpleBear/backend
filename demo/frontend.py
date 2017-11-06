# -*- coding: utf-8 -*-

import logiclayer as X

from flask import Flask,render_template,request,make_response,jsonify,json
import time,datetime
app = Flask(__name__)


@app.route('/',methods=['GET'])
def index():
    # _host, _port, _database, _user, _password = '127.0.0.1', '5432', 'purple', 'postgres', 'kgp168668'
    #
    # conn = X.Z.Database.get_database_conn(_host, _port, _database, _user, _password)
    #
    # cur = X.Z.Database.get_cur(conn)

    print '---------------------------------'

    return render_template("index.html")

@app.route('/<path:path>')
def other(path):
    return render_template("index.html")


@app.route('/build/bundle.js',methods=['GET'])

def rest():
    return app.send_static_file('bundle.js')

@app.route('/res/image/mainBackground.jpg',methods=['GET','POST'])
def mainBackground():
    return app.send_static_file("mainBackground.jpg")

@app.route('/api/login',methods=['GET','POST'])

def FrontLogin():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "POST":
        userType = request.headers.get('userType')
        userKey = request.headers.get('userKey')
        password = request.headers.get('password')
        #print userType
        #print userKey
        #print password
        if userType == 'userName':
            userType = 'username'
        blockInfo = {"value":str(userKey),"password":password,"type":userType}
        fromX = X.login(blockInfo)
        print fromX
        if fromX["status"]== "success":

            bodyinfo["type"] = "succeed"
            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))
            rsp.headers['token'] = fromX["token"]
            rsp.headers['tokendate'] = fromX["tokenDate"]
            rsp.headers['usertype'] = fromX["userType"]
            rsp.headers['username'] = fromX["username"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "POST failed!"
    print '--------login--------'
    return jsonify(bodyinfo)


@app.route('/api/logout',methods=['GET','POST'])

def FrontLogout():
    bodyinfo ={"type":""}
    if request.method == "POST":
        token = request.headers.get('token')
        print token
        blockInfo = {"token":token}
        fromX = X.logout(blockInfo)
        if fromX["status"]== "success":
            bodyinfo["type"]="succeed"
            bodyinfo["data"]={}
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "POST failed!"

    return jsonify(bodyinfo)


@app.route('/api/signup',methods=['GET','POST'])
def FrontSignup():
    bodyinfo ={"type":""}
    print "test"
    if request.method == "POST":
        username = request.headers.get('userName')
        tel = request.headers.get('tel')
        password = request.headers.get('password')

        blockInfo ={"username":username,"tel":tel,"password":password}

        print blockInfo

        fromX = X.signup(blockInfo)
        if fromX["status"]== "success":
            time.sleep(1)

            fromXX = X.login({'type':"username",'value':username,"password":password})
            if fromXX["status"]== "success":
                bodyinfo["type"] = "succeed"
                bodyinfo["data"] = {}
                rsp = make_response(jsonify(bodyinfo))
                rsp.headers['token'] = fromXX["token"]
                rsp.headers['tokendate'] = fromXX["tokenDate"]
                rsp.headers['usertype'] = fromXX["userType"]
                rsp.headers['username'] = fromXX["username"]
                return rsp
            else:
                bodyinfo["type"] = "failed"
                bodyinfo["errorReason"] = fromX["errorInfo"]
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "POST failed!"

    return jsonify(bodyinfo)

@app.route('/api/book/query',methods=['GET','POST'])
def FrontSearchBook():
    bodyinfo ={"type":""}
    if request.method == "GET":
        bookname = request.args.get('bookName')
        theme = request.args.get('theme')
        authorName = request.args.get('authorName')
        ISBN = request.args.get('ISBN')

        token = request.headers.get('token')



        if authorName != None:
            blockInfo = {"type":"auth","value":[str(authorName)],"token":token}
        else:
            block ={"name":bookname,"theme":theme,"ISBN":ISBN}
            for key in block:
                if block[key] != None:
                    blockInfo = {"type":key,"value":str(block[key]),"token":token}


        #print blockInfo,'in func'
        fromX = X.searchBook(blockInfo)
        #print 'search in fe',fromX
        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"

            bodyinfo["data"] = fromX["data"]

            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokenDate"):
                rsp.headers['tokenDate'] = fromX["tokenDate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)

@app.route('/api/book/info',methods=['GET','POST'])

def FrontGetBookInfo():
    bodyinfo ={"type":""}
    if request.method == "GET":
        ISBN = request.args.get('ISBN')
        print ISBN

        token = request.headers.get('token')

        blockInfo = {"isbn":ISBN,"token":token}

        fromX = X.searchBookByISBN(blockInfo)
        print blockInfo
        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"

            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))

            if fromX.has_key("tokenDate"):
                rsp.headers['tokenDate'] = fromX["tokenDate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)

@app.route('/api/user/info',methods=['GET','POST'])

def FrontGetUserInfo():
    bodyinfo ={"type":""}
    if request.method == "GET":

        token = request.headers.get('token')

        blockInfo = {"token":token}

        fromX = X.getUserInfo(blockInfo)
        #print blockInfo
        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"

            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))

            if fromX.has_key("tokenDate"):
                rsp.headers['tokenDate'] = fromX["tokenDate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)

@app.route('/api/book/recommend',methods=['GET','POST'])

def FrontRecommend():
    bodyinfo ={"type":""}
    if request.method == "GET":

        token = request.headers.get('token')

        blockInfo = {"token":token}

        fromX = X.recommend(blockInfo)
        #print blockInfo
        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"

            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))

            if fromX.has_key("tokenDate"):
                rsp.headers['tokenDate'] = fromX["tokenDate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)

@app.route('/api/user/queryhistory',methods=['GET','POST'])

def FrontQueryHistory():
    bodyinfo ={"type":""}
    if request.method == "GET":

        token = request.headers.get('token')

        blockInfo = {"token":token}

        fromX = X.searchHistory(blockInfo)
        #print blockInfo
        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"

            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))

            if fromX.has_key("tokenDate"):
                rsp.headers['tokenDate'] = fromX["tokenDate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)

@app.route('/api/user/overduelist',methods=['GET','POST'])

def FrontOverdueList():
    bodyinfo ={"type":""}
    if request.method == "GET":

        token = request.headers.get('token')

        blockInfo = {"token":token}

        fromX = X.searchOverdueOrder(blockInfo)
        #print blockInfo
        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"

            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))

            if fromX.has_key("tokenDate"):
                rsp.headers['tokenDate'] = fromX["tokenDate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)


@app.route('/api/book/add',methods=['GET','POST'])

def FrontAddBook():
    bodyinfo ={"type":""}
    if request.method == "POST":

        token = request.headers.get('token')

        temp = request.data
        #print temp
        print '----------------------------------------'

        frontbody = json.loads(temp)
        #print frontbody
        frontbody["isbn"]=frontbody.pop("ISBN")
        frontbody["clc"]=frontbody.pop("CLC")
        frontbody["snapshot"]=frontbody.pop("description")
        frontbody["edition"]=frontbody.pop("version")
        #frontbody["isbn"]=frontbody.pop("ISBN")
        #frontbody["image"]= frontbody["image"].pop("data")
        frontbody["auth"] = [frontbody.pop("auth")]
        frontbody['tags'] = ["fsdf"]
        #frontbody['publish_date'] =
        frontbody["token"]= token
        frontbody["image"]["data"]=''
        frontbody['publish_date'] = datetime.datetime.now()

        fromX = X.addBookInfoNew(frontbody)
        print "fromx in add book",fromX
        if fromX['status'] == 'success':
            if fromX["tokenDate"] != 0:
                bodyinfo["type"] = "succeed"
                rsp = make_response(jsonify(bodyinfo))
                rsp.headers['tokenDate'] = fromX["tokenDate"]
                return rsp
            else:
                pass
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
            print fromX['errorInfo']
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)


@app.route('/api/book/edit',methods=['GET','POST'])

def FrontEditBook():
    bodyinfo ={"type":""}
    if request.method == "POST":

        token = request.headers.get('token')

        temp = request.data
        #print temp
        print '----------------------------------------'

        frontbody = json.loads(temp)

        frontbody["isbn"]=frontbody.pop("ISBN")
        frontbody["clc"]=frontbody.pop("CLC")
        frontbody["snapshot"]=frontbody.pop("description")
        frontbody["edition"]=frontbody.pop("version")
        #frontbody["isbn"]=frontbody.pop("ISBN")
        frontbody["image"]= frontbody["image"].pop("data")
        frontbody["token"]= token
        frontbody["tags"] = ['']
        frontbody["publish_date"] = datetime.datetime.now()

        fromX = X.editBookInfoNew(frontbody)
        if fromX['status'] == 'success':
            if fromX["tokenDate"] != 0:
                rsp = make_response(jsonify(bodyinfo))
                rsp.headers['tokenDate'] = fromX["tokenDate"]
                return rsp
            else:
                pass
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)
#@app.route('/api/book/delete',methods=['GET','POST'])

@app.route('/api/book/addcopy',methods=['GET','POST'])

def FrontAddCopy():
    bodyinfo ={"type":""}
    if request.method == "POST":

        token = request.headers.get('token')

        temp = request.data
        frontbody = json.loads(temp)
        isbn = frontbody["ISBN"]
        print isbn
        fromX = X.addCopy({'token':token,'isbn':isbn})
        if fromX['status'] == 'success':
            if fromX["tokenDate"] != 0:
                bodyinfo["type"] = "succeed"
                bodyinfo["data"] = {'uuid': fromX["new"]}
                rsp = make_response(jsonify(bodyinfo))
                rsp.headers['tokenDate'] = fromX["tokenDate"]
                return rsp
            else:
                pass
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)




@app.route('/api/book/applylist',methods=['GET','POST'])

def FrontApplyList():
    bodyinfo ={"type":""}
    if request.method == "GET":

        token = request.headers.get('token')
        toX={}
        toX["token"] = token
        toX["status"] = "applying"
        fromX = X.searchUserOrder(toX)
        if fromX['status'] == 'success':
            if fromX["tokenDate"] != 0:
                temp = fromX["data"]["orderlist"]
                booklist =[]

                for order in temp:
                    books = order["booklist"]
                    isbnlist = {}
                    for book in books:
                        Book={}
                        if book['isbn'] in isbnlist.keys():
                            isbnlist[book['isbn']] = isbnlist[book['isbn']] + 1
                            continue
                        else:
                            isbnlist[book['isbn']] = 0
                            Book["ISBN"] = book['isbn']
                            Book["name"] = book["name"]
                            Book["position"] = book["clc"]
                            Book['image'] = book['image']
                            Book['timelimits'] = book['returnDate']
                            booklist.append(Book)
                    for book in booklist:
                        book['amount'] = isbnlist[book['isbn']]
                bodyinfo["type"] = "succeed"
                bodyinfo["data"] = booklist

                rsp = make_response(jsonify(bodyinfo))
                rsp.headers['tokenDate'] = fromX["tokenDate"]
                return rsp
            else:
                pass
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)

@app.route('/api/book/returnlist',methods=['GET','POST'])

def FrontReturnList():
    bodyinfo ={"type":""}
    if request.method == "GET":

        token = request.headers.get('token')
        toX={}
        toX["token"] = token
        toX["status"] = "confirmed"
        fromX = X.searchUserOrder(toX)
        if fromX['status'] == 'success':
            if fromX["tokenDate"] != 0:
                temp = fromX["data"]["orderlist"]
                booklist =[]

                for order in temp:
                    books = order["booklist"]
                    isbnlist = {}
                    for book in books:
                        Book={}
                        if book['isbn'] in isbnlist.keys():
                            isbnlist[book['isbn']] = isbnlist[book['isbn']] + 1
                            continue
                        else:
                            isbnlist[book['isbn']] = 0
                            Book["ISBN"] = book['isbn']
                            Book["name"] = book["name"]
                            Book["position"] = book["clc"]
                            Book['image'] = book['image']
                            Book['timelimits'] = book['returnDate']
                            booklist.append(Book)
                    for book in booklist:
                        book['amount'] = isbnlist[book['isbn']]
                bodyinfo["type"] = "succeed"
                bodyinfo["data"] = booklist

                rsp = make_response(jsonify(bodyinfo))
                rsp.headers['tokenDate'] = fromX["tokenDate"]
                return rsp
            else:
                pass
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)



@app.route('/api/book/borrowlist',methods=['GET','POST'])

def FrontBorrowList():
    bodyinfo ={"type":""}
    if request.method == "GET":

        token = request.headers.get('token')
        toX={}
        toX["token"] = token
        toX["status"] = "borrow"
        fromX = X.searchUserOrder(toX)
        if fromX['status'] == 'success':
            if fromX["tokenDate"] != 0:
                temp = fromX["data"]["orderlist"]
                booklist =[]

                for order in temp:
                    books = order["booklist"]
                    isbnlist = {}
                    for book in books:
                        Book={}
                        if book['isbn'] in isbnlist.keys():
                            isbnlist[book['isbn']] = isbnlist[book['isbn']] + 1
                            continue
                        else:
                            isbnlist[book['isbn']] = 0
                            Book["ISBN"] = book['isbn']
                            Book["name"] = book["name"]
                            Book["position"] = book["clc"]
                            Book['image'] = book['image']
                            Book['timelimits'] = book['returnDate']
                            booklist.append(Book)
                    for book in booklist:
                        book['amount'] = isbnlist[book['isbn']]
                bodyinfo["type"] = "succeed"
                bodyinfo["data"] = booklist

                rsp = make_response(jsonify(bodyinfo))
                rsp.headers['tokenDate'] = fromX["tokenDate"]
                return rsp
            else:
                pass
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)

@app.route('/api/user/apply',methods=['GET','POST'])

def FrontApply():
    bodyinfo ={"type":""}
    if request.method == "POST":
        token = request.headers.get('token')
        temp = request.data
        frontbody = json.loads(temp)
        toX={}
        temp = frontbody["uuids"].pop()
        books = str(temp)
        toX={"token":token,"books":[books]}
        print toX
        fromX = X.addWonderCopy(toX)
        print fromX
        if fromX['status'] == 'success':
            if fromX["tokenDate"] != 0:
                bodyinfo["type"] = "succeed"
                rsp = make_response(jsonify(bodyinfo))
                rsp.headers['tokenDate'] = fromX["tokenDate"]
                return rsp
            else:
                pass
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)





@app.route('/res/image',methods=['GET','POST'])
def FrontGetImage():
    bodyinfo ={"type":""}
    if request.method == "GET":
        ISBN = request.args.get('isbn')
        temp = X.getImage(ISBN)
        if temp["status"] == "success":
            test = temp["image"]
            print type(test)
            rsp = make_response(str(test))
            rsp.headers['Content-Type'] = "image/gif"
            return rsp
        else:
            pass
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = fromX["errorInfo"]

    return bodyinfo






if __name__ == '__main__':
    app.run(debug=True)
