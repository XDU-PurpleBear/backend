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

@app.route('/res/icon/user.png',methods=['GET','POST'])

def mainBackground():
    print "user.png"
    return app.send_static_file("user.png")


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
        if userType == 'studentID':
            userType = 'stuid'
        blockInfo = {"value":str(userKey),"password":password,"type":userType}
        fromX = X.login(blockInfo)
        print fromX
        if fromX["status"]== "success":

            bodyinfo["type"] = "succeed"
            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))
            rsp.headers['token'] = fromX["token"]
            rsp.headers['tokendate'] = fromX["tokendate"]
            rsp.headers['usertype'] = fromX["usertype"]
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
    X.Z.setConnDefalt()


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
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    print "test"
    if request.method == "POST":
        userName = request.headers.get('userName')
        studentID = request.headers.get('studentid')
        balance = request.headers.get('balance')
        deposit = request.headers.get('deposit')
        tel = request.headers.get('tel')
        password = request.headers.get('password')
        token = request.headers.get('token')

        newUser ={
        "userName":userName,
        "studentID": studentID,
        "balance": balance,
        "deposit": deposit,
        "password": password,
        "tel": tel
        }

        blockInfo ={"token":token,"newUser":newUser}

        print blockInfo

        fromX = X.signup(blockInfo)
        if fromX["status"]== "success":

            bodyinfo["type"] = "succeed"

            rsp = make_response(jsonify(bodyinfo))
            rsp.headers['tokendate'] = fromX["tokendate"]

            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "POST failed!"

    return jsonify(bodyinfo)

@app.route('/api/book/query',methods=['GET','POST'])
def FrontSearchBook():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "GET":
        bookname = request.args.get('bookName')
        theme = request.args.get('theme')
        authorName = request.args.get('authorName')
        ISBN = request.args.get('ISBN')

        token = request.headers.get('token')



        if authorName != None:
            # print authorName,type(authorName)
            blockInfo = {"type":"auth","value":[authorName],"token":token}
            # print blockInfo
        else:
            block ={"name":bookname,"theme":theme,"ISBN":ISBN}
            for key in block:
                if block[key] != None:
                    blockInfo = {"type":key,"value":block[key].lower(),"token":token}


        # print blockInfo,'in func'
        fromX = X.searchBook(blockInfo)
        #print 'search in fe',fromX
        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"

            bodyinfo["data"] = fromX["data"]

            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
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
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "GET":
        ISBN = request.args.get('ISBN')
        print ISBN

        token = request.headers.get('token')

        blockInfo = {"ISBN":ISBN,"token":token}

        fromX = X.searchBookByISBN(blockInfo)
        print blockInfo
        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"

            bodyinfo["data"] = fromX["data"]



            rsp = make_response(jsonify(bodyinfo))

            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
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
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "GET":

        token = request.headers.get('token')

        blockInfo = {"token":token}

        fromX = X.searchUserInfo(blockInfo)
        #print blockInfo
        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"

            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))

            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
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
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "GET":

        token = request.headers.get('token')

        blockInfo = {"token":token}

        fromX = X.recomends(blockInfo)
        #print blockInfo
        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"

            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))

            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
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
    X.Z.setConnDefalt()
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

            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
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
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "GET":

        token = request.headers.get('token')

        blockInfo = {"token":token}

        fromX = X.overdueList(blockInfo)

        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"

            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))

            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)

@app.route('/api/user/searchinfo',methods=['GET','POST'])

def FrontSearchInfo():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "GET":
        stuid = request.headers.get('studentID')
        token = request.headers.get('token')


        blockInfo = {"token":token,"stuid":stuid}
        print blockInfo
        fromX = X.searchUserInfoAdmin(blockInfo)
        #print blockInfo
        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"

            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)


@app.route('/api/user/editinfo',methods=['GET','POST'])

def FrontEditInfo():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "POST":

        balance = request.headers.get('balance')
        password = request.headers.get('password')
        uuid = request.headers.get('uuid')
        token = request.headers.get('token')
        blockInfo = {"balance":balance,"password":password,"uuid":uuid,"token":token}

        fromX = X.editUserInfo(blockInfo)
        #print blockInfo
        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)

@app.route('/api/book/previewinfo',methods=['GET','POST'])

def FrontPreviewInfo():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "GET":

        token = request.headers.get('token')
        ISBN = request.headers.get('ISBN')

        blockInfo = {"token":token,"ISBN":ISBN}
        # print blockInfo
        fromthird = X.searchBookOnThird(blockInfo)
        # print fromthird
        # thirdimg = X.searchThirdImg(fromthird["data"]['bookInfo']["image"])
        # print thirdimg
        # Ximg = X.addImg({'mime':thirdimg['mime'],'data':thirdimg['data']})

        #print blockInfo
        if fromthird["status"] == "success":
            bodyinfo["type"] = "succeed"
            bookinfo = fromthird['data']['bookInfo']
            bookinfo['image'] = fromthird['data']['bookInfo']['image']
            bodyinfo["data"] = {'bookInfo':bookinfo}

            rsp = make_response(jsonify(bodyinfo))
            if fromthird.has_key("tokendate"):
                rsp.headers['tokendate'] = fromthird["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)



@app.route('/api/book/addcopy',methods=['GET','POST'])

def FrontAddCopy():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "POST":

        token = request.headers.get('token')

        temp = request.data
        frontbody = json.loads(temp)
        ISBN = frontbody["ISBN"]
        #print isbn
        fromX = X.addBookCopy({'token':token,'ISBN':ISBN})

        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"
            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
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
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "POST":

        token = request.headers.get('token')
        name = request.form['name']
        auth = request.form['auth']
        ISBN = request.form['ISBN']
        publisher = request.form['publisher']
        CLC = request.form['CLC']
        version = request.form['version']
        description = request.form['description']
        language = request.form['language'].lower()
        theme = request.form['theme'].lower()
        amount = request.form['amount']

        temptheme =[]
        tempauth = []
        templanguage = []
        if language.find(","):
            temp = language.split(',')
            for i in temp:
                templanguage.append(i.strip())
        if theme.find(","):
            temp = theme.split(',')
            for i in temp:
                temptheme.append(i.strip())

        if auth.find(","):
            temp = auth.split(',')
            for i in temp:
                tempauth.append(i.strip())

        print temptheme,"theme ====="
        print tempauth,"auth ====="

        # print auth,"auth--------------"

        bookInfo = {
        "name":name,
        "auth":tempauth,
        "ISBN":ISBN,
        "publisher":publisher,
        "CLC":CLC,
        "version":version,
        "description":description,
        "language":templanguage,
        "theme":temptheme,
        "amount":amount
        }
        # print bookInfo

        # f = request.files['image']
        # print request.form," ttttt",
        if request.form.has_key('image'):
            imgid = request.form['image'].split('=')[1]
            bookInfo['image'] = imgid

        else:
            f = request.files['image']
            img_ = f.read()
            img_mime = f.content_type
            # print img_
            # print img_mime
            imginfo = {"mime":img_mime,"data":img_}
            Ximg = X.addImg(imginfo)
            bookInfo['image'] = Ximg['uuid']
        # else:
        print bookInfo
        #print isbn
        fromX = X.addBook({'token':token,'bookInfo':bookInfo})

        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"
            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)

@app.route('/api/book/deletecopy',methods=['GET','POST'])

def FrontDeleteCopy():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "POST":

        token = request.headers.get('token')

        temp = request.data
        frontbody = json.loads(temp)
        uuid = frontbody["uuid"]
        #print isbn
        fromX = X.deleteBookCopy({'token':token,'uuid':uuid})

        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)

@app.route('/api/book/editcopy',methods=['GET','POST'])

def FrontEditCopy():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "POST":

        token = request.headers.get('token')

        temp = request.data
        frontbody = json.loads(temp)
        uuid = frontbody["uuid"]
        status = frontbody["status"]
        #print isbn
        fromX = X.editBookCopy({'token':token,'uuid':uuid,'status':status})

        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)

@app.route('/api/user/editimage',methods=['GET','POST'])

def FrontEditImage():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "POST":

        token = request.headers.get('token')

        f = request.files['image']

        img_ = f.read()
        img_mime = f.content_type
        # print img_
        # print img_mime
        imginfo = {"mime":img_mime,"data":img_}
        Ximg = X.addImg(imginfo)

        #print isbn
        fromX = X.editUserImg({'token':token,'imgid':Ximg['uuid']})

        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)




@app.route('/api/user/apply',methods=['GET','POST'])

def FrontUserApply():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "POST":

        token = request.headers.get('token')

        temp = request.data
        frontbody = json.loads(temp)
        uuid = frontbody["uuid"]
        #print isbn
        fromX = X.apply({'token':token,'uuid':uuid})

        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)

@app.route('/api/admin/borrow',methods=['GET','POST'])

def FrontAdminBorrow():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "POST":

        token = request.headers.get('token')

        temp = request.data
        frontbody = json.loads(temp)
        uuid = frontbody["uuid"]
        #print isbn
        fromX = X.agreeBorrow({'token':token,'uuid':uuid})

        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)


@app.route('/api/admin/return',methods=['GET','POST'])

def FrontAdminReturn():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "POST":

        token = request.headers.get('token')

        temp = request.data
        frontbody = json.loads(temp)
        uuid = frontbody["uuid"]
        balance = request.headers.get('newBalance')
        #print isbn
        fromX = X.returnBook({'token':token,'uuid':uuid,'balance':balance})

        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)

@app.route('/api/admin/refuse',methods=['GET','POST'])

def FrontAdminRefuse():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "POST":

        token = request.headers.get('token')

        temp = request.data
        frontbody = json.loads(temp)
        uuid = frontbody["uuid"]
        #print isbn
        fromX = X.refuseBorrow({'token':token,'uuid':uuid})

        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)

@app.route('/api/admin/refuseborrow',methods=['GET','POST'])

def FrontAdminRefuseBorrow():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "POST":

        token = request.headers.get('token')

        temp = request.data
        frontbody = json.loads(temp)
        uuid = frontbody["uuid"]
        #print isbn
        fromX = X.refuseReturn({'token':token,'uuid':uuid})
        print fromX

        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)



@app.route('/api/admin/checkborrow',methods=['GET','POST'])

def FrontAdminCheckBorrow():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "POST":

        token = request.headers.get('token')
        studentID = request.headers.get('studentID')
        uuids = request.headers.get('uuids')

        #print isbn
        fromX = X.checkBorrow({'token':token,'uuids':uuids,'studentID':studentID})

        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"
            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)


@app.route('/api/admin/checkreturn',methods=['GET','POST'])

def FrontAdminCheckReturn():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "POST":

        token = request.headers.get('token')
        studentID = request.headers.get('studentID')
        uuids = request.headers.get('uuids')

        #print isbn
        fromX = X.checkReturn({'token':token,'uuids':uuids,'studentID':studentID})

        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"
            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)

@app.route('/api/user/applylist',methods=['GET','POST'])

def FrontUserApplyList():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "GET":

        token = request.headers.get('token')

        #print isbn
        fromX = X.applyList({'token':token})

        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"
            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)


@app.route('/api/user/returnlist',methods=['GET','POST'])

def FrontUserReturnList():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "GET":

        token = request.headers.get('token')

        #print isbn
        fromX = X.finishedList({'token':token})

        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"
            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)


@app.route('/api/user/borrowlist',methods=['GET','POST'])

def FrontUserBorrowList():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "GET":

        token = request.headers.get('token')

        #print isbn
        fromX = X.borrowList({'token':token})

        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"
            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)


@app.route('/api/user/invalidlist',methods=['GET','POST'])

def FrontUserInvalidList():
    X.Z.setConnDefalt()
    bodyinfo ={"type":""}
    if request.method == "GET":

        token = request.headers.get('token')

        #print isbn
        fromX = X.invalidList({'token':token})

        if fromX["status"] == "success":
            bodyinfo["type"] = "succeed"
            bodyinfo["data"] = fromX["data"]
            rsp = make_response(jsonify(bodyinfo))
            if fromX.has_key("tokendate"):
                rsp.headers['tokendate'] = fromX["tokendate"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "GET failed!"

    return jsonify(bodyinfo)

@app.route('/db/image',methods=['GET','POST'])
def FrontGetImage():
    bodyinfo ={"type":""}
    if request.method == "GET":
        ID = request.args.get('id')
        print request.args
        if ID == None:
            ID = request.args.get('id')

        temp = X.getImage(ID)
        # print '--------------test--------------'
        # print temp
        if temp["status"] == "success":
            test = temp["data"]
            # print '--------------test--------------'
            # print test

            rsp = make_response(str(test['binarydata']))
            rsp.headers['Content-Type'] = test['MIME']
            return rsp
        else:
            pass
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = fromX["errorInfo"]

    return bodyinfo




'''
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
            if fromX["tokendate"] != 0:
                rsp = make_response(jsonify(bodyinfo))
                rsp.headers['tokendate'] = fromX["tokendate"]
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
            if fromX["tokendate"] != 0:
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
                rsp.headers['tokendate'] = fromX["tokendate"]
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
            if fromX["tokendate"] != 0:
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
                rsp.headers['tokendate'] = fromX["tokendate"]
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
            if fromX["tokendate"] != 0:
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
                rsp.headers['tokendate'] = fromX["tokendate"]
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
            if fromX["tokendate"] != 0:
                bodyinfo["type"] = "succeed"
                rsp = make_response(jsonify(bodyinfo))
                rsp.headers['tokendate'] = fromX["tokendate"]
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



'''


if __name__ == '__main__':
    app.run(debug=True)
