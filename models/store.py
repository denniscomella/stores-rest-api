from db import db

class StoreModel(db.Model): #inherits from SQLAlchemy
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic') #links items to store; many items, one store!

    def __init__(self, name):
        self.name = name

    def json(self):
        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}
        # self.items is a query builder (not list) when using lazy='dynamic' above
        # # speed tradeoff between store creation (here it's faster) and items access in table (otherwise)
        pass

    @classmethod
    def find_by_name(cls, name):
        #do not have to open and close connection (etc.) with SQLAlchemy as we did with sqlite3
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1
        #returns ItemModel object with traits
        pass

    def save_to_db(self): # functions as "update" and "insert" methods
        db.session.add(self) # you can write multiple objects before committing
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()