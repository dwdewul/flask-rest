"""Flask REST API"""
from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity, create_access_token

from security import authenticate, identity

APP = Flask(__name__)
API = Api(APP)
APP.secret_key = "7sz04=77q8^3ui6oq#@o3wqpiwl$&qsw^3n%&pbjd47fzi5sq-"

JWT = JWTManager(APP)

# import views

# STORES = [
#     {
#         'name': 'my_store',
#         'items': [
#             {
#                 'name': 'piano_wire',
#                 'price': 399.06
#             }
#         ]
#     }
# ]

ITEMS = []

class Login(Resource):
    """Login"""
    def post(self):
        """POST Method for logging in"""
        if not request.is_json:
            return {"msg": "Missing JSON in request"}, 400

        # Ensure request has the username and password
        username = request.json.get('username', None)
        password = request.json.get('password', None)

        if not username:
            return {"msg": "Missing username parameter"}, 400

        if not password:
            return {"msg": "Missing password parameter"}, 400

        # authenticate the user name against the password
        # will use bcrypt to check passwords
        user = authenticate(username, password)

        if not user:
            return {"msg": "Bad credentials"}, 401

        # Identity can be any data that is json serializable
        access_token = create_access_token(identity=username)
        return {"JWT_access_token": access_token}, 200


class Item(Resource):
    """Item API endpoints"""
    def get(self, name):
        """Item GET Method"""
        item = next(filter(lambda x: x['name'] == name, ITEMS), None)

        return {'item': item}, 200 if item is not None else 404

    @jwt_required
    def post(self, name):
        """Item POST Method"""
        if next(filter(lambda x: x['name'] == name, ITEMS), None) is not None:
            return {'error': 'Item with that name already exists'}, 400

        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        ITEMS.append(item)
        return item, 201

    @jwt_required
    def delete(self, name):
        """Item DELETE Method"""
        global ITEMS
        items = list(filter(lambda x: x['name'] == name, ITEMS))
        return {'message': 'Item Deleted'}, 200


    @jwt_required
    def put(self, name):
        """Item PUT Method"""
        data = request.get_json()
        item = next(filter(lambda x: x['name'] == name, ITEMS), None)

        if item is None:
            item = {'name': name, 'price': data['price']}
            ITEMS.append(item)
        else:
            item.update(data)

        return item      


class ItemList(Resource):
    """Multiple Items"""
    def get(self):
        """ItemList GET Method"""
        return {'items': ITEMS}

API.add_resource(Item, '/items/<string:name>')
API.add_resource(ItemList, '/items')
API.add_resource(Login, '/login')

if __name__ == '__main__':
    APP.run(port=5000, debug=True)
