import json
from pathlib import Path
import argparse


import psycopg2


class Store:

    def save_contact(self, _first_name, _surname, _email, _phone):
        pass

    def delete_contact(self, _idx):
        pass

    def update_contact(self, _idx):
        pass

    def find_contact(self, search_key):
        pass

    def print_all_contacts(self):
        pass

    def quit(self):
        pass


class FileStore(Store):

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


class DBStore(Store):

    def __init__(self):
        self.contacts = []
        self.connection = None
        self.cursor = None
        self.connect_to_db()

    # Class specific methods
    def connect_to_db(self):
        try:
            self.connection = psycopg2.connect(user="serhat",
                                               password="",
                                               host="127.0.0.1",
                                               port="5432",
                                               database="phonebook_db")
            self.cursor = self.connection.cursor()
            print('PostgreSQL connection is opened')

        except (Exception, psycopg2.Error) as error:
            if not self.connection:
                print("Failed to connect to DB", error)

    def disconnect_from_db(self):
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")

    def print_contact(self, cont):
        print('=> Id: {0}, Name: {1}, Surname: {2}, Phone: {3}, Email: {4}'
              .format(cont[4], cont[0], cont[1], cont[2], cont[3]))

    # Inherited methods
    def save_contact(self, _first_name, _surname, _email, _phone):
        postgres_insert_query = """ INSERT INTO contacts (NAME, SURNAME, EMAIL, PHONE) VALUES (%s,%s,%s,%s)"""
        record_to_insert = (_first_name, _surname, _email, _phone)
        self.cursor.execute(postgres_insert_query, record_to_insert)
        self.connection.commit()

    def delete_contact(self, _idx):
        postgres_delete_query = """ DELETE FROM contacts WHERE id = %s"""
        id_to_delete = [_idx]
        self.cursor.execute(postgres_delete_query, id_to_delete)
        self.connection.commit()

    def update_contact(self, _idx):
        pass

    def find_contact(self, search_key):
        postgres_select_query = ("SELECT * "
                                 "FROM contacts "
                                 "WHERE name LIKE '%" + search_key + "%' "
                                 "   OR surname LIKE '%" + search_key + "%' "
                                 "   OR email LIKE '%" + search_key + "%' "
                                 "   OR phone LIKE '%" + search_key + "%' "
                                 "ORDER BY (CASE WHEN name LIKE '%" + search_key + "%' THEN 1 ELSE 0 END) + "
                                 "         (CASE WHEN surname LIKE '%" + search_key + "%' THEN 1 ELSE 0 END) + "
                                 "         (CASE WHEN email LIKE '%" + search_key + "%' THEN 1 ELSE 0 END) + "
                                 "         (CASE WHEN phone LIKE '%" + search_key + "%' THEN 1 ELSE 0 END) DESC"
                                 )
        self.cursor.execute(postgres_select_query)
        contacts_records = self.cursor.fetchall()
        if len(contacts_records) == 0:
            print('No contact found!!')
            return
        for row in contacts_records:
            self.print_contact(row)

    def print_all_contacts(self):
        postgres_select_query = 'SELECT * FROM contacts'
        self.cursor.execute(postgres_select_query)
        contacts_records = self.cursor.fetchall()
        for row in contacts_records:
            self.print_contact(row)

    def quit(self):
        self.disconnect_from_db()
        print('Exiting program')

#     def get_max_id(self):
#         # return max(max(part.values()) for part in self.contacts)
#         # return max(c['id'].values() for c in self.contacts)
#         max_id = 0
#         for c in self.contacts:
#             if c['id'] > max_id:
#                 max_id = c['id']
#         return max_id


class BothStore(Store):

    def __init__(self, _file_store, _db_store):
        self.file_store = _file_store
        self.db_store = _db_store

    def save_contact(self, _first_name, _surname, _email, _phone):
        self.file_store.save_contact(_first_name, _surname, _email, _phone)
        self.db_store.save_contact(_first_name, _surname, _email, _phone)

    def delete_contact(self, _idx):
        self.file_store.delete_contact(_idx)

    def update_contact(self, _idx):
        pass

    def find_contact(self, search_key):
        self.db_store.find_contact(search_key)

    def print_all_contacts(self):
        self.db_store.print_all_contacts()

    def quit(self):
        self.file_store.quit()
        self.db_store.quit()


class UserInput:

    def __init__(self):
        self.my_store = None

    def start(self, _my_store):
        self.my_store = _my_store
        while True:
            choice = input('type "a" to add a contact...\n'
                           'type "d" to delete a contact...\n'
                           'type "u" to update a contact...\n'
                           'type "f" to find a contact...\n'
                           'type "p" to print all contacts...\n'
                           'type "q" to quit...\n\n')

            if choice == 'a':
                self.add_contact()
            elif choice == 'd':
                self.delete_contact()
            elif choice == 'u':
                self.update_contact()
            elif choice == 'f':
                self.find_contact()
            elif choice == 'p':
                self.print_all_contacts()
            elif choice == 'q':
                self.quit_program()
                break
            else:
                print('invalid option!\n')

    def add_contact(self):
        first_name = input('type name of the contact: ')
        surname = input('type surname of the contact: ')
        email = input('type email address of the contact: ')
        phone = input('type phone number of the contact: ')

        self.my_store.save_contact(first_name, surname, email, phone)

    def print_all_contacts(self):
        self.my_store.print_all_contacts()

    def delete_contact(self):
        idx = int(input('type id of the contact to delete'))
        self.my_store.delete_contact(idx)

    def find_contact(self):
        search_key = input('type search keyword: ')
        self.my_store.find_contact(search_key)

    def update_contact(self):
        pass

    def quit_program(self):
        self.my_store.quit()


def main():
    parser = argparse.ArgumentParser(description='This is a phonebook application')
    parser.add_argument('--s',
                        choices=['file', 'database', 'both'],
                        required=True, type=str, help='This is the store type')
    args = parser.parse_args()
    store_type = args.s

    file_store = FileStore()
    db_store = DBStore()
    both_store = BothStore(file_store, db_store)
    store_dict = {'file': file_store, 'database': db_store, 'both': both_store}
    my_store = store_dict[store_type]

    user_input = UserInput()
    user_input.start(my_store)


main()
