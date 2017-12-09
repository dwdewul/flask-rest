from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

STORES = [
    {
        'name': 'my_store',
        'items': [
            {
                'name': 'piano_wire',
                'price': 399.06
            }
        ]
    }
]

@app.route('/')
def index():
    """The home route"""
    return render_template('index.html')

@app.route('/store', methods=['POST'])
def create_store():
    request_data = request.get_json()
    new_store = {
        'name': request_data['name'],
        'items': []
    }
    STORES.append(new_store)
    return jsonify(new_store)

@app.route('/store/<string:name>/item', methods=['POST'])
def create_store_item(name):
    request_data = request.get_json()
    for store in STORES:
        if store['name'] == name:
            new_item = {
                'name': request_data['name'],
                'price': request_data['price']
            }
            store['items'].append(new_item)
            return jsonify(new_item)
    return jsonify({'error': 'could not add item to store'})

@app.route('/store')
def get_stores():
    return jsonify({'stores': STORES})

@app.route('/store/<string:name>')
def get_store(name):
    for store in STORES:
        if store['name'] == name:
            return jsonify({'store': store})
    return jsonify({'error': 'store not found'})

@app.route('/store/<string:name>/item')
def get_store_item(name):
    for store in STORES:
        if store['name'] == name:
            return jsonify({'items': store['items']})
    return jsonify({'error': 'store not found'})


if __name__ == '__main__':
    app.run(port=5000)
