import psycopg2

from stores.store import Store
from stores.store_factory import store_factory_instance


class DBStore(Store):

    # # singleton
    # def __new__(cls):
    #     if not hasattr(cls, 'instance'):
    #         cls.instance = super().__new__(cls)
    #     return cls.instance

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
                                 "WHERE name LIKE '" + search_key + "%' "
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

