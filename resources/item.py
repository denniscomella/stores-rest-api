from flask import Flask, request
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser() # belongs to class itself and not an instance, due to lack of "self."
    parser.add_argument('price',  # must contain a 'price' field with type = float
                        type=float,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Every item needs a store ID."
                        ) # must be passed in every instance an item is called, or use **data

    @jwt_required() #requires authorization, can use on any method
    def get(self, name):
        # for item in items:
        #     if item['name'] == name:
        #         return item
        #item = next(filter(lambda x: x['name'] == name, items), None)

        #return {'item': item}, 200 if item else 404

        item = ItemModel.find_by_name(name)

        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post (self, name):
        #if next(filter(lambda x: x['name'] == name, items), None) is not None:
        #    return {'message': f"An item with name '{name}' already exists."}, 400

        # data = request.get_json()

        if ItemModel.find_by_name(name):
            return {'message': f"An item with name '{name}' already exists."}, 400

        data = Item.parser.parse_args()

        #item = {'name': name, 'price': data['price']}
        item = ItemModel(name, data['price'], data['store_id'])

        # items.append(item)
        try:
            #ItemModel.insert(item)
            item.save_to_db()
        except:
            return {'message': "An error occurred inserting the item."}, 500 # Internal Server Error

        return item.json(), 201 #item is in JSON format

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        else:
            return {'message': "Item '{}' did not exist.".format(name)}

        return {'message': "Item '{}' deleted.".format(name)}

    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            try:
                item = ItemModel(name, data['price'], data['store_id']) # **data
            except:
                return {'message': "An error occurred inserting the item."}, 500  # Internal Server Error
        else:
            try:
                item.price = data['price']
            except:
                return {'message': "An error occurred updating the item."}, 500  # Internal Server Error
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.query.all()]} #list comprehension
        # return {'items': [list(map(lambda x: x.json(), ItemModel.query.all()))} # good for users with other languages
         # # you can stack filters using the mapping method