import json
from pathlib import Path


class Store:
    # file_name = ''
    # contacts = []

    def __init__(self, _file_name):
        self.file_name = _file_name
        self.contacts = []
        self.max_id = 0
        self.load_file()

    def load_file(self):
        my_file = Path(self.file_name)
        if my_file.is_file():
            with open(self.file_name) as json_file:
                self.contacts = json.load(json_file)

    def save(self):
        with open(self.file_name, 'w') as outfile:
            json.dump(self.contacts, outfile)

    def add_save_contact(self, _first_name, _surname, _email, _phone):
        if len(self.contacts) > 0:
            self.max_id = self.get_max_id()
        self.contacts.append({'id': self.max_id + 1, 'name': _first_name, 'surname': _surname, 'email': _email, 'phone': _phone})
        self.save()

    def delete_save_contact(self, _idx):
        self.contacts.pop(_idx)
        self.save()

    def get_max_id(self):
        # return max(max(part.values()) for part in self.contacts)
        # return max(c['id'].values() for c in self.contacts)
        max_id = 0
        for c in self.contacts:
            if c['id'] > max_id:
                max_id = c['id']
        return max_id


my_store = Store('deneme5.json')


def add_contact():
    first_name = input('type name of the contact: ')
    surname = input('type surname of the contact: ')
    email = input('type email address of the contact: ')
    phone = input('type phone number of the contact: ')

    my_store.add_save_contact(first_name, surname, email, phone)


def print_all_contacts():
    for c in my_store.contacts:
        print_contact(c)


def print_contact(cont):
    print('----------------------')
    for attr, val in cont.items():
        print(attr + ': ' + str(val))
    print('----------------------')


def delete_contact():
    idx = int(input('type id of the contact to delete'))
    my_store.delete_save_contact(idx-1)


def find_contact():
    search_key = input('type search keyword: ')
    order = []
    for idx, contact in enumerate(my_store.contacts):
        i = 0
        for attr, val in contact.items():
            if str(val).startswith(search_key):
                i += 1
        if i > 0:
            order.append((i, idx))
            # order.append((i, my_store.contacts.index(contact)))

    if len(order) == 0:
        input('no such contact, type again: ')
        return
    order.sort(reverse=True)
    for o in order:
        print(o[0], my_store.contacts[o[1]])


def update_contact():
    pass


# def search_dictionaries(key, value, list_of_dictionaries):
#     return [element for element in list_of_dictionaries if element[key] == value]


def main():

    while True:
        choice = input('type "a" to add a contact...\n'
                       'type "d" to delete a contact...\n'
                       'type "u" to update a contact...\n'
                       'type "f" to find a contact...\n'
                       'type "p" to print all contacts...\n'
                       'type "q" to quit...\n\n')

        if choice == 'a':
            add_contact()
        elif choice == 'd':
            delete_contact()
        elif choice == 'u':
            update_contact()
        elif choice == 'f':
            find_contact()
        elif choice == 'p':
            print_all_contacts()
        elif choice == 'q':
            break
        else:
            print('invalid option!\n')


main()



