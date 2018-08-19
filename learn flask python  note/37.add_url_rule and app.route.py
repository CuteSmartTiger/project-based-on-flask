from flask import Flask,url_for

app = Flask(__name__)

# 此处可以看一下route的底层执行代码
# route(self, rule, **options)
@app.route('/',endpoint='index')
def hello_world():
    print(url_for('zhiliao'))
    return 'Hello World!'

def my_list():
    return '我是列表页'

# 以后在使用`url_for`的时候，
# 就要看在映射的时候有没有传递`endpoint`参数，如果传递了，那么就应该使用
# `endpoint`指定的字符串，如果没有传递，那么就应该使用`view_func`的名字。
app.add_url_rule('/list/',endpoint='zhiliao',view_func=my_list)

# app.test_request_context
# 请求上下文
with app.test_request_context():
    print(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
