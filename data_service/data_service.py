import sqlite3


class DataService:

    def __init__(self) -> None:
        pass

    def get_item(self):
        pass

    def list(self, entity_name: str, where: str = None) -> list:
        pass

    def create_item(self, entity_name: str, item: dict) -> None:
        pass

    def update(self):
        pass

    def delete(self):
        pass