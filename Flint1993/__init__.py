#1.1
from flask import Flask  
from config import Config

#1.2
from .site.routes import site 
from .authentication.routes import auth 

# #1.3
from Flint1993.models import db as root_db ,login_manager
from Flint1993 import models
from flask_migrate import Migrate #moves data betwen FLASK and DB via .env, stores changes of models as well
#3 make models available to whole 

from Flint1993.models import User

#1.1
app = Flask(__name__)
app.config.from_object(Config)

#1.2
app.register_blueprint(site) #1 site bp init
app.register_blueprint(auth) #1 auth bp init

#1.3
root_db.init_app(app) #3 db init
migrate = Migrate(app,root_db) #3 pass in app and db
login_manager.init_app(app)#3
login_manager.login_view = 'auth.login' #3 specify rte for non authroized user

@login_manager.user_loader #gets id 
def load_user(user_id): #take in user id
    return User.query.get(user_id) #query db table and find user_id and store them in current session
