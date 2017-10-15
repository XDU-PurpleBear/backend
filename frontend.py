import X

from flask import Flask,render_template,request,make_response,jsonify
app = Flask(__name__)


@app.route('/api/login',methods=['GET','POST'])

def FrontLogin():
    bodyinfo ={"type":""}
    if request.method == "POST":
        userKey = request.headers.get('userKey')
        password = request.headers.get('password')
        print userKey
        blockInfo = {"userKey":userKey,"password":password}
        fromX = X.login(blockInfo)
        if fromX["Status"]== "Success":
            bodyinfo["type"] = "succeed"
            bodyinfo["data"] = {}
            rsp = make_response(jsonify(bodyinfo))
            rsp.headers['token'] = fromX["token"]
            rsp.headers['tokenDate'] = fromX["tokenDate"]
            rsp.headers['userType'] = fromX["userType"]
            return rsp
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "POST failed!"

    return jsonify(bodyinfo)


@app.route('/api/logout',methods=['GET','POST'])

def FrontLogout():
    bodyinfo ={"type":""}
    if request.method == "POST":
        token = request.headers.get('token')
        print token
        blockInfo = {"token":token}
        fromX = X.logout(blockInfo)
        if fromX["Status"]== "Success":
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
    if request.method == "POST":
        username = request.headers.get('userName')
        tel = request.headers.get('tel')
        password = request.headers.get('password')
        blockInfo ={"username":username,"tel":tel,"password":password}
        fromX = X.signup(blockInfo)
        if fromX["Status"]== "Success":
            bodyinfo["type"]="succeed"
            bodyinfo["data"]={}
        else:
            bodyinfo["type"] = "failed"
            bodyinfo["errorReason"] = fromX["errorInfo"]
    else:
        bodyinfo["type"] = "failed"
        bodyinfo["errorReason"] = "POST failed!"

    return jsonify(bodyinfo)
'''
@app.route('/api/usrinfoModified',methods=['GET','POST'])

def FrontUsrInfoModified():
    if request.method == "POST":
        firstname = request.headers.get('firstname')
        lastname = request.headers.get('lastname')
        birthday = request.headers.get('birthday')
        registerdate = request.headers.get('registerdate')
        balance = request.headers.get('balance')
        sex = request.headers.get('sex')
        telephone = request.headers.get('telephone_number')
        if :
            return "<h1>signup success !</h1>"
        else:
            return "<h1>signup Failure !</h1>"
    else:
        return "<h1>signup Failure !</h1>"
'''

@app.route('/api/book/query',methods=['GET','POST'])

def FrontSearchBook():
    bodyinfo ={"type":""}
    if request.method == "GET":
        bookname = request.args.get('bookname')
        booktype = request.args.get('booktype')
        ISBN = request.args.get('ISBN')
        token = request.headers.get('token')
        blockInfo ={"bookname":bookname,"booktype":booktype,"ISBN":ISBN,"toekn":token}
        fromX = X.searchBook(blockInfo)
        if fromX["Status"] == "Success":
            bodyinfo["type"] = "succeed"
            bodyinfo["data"] = fromX["booklist"]
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




'''

@app.route('/api/api-version',method=['GET','POST'])

def FrontGetApiVersion():
    if request.method == "POST":
        api-version = request.headers.get('api-version')



#def FrontLogin():
    #

#def FrontLogout():
    #

#def FrontSignup():
    #

#def FrontUsrInfoModified():
    #

#def FrontGetApiVersion():
    #

'''
if __name__ == '__main__':
    app.run(debug=True)
