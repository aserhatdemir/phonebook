import google as google
from google.cloud import firestore

from stores.store import Store


class FireStore(Store):

    def __init__(self):
        self.db = None
        self.contacts_ref = None
        self.fields = ['name', 'surname', 'email', 'phone']
        self.connect_to_firestore()

    # Class specific methods
    def connect_to_firestore(self):
        self.db = firestore.Client.from_service_account_json('/Users/serhat/PycharmProjects/'
                                                        'python-firestore-cfaa14f93b17.json')

        try:
            self.contacts_ref = self.db.collection(u'contacts')
        except google.cloud.exceptions.NotFound:
            print('Could not connect to Firestore!!')

    def print_contact(self, cont):
        pass

    # increment the last character of string with 1
    def find_key_limit(self, search_key):
        str_len = len(search_key)
        last_char = search_key[str_len - 1]
        x = chr(ord(last_char) + 1)
        key_limit = search_key[:str_len - 1] + x
        return key_limit

    # Inherited methods
    def save_contact(self, name=None, surname=None, email=None, phone=None):
        new_contact_ref = self.contacts_ref.document()
        new_contact_ref.set({
            u'name': name,
            u'surname': surname,
            u'email': email,
            u'phone': phone
        })
        doc = new_contact_ref.get()
        con = {doc.id: doc.to_dict()}
        return con

    def delete_contact(self, idx):
        document_to_delete = self.find_contact_by_id(idx)
        self.contacts_ref.document(idx).delete()
        return document_to_delete

    def update_contact(self, contact):
        if self.find_contact_by_id(contact['id']):
            doc_ref = self.contacts_ref.document(contact['id'])
            data = {
                u'name': contact['name'],
                u'surname': contact['surname'],
                u'email': contact['email'],
                u'phone': contact['phone']
            }
            doc_ref.set(data)
        return self.find_contact_by_id(contact['id'])

    def find_contact_by_id(self, idx):
        doc_ref = self.contacts_ref.document(idx)
        doc = doc_ref.get()
        if doc.to_dict():
            return {doc.id: doc.to_dict()}
        return None

    def find_contact(self, search_key):
        if search_key is None:
            return None
        key_limit = self.find_key_limit(search_key)
        found_contacts = {}
        order = {}
        # search for each field and increment document id value with 1 for each match
        for field in self.fields:
            query = self.contacts_ref.where(field, u'>=', search_key).where(field, u'<', key_limit)
            docs = query.stream()
            for doc in docs:
                found_contacts[doc.id] = doc.to_dict()
                if doc.id in order:
                    order[doc.id] += 1
                else:
                    order[doc.id] = 1

        if len(found_contacts) > 0:
            # order the result according to most match
            ordered = sorted(order.items(), key=lambda x: x[1], reverse=True)
            contacts_view = []
            # print(ordered)
            for o in ordered:
                contacts_view.append({'id': o[0],
                                      'name': found_contacts[o[0]]['name'],
                                      'surname': found_contacts[o[0]]['surname'],
                                      'email': found_contacts[o[0]]['email'],
                                      'phone': found_contacts[o[0]]['phone']})
            return contacts_view
            # return found_contacts
        return None

    def print_all_contacts(self):
        docs = self.contacts_ref.stream()
        contacts_view = {}
        for doc in docs:
            contacts_view[doc.id] = doc.to_dict()
        if len(contacts_view) > 0:
            return contacts_view
        return None

    def quit(self):
        pass
