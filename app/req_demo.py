from app import app,db
from .models import User
from flask_resultful_plugin import restful
import uuid

params = {
    'a': {
        'required': True,
        'type': int
    },
    'b': {
        'required': True,
        'type': int
    }
}

# 查询字符串参数注入示例
@app.route('/')
@restful(query=params)
def index_get(args):
    return args['a'] + args['b']

# JSON Body注入示例
@app.route('/',methods=['POST'])
@restful(body=User,
         required=[User.password, User.username, User.age])
def index(user):
    user.id = str(uuid.uuid4())
    db.session.add(user)
    db.session.commit()
    return user.to_dict()

# 路径参数实例（该插件不影响Flask应用本身的路径参数注入）
@app.route('/<int:id>')
@restful()
def path(id):
    return id

# 路径参数和JSON Body共用示例
@app.route('/<int:id>', methods=['POST'])
@restful(body=User)
# 注意：需要将注入的值放在路径参数的前边
def path_post(user,id):
    return "User(id={}, username={})".format(id, user.username)