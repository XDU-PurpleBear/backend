from flask import Flask,render_template,request,make_response
app = Flask(__name__)

@app.route('/api/v1/login',method=['GET','POST'])

def FrontLogin():
    if request.method == "POST":
        username = request.headers.get('username')
        password = request.headers.get('password')
        if :
            rsp = make_response('success')
            rsp.headers['token'] =
            rsp.headers['token_date'] =
            rsp.headers['usertype'] =
            return rsp
        else:
            return "<h1>login Failure !</h1>"
    else:
        return "<h1>login Failure !</h1>"

@app.route('/api/v1/login',method=['GET','POST'])

def FrontLogout():
    if request.method == "POST":
        token = request.headers.get('token')
        #judge
        if:
            return "<h1>logout success !</h1>"
        else:
            return "<h1>logout Failure !</h1>"
    else:
        return "<h1>logout Failure !</h1>"


@app.route('/api/v1/signup',method=['GET','POST'])
def FrontSignup():
    if request.method == "POST":
        username = request.headers.get('username')
        password = request.headers.get('password')
        if :
            return "<h1>signup success !</h1>"
        else:
            return "<h1>signup Failure !</h1>"
    else:
        return "<h1>signup Failure !</h1>"

@app.route('/api/v1/usrinfoModified',method=['GET','POST'])
def FrontUsrInfoModified():
    if request.method == "POST":
        firstname = request.headers.get('firstname')
        lastname = request.headers.get('lastname')
        birthday = request.headers.get('birthday')
        registerdate = request.headers.get('registerdate')
        balance = request.headers.get('balance')
        sex = request.headers.get('sex')
        telephone = request.headers.get('telephone_number')
        right = request.headers.get('right')
        if :
            return "<h1>signup success !</h1>"
        else:
            return "<h1>signup Failure !</h1>"
    else:
        return "<h1>signup Failure !</h1>"

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


if __name__ == '__main__':
    app.run(debug=True)
