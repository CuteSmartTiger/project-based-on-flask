from flask_restful import Resource,marshal_with,fields,Api
from flask import Flask


app = Flask(__name__)
api=Api(app)


# 此处定义对象，后续return可以返回article对象，而不是字典或者json格式
class Article(object):
    def __init__(self,title,content):
        self.title = title
        self.content = content
article = Article(title='abc',content='sfasdf')




class ArticleView(Resource):


    resource_fields = {
        'title': fields.String,
        'content': fields.String
    }

    # restful规范中，要求，定义好了返回的参数
    # 即使这个参数没有值，也应该返回，返回一个None回去

    # 此处需要使用@marshal_with
    @marshal_with(resource_fields)
    def get(self):
        return article

api.add_resource(ArticleView,'/article/',endpoint='article')


if __name__ == '__main__':
    app.run(debug=True)