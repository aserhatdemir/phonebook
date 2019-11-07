import json
from pathlib import Path

from stores.store import Store
from stores.store_factory import store_factory_instance


class FileStore(Store):

    # # singleton
    # def __new__(cls):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super().__new__(cls)
    #     return cls.instance

    def __init__(self):
        self.file_name = 'phonebook_file_store.json'
        self.contacts = []
        self.max_id = 0
        self.load_file()

    # Class specific methods
    def load_file(self):
        my_file = Path(self.file_name)
        if my_file.is_file():
            with open(self.file_name) as json_file:
                self.contacts = json.load(json_file)

    def save_to_file(self):
        with open(self.file_name, 'w') as outfile:
            json.dump(self.contacts, outfile)

    def get_max_id(self):
        # return max(max(part.values()) for part in self.contacts)
        # return max(c['id'].values() for c in self.contacts)
        max_id = 0
        for c in self.contacts:
            if c['id'] > max_id:
                max_id = c['id']
        return max_id

    def print_contact(self, cont):
        print('----------------------')
        for attr, val in cont.items():
            print(attr + ': ' + str(val))
        print('----------------------')

    # Inherited methods
    def save_contact(self, name=None, surname=None, email=None, phone=None):
        if len(self.contacts) > 0:
            self.max_id = self.get_max_id()
        contact = {'id': self.max_id + 1, 'name': name, 'surname': surname, 'email': email, 'phone': phone}
        self.contacts.append(
            contact)
        self.save_to_file()
        return contact

    def delete_contact(self, idx):
        con = self.find_contact_by_id(idx)
        if con:
            self.contacts.remove(con)
            self.save_to_file()
        return con

    def find_contact_by_id(self, _idx):
        for c in self.contacts:
            if c['id'] == _idx:
                return c
        return None

    def update_contact(self, contact):
        con = self.find_contact_by_id(contact['id'])
        for attr, val in contact.items():
            con[attr] = val
        self.save_to_file()
        return con

    def find_contact(self, search_key):
        order = []
        for idx, contact in enumerate(self.contacts):
            i = 0
            for attr, val in contact.items():
                if str(val).startswith(search_key):
                    i += 1
            if i > 0:
                order.append((i, idx))
                # order.append((i, my_store.contacts.index(contact)))

        if len(order) == 0:
            print('No contact found!!')
            return
        order.sort(reverse=True)
        result = []
        for o in order:
            self.print_contact(self.contacts[o[1]])
            result.append(self.contacts[o[1]])
        return result

    def print_all_contacts(self):
        for c in self.contacts:
            self.print_contact(c)

    def quit(self):
        print('Exiting program')
