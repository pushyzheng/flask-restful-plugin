from app import app,db
from .models import User
from flask_resultful_plugin import restful
import uuid

@app.route('/',methods=['POST'])
@restful(body=User,
         required=[User.password, User.username])
def index(user):
    user.id = str(uuid.uuid4())
    db.session.add(user)
    db.session.commit()
    return user.to_dict()