import json

from flask import Flask, request
from flask import abort

from stores.file_store import FileStore
from stores.store_factory import store_factory_instance

app = Flask(__name__)

store_factory_instance.register_store('file', FileStore)
store = store_factory_instance.create_store('file')


@app.route('/hello')
def hello():
    return "Hello World!"


@app.route('/contact/<uuid>', methods=['GET'])
def contact(uuid):
    result = store.find_contact_by_id(int(uuid))
    if result:
        return result
    abort(404)


@app.route('/contact', methods=['PUT'])
def add_contact():
    contact = request.get_json()
    return store.save_contact(**contact)


@app.route('/contact/<uuid>', methods=['POST'])
def update_contact(uuid):
    contact = request.get_json()
    contact['id'] = int(uuid)
    result = store.update_contact(contact)
    if result:
        return result
    abort(404)


@app.route('/contact/<uuid>', methods=['DELETE'])
def delete_contact(uuid):
    result = store.delete_contact(int(uuid))
    if result:
        return result
    abort(404)


@app.route('/contact/', methods=['GET'])
def find_contact():
    search_key = request.args.get('q')
    result = store.find_contact(search_key)
    if result:
        return json.dumps(result, indent=4, sort_keys=True)
    abort(404)


# GET /contact -> read all contacts
# GET /contact/3 -> read contact with id 3
# GET /contact/?q=ser -> search start with ser
# POST /contact/3 -> write contact with id=3, contact content given in the body
if __name__ == '__main__':
    app.run()
