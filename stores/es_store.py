from elasticsearch import Elasticsearch
from elasticsearch import ConnectionError
from elasticsearch import NotFoundError

from stores.store import Store


# if you get index read-only error you may be low in disk space or your index is read only:
# curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_cluster/settings -d '{ "transient": { "cluster.routing.allocation.disk.threshold_enabled": false } }'
# curl -XPUT -H "Content-Type: application/json" http://localhost:9200/_all/_settings -d '{"index.blocks.read_only_allow_delete": null}'

class ESStore(Store):

    def __init__(self):
        self.es = None
        self.index_name = 'phonebook'
        self.doc_type_name = 'contacts'
        self._connect_to_elastic_search()
        self._create_es_index_with_mapping(self.index_name)

    # Class specific methods
    def _connect_to_elastic_search(self):
        try:
            self.es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
            print("Connected", self.es.info())
        except ConnectionError:
            print('Could not connect to ElasticSearch!!')

    def _create_es_index_with_mapping(self, index_name):
        # check if index exists
        index_exists = self.es.indices.exists(index=index_name)
        if index_exists:
            return
        # when we insert a document it creates the index and set the mapping accordingly
        doc_data = {
            'name': 'serhat',
            'surname': 'demir',
            'email': 'serhatdemir@gmail.com',
            'phone': '121243544657'
        }
        self.es.index(index=self.index_name, doc_type=self.doc_type_name, id=1, body=doc_data)

    def _print_contact(self, doc):
        pass

    def _print_contacts_ordered(self, docs):
        contacts_view = []
        if not docs:
            return None
        for hit in docs:
            score = hit['_score']
            con = {hit['_id']: {f'match score: {score}': hit['_source']}}
            contacts_view.append(con)
        return contacts_view

    # Inherited methods
    def save_contact(self, name=None, surname=None, email=None, phone=None):
        doc_data = {
            'name': name,
            'surname': surname,
            'email': email,
            'phone': phone
        }
        res = self.es.index(index=self.index_name, doc_type=self.doc_type_name, body=doc_data)
        return {res['_id']: self.find_contact_by_id(res['_id'])}

    def delete_contact(self, idx):
        document_to_delete = self.find_contact_by_id(idx)
        if document_to_delete:
            res = self.es.delete(index=self.index_name, doc_type=self.doc_type_name, id=idx)
            return {idx: document_to_delete}

    def update_contact(self, contact):
        if self.find_contact_by_id(contact['id']):
            doc_data = {
                'name': contact['name'],
                'surname': contact['surname'],
                'email': contact['email'],
                'phone': contact['phone']
            }
            res = self.es.index(index=self.index_name, doc_type=self.doc_type_name, id=contact['id'], body=doc_data)
        return {contact['id']: self.find_contact_by_id(contact['id'])}

    def find_contact_by_id(self, idx):
        try:
            res = self.es.get(index=self.index_name, doc_type=self.doc_type_name, id=idx)
            return res['_source']
        except NotFoundError:
            return None

    # sort according to number of matches
    def find_contact(self, search_key):
        if search_key is None:
            return None
        # putting wildcard in the beginning is not suggested.
        res = self.es.search(index=self.index_name, body={
            'query': {
                'multi_match': {
                    "query": search_key,
                    "type":       "phrase_prefix",
                    # "fields": ["name", "surname", "email", "phone"]
                }
            },
            # "query": {
            #     "bool": {
            #         "should": [
            #             {"prefix": {"name": search_key}},
            #             {"prefix": {"surname": search_key}},
            #             {"prefix": {"email": search_key}},
            #             {"prefix": {"phone": search_key}}
            #         ]
            #     }
            # },
            "sort": [
                {
                    "_score": {
                        "order": "desc"
                    }
                }
            ]

        })
        return self._print_contacts_ordered(res['hits']['hits'])

    def print_all_contacts(self):
        res = self.es.search(index=self.index_name, body={"query": {"match_all": {}}})
        print(f"There are {res['hits']['total']['value']} contacts in the phonebook")
        if not res['hits']['hits']:
            return None
        # add ID for nicer display
        contacts_view = {}
        for hit in res['hits']['hits']:
            contacts_view[hit["_id"]] = hit["_source"]
        return contacts_view

    def quit(self):
        pass
