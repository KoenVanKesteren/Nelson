import sqlite3
from data_service.data_service import DataService


class SqliteService(DataService):

    def __init__(self, config: dict) -> None:
        super().__init__()

        # self.db_path = config['db_path']
        self.db_path = "D:\\ict\\projecten\\opdrachten\\Nelson\\test.db"

    def connect(self):
        self.connection = sqlite3.connect(self.db_path)

    def close_connection(self):
        self.connection.close()

    def create_entity(self, entity_name, attributes):
        cur = self.connection.cursor()

        query_attributes = ",".join(["{0} {1}".format(att['name'], self.map_type(att['type'])) for att in attributes])

        query = '''
            CREATE TABLE IF NOT EXISTS {0} 
            ({1})
        '''.format(entity_name, query_attributes)

        cur.execute(query)

        self.connection.commit()

    def map_type(self, type):
        # TODO: implement mapping for service type
        mapped_type = type
        return mapped_type

    def get(self):
        pass

    def list(self, entity_name: str, where="1", limit=1000):

        self.connection.row_factory = sqlite3.Row
        cur = self.connection.cursor()

        query = '''
            SELECT * FROM {0} 
            WHERE {1}
            limit {2}
        '''.format(entity_name, where, limit)
        cur.execute(query)
        result = [dict(row) for row in cur.fetchall()]

        return result

    def create_item(self, entity_name, item):
        # split dict into two separate tuples for column names and values
        column_names, query_values = zip(*[(key, value) for key, value in item.items()])

        cur = self.connection.cursor()

        query = '''
            INSERT INTO {0} {1} VALUES {2}
        '''.format(entity_name, column_names, query_values)

        cur.execute(query)
        self.connection.commit()

    def update(self):
        pass

    def delete(self):
        pass


