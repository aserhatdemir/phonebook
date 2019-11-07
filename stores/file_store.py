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
    def save_contact(self, _first_name, _surname, _email, _phone):
        if len(self.contacts) > 0:
            self.max_id = self.get_max_id()
        self.contacts.append(
            {'id': self.max_id + 1, 'name': _first_name, 'surname': _surname, 'email': _email, 'phone': _phone})
        self.save_to_file()

    def delete_contact(self, _idx):
        self.contacts.pop(_idx)
        self.save_to_file()

    def update_contact(self, _idx):
        pass

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
        for o in order:
            self.print_contact(self.contacts[o[1]])

    def print_all_contacts(self):
        for c in self.contacts:
            self.print_contact(c)

    def quit(self):
        print('Exiting program')
