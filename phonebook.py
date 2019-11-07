import argparse

from stores.both_store import BothStore
from stores.db_store import DBStore
from stores.file_store import FileStore
from stores.store_factory import store_factory_instance


def boot_strap():
    store_factory_instance.register_store('both', BothStore)
    store_factory_instance.register_store('file', FileStore)
    store_factory_instance.register_store('db', DBStore)


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
    boot_strap()
    parser = argparse.ArgumentParser(description='This is a phonebook application')
    parser.add_argument('--s',
                        choices=list(store_factory_instance.class_dict.keys()),
                        required=True, type=str, help='This is the store type')
    args = parser.parse_args()
    store_type = args.s

    my_store = store_factory_instance.create_store(store_type)

    user_input = UserInput()
    user_input.start(my_store)


main()
