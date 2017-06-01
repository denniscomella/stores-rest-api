from app import app
from db import db

db.init_app(app)

@app.before_first_request # flask method; eliminates need for create_tables.py
def create_tables():
    db.create_all() # creates all "app" stuff above, only tables that it sees (e.g. it's not imported)
 # create_tables was moved from app.py so db is accepted in Heroku