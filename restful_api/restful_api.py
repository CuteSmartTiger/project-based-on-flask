 from flask import Flask,url_for
from flask_restful import Api,Resource,inputs,reqparse

app = Flask(__name__)
api=Api(app)


class LoginView(Resource):
    # 内容一：基本使用
    # def post(self,username=None):
    #     return {'username':'liuhu'}

    # 内容二：WTForms参数验证
    def post(self):
        # 验证姓名，年龄，性别，手机号
        parse=reqparse.RequestParser()
        parse.add_argument('username',type=str,default='liuziyao',help='姓名参数错误',)
        parse.add_argument('gender',type=str,choices=['male','female','secret'],help='性别参数错误')
        parse.add_argument('age',type=int,help='年龄参数错误')
        parse.add_argument('telephone',type=inputs.regex(r'1[3578]\d{9}'),help='号码参数错误')
        parse.add_argument('home_page',type=inputs.url,help='网上参数错误')
        # 使用inputs中的date，python中的date函数需要传递三个参数
        parse.add_argument('date',type=inputs.date,help='时间参数错误')
        args=parse.parse_args()
        print(args)
        return {'username':'liujiangjun'}

# api.add_resource(LoginView,'/login/<username>','/regist/',endpoint='login')
api.add_resource(LoginView,'/login/',endpoint='login')

#  # 上下文请求
# with app.test_request_context():
#     print(url_for('login',username='hu'))


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
