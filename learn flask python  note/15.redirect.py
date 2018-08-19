from flask import Flask,request,redirect,url_for

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login/')
def login():
    return '登录页面'

@app.route('/profile/')
def profile():
    # 当？传参获取name属性时，返回个人中心
    name = request.args.get('name')
    if name:
        return '个人中心 %s'%name
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True,port= 8000)
