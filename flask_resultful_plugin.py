# encoding:utf-8
from functools import wraps
from flask import jsonify, request
import http
import copy
import logging

# 定义返回字段
response_template = {
    'data': '',
    'code': 0,
    'message': ''
}

def restful(body = None, query = None, required = None):
    def decotator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                # 当body不为空，通过POST提交的表单情况
                if body != None:
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
                elif query != None:
                    params = request.args
                    result = {}
                    for k,b in query.items():
                        print(b)
                        value = params.get(k)
                        # 如果该参数是不为空的，并且参数的值为None，则返回400错误
                        if b['required'] and value == None:
                            raise BadRequestError("The {} params is not present".format(k))
                        # 如果有特殊的格式要求，进行转换格式
                        t = b.get('type')
                        if t:
                            result[k] = t(value)
                    data = func(result)
                else:
                    data = func(*args, **kwargs)
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

# 401 错误
class UnauthorizedError(Exception):
    pass

# 400 错误
class BadRequestError(Exception):
    pass

# 父异常
class RestfulException(Exception):
    pass