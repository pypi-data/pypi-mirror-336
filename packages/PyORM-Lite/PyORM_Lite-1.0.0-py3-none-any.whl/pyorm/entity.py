from .db_manager import DBManager
from .utils import pluralize


class Entity:
    db = None  # Static database connection

    @classmethod
    def connect(cls, path=None):
        cls.db = DBManager.connect(path)
        if cls.db is None:
            raise ConnectionError("Failed to establish a database connection.")

    @classmethod
    def create_table(cls):
        table_name = pluralize(cls.__name__)
        fields = getattr(cls, "_fields", {})
        columns = []
        for field, metadata in fields.items():
            column_definition = f"{field} {metadata['type']}"
            if "constraints" in metadata:
                column_definition += f" {metadata['constraints']}"
            if "default" in metadata:
                column_definition += f" DEFAULT {metadata['default']}"
            columns.append(column_definition)
        if not columns:
            print(f"No fields defined for table '{table_name}'. Cannot create table.")
            return False
        sql_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY AUTOINCREMENT, {', '.join(columns)});"
        try:
            cursor = cls.db.cursor()
            cursor.execute(sql_query)
            cls.db.commit()
            print(f"Table '{table_name}' created successfully.")
            return True
        except Exception as e:
            print(f"Error creating table '{table_name}': {e}")
            return False

    @classmethod
    def is_table_exist(cls):
        table_name = pluralize(cls.__name__)
        sql_query = f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';"
        try:
            cursor = cls.db.cursor()
            cursor.execute(sql_query)
            result = cursor.fetchone()
            return bool(result)
        except Exception as e:
            print(f"Error checking if table '{table_name}' exists: {e}")
            return False

    @classmethod
    def find_by_id(cls, id):
        table_name = pluralize(cls.__name__)
        sql_query = f"SELECT * FROM {table_name} WHERE id = ?;"
        try:
            cursor = cls.db.cursor()
            cursor.execute(sql_query, (id,))
            row = cursor.fetchone()
            if row:
                return cls(**dict(row))
            return None
        except Exception as e:
            print(f"Error finding record by ID: {e}")
            return None

    @classmethod
    def where(cls, condition, params=None):
        table_name = pluralize(cls.__name__)
        query = f"SELECT * FROM {table_name} WHERE {condition};"
        try:
            cursor = cls.db.cursor()
            cursor.execute(query, params or [])
            rows = cursor.fetchall()
            return [cls(**dict(row)) for row in rows]
        except Exception as e:
            print(f"Error retrieving records with condition '{condition}': {e}")
            return []

    @classmethod
    def all(cls):
        table_name = pluralize(cls.__name__)
        sql_query = f"SELECT * FROM {table_name};"
        try:
            cursor = cls.db.cursor()
            cursor.execute(sql_query)
            rows = cursor.fetchall()
            return [cls(**dict(row)) for row in rows]
        except Exception as e:
            print(f"Error retrieving all records: {e}")
            return []

    @classmethod
    def count(cls, condition=None, params=None):
        table_name = pluralize(cls.__name__)
        query = f"SELECT COUNT(*) FROM {table_name}"
        if condition:
            query += f" WHERE {condition};"
        try:
            cursor = cls.db.cursor()
            cursor.execute(query, params or [])
            result = cursor.fetchone()
            return result[0] if result else 0
        except Exception as e:
            print(f"Error counting records in table '{table_name}': {e}")
            return 0

    @classmethod
    def drop(cls):
        table_name = pluralize(cls.__name__)
        sql_query = f"DROP TABLE IF EXISTS {table_name};"
        try:
            cursor = cls.db.cursor()
            cursor.execute(sql_query)
            cls.db.commit()
            print(f"Table '{table_name}' dropped successfully.")
            return True
        except Exception as e:
            print(f"Error dropping table '{table_name}': {e}")
            return False

    @classmethod
    def delete_all(cls):
        table_name = pluralize(cls.__name__)
        sql_query = f"DELETE FROM {table_name};"
        try:
            cursor = cls.db.cursor()
            cursor.execute(sql_query)
            cls.db.commit()
            print(f"All records deleted from table '{table_name}'.")
            return True
        except Exception as e:
            print(f"Error deleting all records from table '{table_name}': {e}")
            return False

    def save(self):
        if self.id is None:
            return self._insert()
        else:
            return self._update()

    def _insert(self):
        table_name = pluralize(self.__class__.__name__)
        fields = getattr(self.__class__, "_fields", {})
        columns = []
        values = []
        for field in fields:
            value = getattr(self, field, None)
            if value is not None:
                columns.append(field)
                values.append(value)
        if not columns:
            print("No valid fields to insert.")
            return False
        placeholders = ", ".join(["?"] * len(columns))
        sql_query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders});"
        try:
            cursor = self.db.cursor()
            cursor.execute(sql_query, values)
            self.db.commit()
            self.id = cursor.lastrowid
            print(f"Inserted record into table '{table_name}' with ID {self.id}.")
            return self
        except Exception as e:
            print(f"Error inserting record: {e}")
            return False

    def _update(self):
        table_name = pluralize(self.__class__.__name__)
        updates = [f"{field} = ?" for field in getattr(self.__class__, "_fields", {}) if getattr(self, field) is not None]
        values = [getattr(self, field) for field in getattr(self.__class__, "_fields", {}) if getattr(self, field) is not None] + [self.id]
        sql_query = f"UPDATE {table_name} SET {', '.join(updates)} WHERE id = ?;"
        try:
            cursor = self.db.cursor()
            cursor.execute(sql_query, values)
            self.db.commit()
            print(f"Updated record in table '{table_name}' with ID {self.id}.")
            return True
        except Exception as e:
            print(f"Error updating record: {e}")
            return False

    def delete(self):
        table_name = pluralize(self.__class__.__name__)
        sql_query = f"DELETE FROM {table_name} WHERE id = ?;"
        try:
            cursor = self.db.cursor()
            cursor.execute(sql_query, (self.id,))
            self.db.commit()
            print(f"Deleted record from table '{table_name}' with ID {self.id}.")
            return True
        except Exception as e:
            print(f"Error deleting record: {e}")
            return False