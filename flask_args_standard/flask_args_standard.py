from flask import Flask,render_template,url_for,session
from flask_restful import Api,Resource,reqparse,fields,marshal_with
import config
from exts import db

from models import User,Article,Tag

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
api=Api(app)


# flask-restful表达方式，返回的json数据格式
class ArticleView(Resource):
    resource_fields={
        'title':fields.String,
        'content':fields.String,
        # nested嵌套,({})
        'author':fields.Nested({
            'username':fields.String,
            'email':fields.String
        }),
        # 获取tags信息
        'tags':fields.List(fields.Nested({
            'id':fields.Integer,
            'name':fields.String
        }))
    }
    #
    @marshal_with(resource_fields)
    # 传入author_id参数,这里传入author_id，而不传入tag_id，因为user与article是
    # 一对多的关系，通过article可以获得user属性信息，同时article与tag是多对多，
    # 可以通过中间表获得tag的相关信息
    def get(self,article_id):
        article=Article.query.get(article_id)
        # 查询
        # article.title
        # article.author.username
        return article

# <article_id>不能忘
api.add_resource(ArticleView,'/article/<article_id>',endpoint='article')

# class Article(object):
#     def __init__(self,title,content):
#         self.title = title
#         self.content = content
# article = Article(title='lh',content='test')
#
# class ArticleView(Resource):
#     resource_fields={
#         'title':fields.String,
#         'content':fields.String
#     }
#
#     @marshal_with(resource_fields)
#     def get(self):
#         # return {'title':'---','content':'+++'}
#         return article
#
#
#
# api.add_resource(ArticleView,'/article/',endpoint='article')

# 点击http://127.0.0.1:5000/ 运行，方可执行以下代码，将相关信息导入表中，
# 否则数据库中无法查询到相关信息
@app.route('/')
def hello_world():
    user = User(username='zhiliao', email='xxx@qq.com')
    # author_id不用输入，其为外键，所以导入两个参数
    article = Article(title='abc', content='123')
    article.author = user
    tag1 = Tag(name='前端')
    tag2 = Tag(name='Python')
    article.tags.append(tag1)
    article.tags.append(tag2)
    db.session.add(article)
    db.session.commit()
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
