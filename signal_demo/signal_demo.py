# -*- coding：utf-8 -*-
from flask import Flask,request,g,template_rendered,render_template,got_request_exception
# 从信号导入命令空间
# from blinker import Namespace
# 从文件中导入信号变量
from signals import login_signal


# # 1.定义信号
# lhspace=Namespace()
# fire_signal = lhspace.signal('fire')
#
#
# # 2.监听信号
# def fire_bullet(sender):
#     print(sender)
#     print('start fire bullet')
# fire_signal.connect(fire_bullet)
#
#
# # 3 发送信号
# fire_signal.send()
#
#
# # 定义一个登录的信号，以后用户登录进来以后
# # 就发送一个登录信号，然后能够监听这个信号
# # 在监听到这个信号以后，就记录当前这个用户登录的信息
# # 用信号的方式，记录用户的登录信息

app = Flask(__name__)

# # 渲染模板监听   sender 发送信号者，template为传送的模板名称，context为传送内容
# def template_rendered_func(sender,template,context):
#     print('sender:',sender)
#     print('template:',template)
#     print('context:',context)
# # python中函数加（），表示返回的是一个函数的结果，不加括号表示的是对函数的调用，监听函数运行时的方法，信息动作
# template_rendered.connect(template_rendered_func)


def request_exception_log(sender,*args,**kwargs):
    print(sender)
    print(args)
    print(kwargs)
got_request_exception.connect(request_exception_log)


# 登陆视图函数
@app.route('/login/')
def login():
    # 通过查询字符串的形式来传递username这个参数,以问号的方式在"http://127.0.0.1:5000/login/"输入"?username=liuhu"
    username = request.args.get('username')
    if username:
        # 使用g进行优化,将username传给g函数
        g.username = username
        # 发送信号
        login_signal.send()
        return '登录成功！'
    else:
        return '请输入用户名！'


@app.route('/')
def hello_world():
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True)


# ### Flask内置的信号：
# 1. template_rendered：模版渲染完成后的信号。
# 2. before_render_template：模版渲染之前的信号。
# 3. request_started：模版开始渲染。
# 4. request_finished：模版渲染完成。
# 5. request_tearing_down：request对象被销毁的信号。
# 6. got_request_exception：视图函数发生异常的信号。一般可以监听这个信号，来记录网站异常信息。
# 7. appcontext_tearing_down：app上下文被销毁的信号。
# 8. appcontext_pushed：app上下文被推入到栈上的信号。
# 9. appcontext_popped：app上下文被推出栈中的信号
# 10. message_flashed：调用了Flask的`flashed`方法的信号。