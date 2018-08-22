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

@app.route('/')
@restful(query=params)
def index_get(args):
    return args['a'] + args['b']

@app.route('/',methods=['POST'])
@restful(body=User,
         required=[User.password, User.username, User.age])
def index(user):
    user.id = str(uuid.uuid4())
    db.session.add(user)
    db.session.commit()
    return user.to_dict()

@app.route('/test/<int:id>')
@restful()
def test(id):
    return id