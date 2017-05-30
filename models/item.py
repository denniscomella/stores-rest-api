from db import db

class ItemModel(db.Model): #inherits from SQLAlchemy
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id = db.Column(db.Integer, db.ForeignKey('stores.id')) # stores.id => table name, column name
    store = db.relationship('StoreModel') # don't have to use a 'join'; finds a store that matches store_id


    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):
        return {'name': self.name, 'price':self.price}

    @classmethod
    def find_by_name(cls, name):
        #do not have to open and close connection (etc.) with SQLAlchemy as we did with sqlite3
        return cls.query.filter_by(name=name).first() # SELECT * FROM items WHERE name=name LIMIT 1
        #returns ItemModel object with traits

    def save_to_db(self): # functions as "update" and "insert" methods
        db.session.add(self) # you can write multiple objects before committing
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
