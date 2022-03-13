import sqlite3

class DB:

    METHOD_CREATE = 'create'
    METHOD_DELETE = 'delete'
    METHOD_INSERT = 'insert'
    METHOD_SELECT = 'select'
    METHOD_UPDATE = 'update'

    METHODS = [
        METHOD_CREATE,
        METHOD_DELETE,
        METHOD_INSERT,
        METHOD_SELECT,
        METHOD_UPDATE,
    ]

    def __init__(self, name='db.sqlite'):
        self.name = name
        self.db = sqlite3.connect(self.name)
        self.transaction_active = False

    def __del__(self):
        self.db.close()

    def __getattr__(self, name):
        def shortcut(*args, **kwargs):
            method, table = name.split('_', 1)
            if table not in self.tables() and method != self.METHOD_CREATE:
                raise NameError(f"Unable to find table '{table}' in '{self.name}'")
            if method not in self.METHODS:
                raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")
            return getattr(self, method)(table, *args, **kwargs)
        return shortcut

    def begin_transaction(self):
        self.transaction_active = True

    def run(self, query, parameters=()):
        cursor = self.db.cursor()
        cursor.execute(query, parameters)
        result = cursor.fetchall()
        if not self.transaction_active:
            self.commit()
        return result

    def commit(self):
        self.transaction_active = False
        self.db.commit()

    def rollback(self):
        self.transaction_active = False
        self.db.rollback()

    def tables(self):
        return [table[0] for table in self.run('SELECT name FROM sqlite_master')]

    def create(self, table, **columns):
        columns = ', '.join([f'{k} {v}' for k, v in columns.items()])
        return self.run(f'CREATE TABLE {table} ({columns})')

    def delete(self, table, where={}):
        where_sql = (' WHERE ' + ' AND '.join([f'{column} = ?' for column in where.keys()])) if where else ''
        return self.run(f'DELETE FROM {table}{where_sql}', tuple(where.values()))

    def insert(self, table, **columns):
        columns_sql = ', '.join(columns.keys())
        placeholders_sql = ', '.join(['?'] * len(columns))
        return self.run(f'INSERT INTO {table} ({columns_sql}) VALUES ({placeholders_sql})', tuple(columns.values()))

    def select(self, table, where={}, *columns):
        columns = ', '.join(columns) if columns else '*'
        where_sql = (' WHERE ' + ' AND '.join([f'{column} = ?' for column in where.keys()])) if where else ''
        return self.run(f'SELECT {columns} FROM {table}{where_sql}', tuple(where.values()))

    def update(self, table, where={}, **columns):
        columns_sql = ', '.join([f'{column} = ?' for column in columns.keys()])
        where_sql = (' WHERE ' + ' AND '.join([f'{column} = ?' for column in where.keys()])) if where else ''
        return self.run(f'UPDATE {table} SET {columns_sql}{where_sql}', tuple(columns.values()) + tuple(where.values()))
