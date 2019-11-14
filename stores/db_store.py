import psycopg2

from stores.store import Store


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
    def save_contact(self, name=None, surname=None, email=None, phone=None):
        postgres_insert_query = """ INSERT INTO contacts (NAME, SURNAME, EMAIL, PHONE) VALUES (%s,%s,%s,%s) RETURNING ID"""
        record_to_insert = (name, surname, email, phone)
        self.cursor.execute(postgres_insert_query, record_to_insert)
        self.connection.commit()
        inserted_id = self.cursor.fetchone()[0]
        return self.find_contact_by_id(inserted_id)

    def delete_contact(self, idx):
        idx = int(idx)
        record_to_delete = self.find_contact_by_id(idx)
        postgres_delete_query = """ DELETE FROM contacts WHERE id = %s"""
        id_to_delete = [idx]
        self.cursor.execute(postgres_delete_query, id_to_delete)
        self.connection.commit()
        return record_to_delete

    def update_contact(self, contact):
        print(contact)
        postgres_update_query = """ UPDATE contacts SET NAME = %s, SURNAME = %s, EMAIL = %s, PHONE = %s WHERE ID = %s"""
        record_to_update = (contact['name'], contact['surname'], contact['email'], contact['phone'], int(contact['id']))
        self.cursor.execute(postgres_update_query, record_to_update)
        self.connection.commit()
        return self.find_contact_by_id(contact['id'])

    def find_contact_by_id(self, idx):
        idx = int(idx)
        postgres_select_query = """ SELECT * FROM contacts WHERE id = %s"""
        id_to_find = [idx]
        self.cursor.execute(postgres_select_query, id_to_find)
        contact_record = self.cursor.fetchone()
        if contact_record:
            self.print_contact(contact_record)
            contact_view = {'id': contact_record[4], 'name': contact_record[0],
                            'surname': contact_record[1], 'phone': contact_record[3], 'email': contact_record[2]}
            return contact_view
        return None

    def find_contact(self, search_key):
        postgres_select_query = ("SELECT * "
                                 "FROM contacts "
                                 "WHERE name LIKE %(key)s "
                                 "   OR surname LIKE %(key)s "
                                 "   OR email LIKE %(key)s "
                                 "   OR phone LIKE %(key)s "
                                 "ORDER BY (CASE WHEN name LIKE %(key)s THEN 1 ELSE 0 END) + "
                                 "         (CASE WHEN surname LIKE %(key)s THEN 1 ELSE 0 END) + "
                                 "         (CASE WHEN email LIKE %(key)s THEN 1 ELSE 0 END) + "
                                 "         (CASE WHEN phone LIKE %(key)s THEN 1 ELSE 0 END) DESC"
                                 )
        self.cursor.execute(postgres_select_query, {'key': search_key + '%'})
        contacts_records = self.cursor.fetchall()
        if len(contacts_records) == 0:
            print('No contact found!!')
            return None
        contacts_view = []
        for rec in contacts_records:
            self.print_contact(rec)
            contacts_view.append({'id': rec[4], 'name': rec[0],
                                  'surname': rec[1], 'phone': rec[3], 'email': rec[2]})
        return contacts_view

    def print_all_contacts(self):
        postgres_select_query = 'SELECT * FROM contacts'
        self.cursor.execute(postgres_select_query)
        contacts_records = self.cursor.fetchall()
        for row in contacts_records:
            self.print_contact(row)

    def quit(self):
        self.disconnect_from_db()
        print('Exiting program')

