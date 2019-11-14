import json

from flask import Flask, request
from flask import abort

# from stores.file_store import FileStore
# from stores.db_store import DBStore
from stores.firestore import FireStore
from stores.store_factory import store_factory_instance

app = Flask(__name__)

# store_factory_instance.register_store('file', FileStore)
# store = store_factory_instance.create_store('file')
# store_factory_instance.register_store('db', DBStore)
# store = store_factory_instance.create_store('db')
store_factory_instance.register_store('firestore', FireStore)
store = store_factory_instance.create_store('firestore')


@app.route('/hello')
def hello():
    return "Hello World!"


@app.route('/contacts/', methods=['GET'])
def list_contacts():
    result = store.print_all_contacts()
    if result:
        return result
    abort(404)


@app.route('/contact/<uuid>', methods=['GET'])
def contact(uuid):
    result = store.find_contact_by_id(uuid)
    if result:
        return result
    abort(404)


@app.route('/contact', methods=['PUT'])
def add_contact():
    contact = request.get_json()
    result = store.save_contact(**contact)
    if result:
        return result
    abort(404)


@app.route('/contact/<uuid>', methods=['POST'])
def update_contact(uuid):
    contact = request.get_json()
    contact['id'] = uuid
    result = store.update_contact(contact)
    if result:
        return result
    abort(404)


@app.route('/contact/<uuid>', methods=['DELETE'])
def delete_contact(uuid):
    result = store.delete_contact(uuid)
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
# PUT /contact -> write contact, contact content given in the body, id given by postgresql
# DELETE /contact/3 -> delete contact with id 3

if __name__ == '__main__':
    app.run()
