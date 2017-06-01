import os

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList #imports model FROM resources (required)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///data.db') #works locally and on Heroku with 2 vars
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False # only turns change tracking off for Flask module
app.secret_key = 'poop'
api = Api(app)

jwt = JWT(app, authenticate, identity)  # /auth

# items = [] # unneeded after creation of item.py

api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, "/items")
api.add_resource(StoreList, '/stores')
api.add_resource(UserRegister, '/register') # posts to /register and creates User from user.py

if __name__ == '__main__': # only runs the code if the app.py file is run (not on being imported)
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)