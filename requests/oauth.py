from flask import request

BASE_URL="https://api.github.com"

def construct_url(end_point):
    return "/".join([BASE_URL,end_point])

def basic_auth():
    # 基本认证
    response = request.get(construct_url("user"),auth=('Max-Liuhu','max_liuhu@163.com'))
    print(response.text)
    print(response.request.headers)

def basic_oauth():
    headers = {"Authorization":'token  '}
    # user/emails
    response = request.get(construct_url("user/email"),headers=headers)
    print(response.request.headers)
    print(response.text)
    print(response.status_code)


from requests.auth import AuthBase
class GithubAuth(AuthBase):
    def __init__(self,token):
        self.token = token

    def __call__(self,r):
        r.headers["Authorization"] = ''.join(['token',self.token])
        return r


def oauth_advanced():
    auth = GithubAuth('')
    response = request.get.(construct_url('user/emails'),auth=auth)
    print(response.text)