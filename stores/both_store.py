from stores.store import Store
from stores.store_factory import store_factory_instance


class BothStore(Store):

    def __init__(self):
        from stores.store_factory import store_factory_instance
        self.file_store = store_factory_instance.create_store('file')
        self.db_store = store_factory_instance.create_store('db')

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


