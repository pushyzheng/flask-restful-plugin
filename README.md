# flask-restful-plugin

`flask-restful-plugin`是基于Flask的Restful轻量插件，让开发能够更加简便地进行Restful规范开发。

## Features

- 自动注入查询字符串查询，JSON Body，自动校验的功能

- 自动封装返回数据，自定义返回数据参数的功能

- 实现类似Spring的Controlleradvice注解全局异常处理的功能

## Simple example

直接返回返回数据，让你无需再定义返回的字段：

```python
@app.route('/res/hello')
@restful()
def hello():
    return 'hello'
```

自动注入JSON，并装换成响应的SQLAlchemy对象，并且能够自动校验不为空的字段属性：

```python
@app.route('/',methods=['POST'])
@restful(body=User,
         required=[User.password, User.username, User.age])
def index(user):
    user.id = str(uuid.uuid4())
    db.session.add(user)
    db.session.commit()
    return user.to_dict()
```

返回HTTP错误直接通过抛出异常的方式，简单明了：

```python
@app.route('/res/error/1')
@restful()
def res_error():
    raise UnauthorizedError("You don't have admission")
```

## Contact

[博客](htts://pushy.site)

## License

MIT