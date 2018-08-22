# encoding:utf-8
from functools import wraps
from flask import Flask, jsonify, request
import http
import copy
import logging

app = Flask(__name__)

class User():
    username = ""
    password = ""

# 定义返回字段
response_template = {
    'data': '',
    'code': 0,
    'message': ''
}

def restful(body, required = None):
    def decotator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                json_body = request.json
                e = body()
                for attr in dir(body):
                    data = json_body.get(attr)
                    if data != None:
                        setattr(e, attr, data)
                    else:
                        # 该属性在不能为空的参数列表required中，必须校验客户端提交的该参数值是否为空
                        for i in required:
                            if i is getattr(body, attr):
                                raise BadRequestError("The {} params is not present".format(attr))
                        continue
                data = func(e)
                resp = copy.copy(response_template)
                resp['data'] = data
                resp['code'] = http.HTTPStatus.OK
                return jsonify(resp)
            except UnauthorizedError as e:
                resp = copy.copy(response_template)
                resp['code'] = http.HTTPStatus.UNAUTHORIZED
                resp['message'] = e.args[0]
                return jsonify(resp),http.HTTPStatus.UNAUTHORIZED
            except BadRequestError as e:
                resp = copy.copy(response_template)
                resp['code'] = http.HTTPStatus.BAD_REQUEST
                resp['message'] = e.args[0]
                return jsonify(resp),http.HTTPStatus.BAD_REQUEST
            except RestfulException as e:
                resp = copy.copy(response_template)
                code = e.args[1]
                resp['message'] = e.args[0]
                resp['code'] = code
                return jsonify(resp),code
        return wrapper
    return decotator

class UnauthorizedError(Exception):
    pass

class BadRequestError(Exception):
    pass

class RestfulException(Exception):
    pass

@app.route('/')
@restful
def hello():
    return 'hello'

@app.route('/post',methods=['POST'])
@restful(body=User)
def post(user):
    print(user.username)
    return "ok"

@app.route('/error')
# @restful
def error():
    # raise UnauthorizedError("认证失败")
    # raise BadRequestError("code参数为空")
    raise RestfulException("参数为空", 400)


if __name__ == '__main__':
    app.run(debug=True)