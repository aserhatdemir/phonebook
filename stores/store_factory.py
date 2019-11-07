class StoreFactory:

    def __init__(self):
        self.class_dict = {}
        self.instance_dict = {}

    def register_store(self, store_type: str, store_class: type):
        self.class_dict[store_type] = store_class

    def create_store(self, store_type):
        if store_type not in self.instance_dict:
            self.instance_dict[store_type] = self.class_dict[store_type]()

        return self.instance_dict[store_type]


store_factory_instance = StoreFactory()
