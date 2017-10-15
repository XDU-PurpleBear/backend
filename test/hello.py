from flask import Flask,render_template,request
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/user/<name>")
def user(name):
    return render_template("user.html",name=name)

@app.route("/login",methods = ['GET', 'POST'])
def login():
    if request.method == "POST":
        print request.headers.get('token')
        print request.headers.get('username')
        username = request.form.get('name')
        password = request.form.get('pw')
        if username=="zhangsan" and password=="123":
            return "<h1>welcome, %s !</h1>" %username
        else:
            return "<h1>login Failure !</h1>"
    else:
        return "<h1>login Failure !</h1>"


if __name__ == '__main__':
    app.run(debug=True)
