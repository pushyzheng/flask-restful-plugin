# encoding:utf-8
from app import app
from flask_resultful_plugin import restful
from flask_resultful_plugin.error import *

@app.route('/res/hello')
@restful()
def hello():
    return 'hello'

@app.route('/res/error/1')
@restful()
def res_error():
    raise UnauthorizedError("You don't have admission")

@app.route('/res/error/2')
@restful()
def res_error2():
    raise RestfulException("Not Found", 404)