import sqlite3
from typing import List


class DatabaseProvider:
    def __init__(self):
        self.db_name = 'example.db'
        self.__connection = sqlite3.connect(self.db_name)
        self.__cursor = self.__connection.cursor()
        self.__tables = ['countries']

    def create_countries_table(self):
        self.__cursor.execute('''CREATE TABLE countries (id integer primary key, name text)''')
        self.__connection.commit()

    def fill_countries(self, countries: List):
        for country in countries:
            self.__cursor.execute("INSERT INTO countries (id, name) VALUES (NULL, ?);", (country,))
        self.__connection.commit()

    def select_table(self, table_name: str):
        for row in self.__cursor.execute(f'SELECT * FROM {table_name};'):
            print(row)

    def drop_table(self, table_name: str):
        self.__cursor.execute(f'''DROP TABLE {table_name};''')
        self.__connection.commit()
