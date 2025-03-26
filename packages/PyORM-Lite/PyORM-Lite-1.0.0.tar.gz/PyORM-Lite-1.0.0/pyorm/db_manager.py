import os
import sqlite3


class DBManager:
    db = None  # Static database connection

    @staticmethod
    def connect(db_name="database.db"):
        """
        Connect to the SQLite database.
        :param db_name: Name of the database file.
        """
        if DBManager.db is None:
            try:
                # Ensure the directory exists
                os.makedirs(os.path.dirname(db_name), exist_ok=True)

                # Attempt to connect to the database
                DBManager.db = sqlite3.connect(db_name)
                DBManager.db.row_factory = sqlite3.Row  # Allows accessing rows as dictionaries
                print(f"Connected to database: {db_name}")
            except Exception as e:
                print(f"Error connecting to the database: {e}")
                DBManager.db = None  # Reset db to None in case of failure
        else:
            print("Already connected to the database.")
        return DBManager.db

    @staticmethod
    def disconnect():
        """
        Disconnect from the database.
        """
        if DBManager.db is not None:
            try:
                DBManager.db.close()
                DBManager.db = None
                print("Disconnected from the database.")
            except Exception as e:
                print(f"Error disconnecting from the database: {e}")
        else:
            print("No active database connection to disconnect.")

    @staticmethod
    def execute_raw_query(query, params=None):
        """
        Execute a raw SQL query.
        :param query: The SQL query to execute.
        :param params: Optional parameters for the query.
        :return: Query results if applicable, or None.
        """
        if DBManager.db is None:
            raise ConnectionError("Database connection is not established.")
        try:
            cursor = DBManager.db.cursor()
            cursor.execute(query, params or [])
            DBManager.db.commit()
            rows = cursor.fetchall()
            return [dict(row) for row in rows] if rows else []
        except Exception as e:
            print(f"Error executing query: {e}")
            return None

    @staticmethod
    def execute_sql_file(file_path):
        """
        Execute SQL commands from a file.
        :param file_path: Path to the SQL file.
        :return: True if the file was executed successfully, False otherwise.
        """
        if DBManager.db is None:
            raise ConnectionError("Database connection is not established.")
        if not os.path.exists(file_path):
            print(f"SQL file not found: {file_path}")
            return False
        try:
            with open(file_path, "r") as file:
                sql_script = file.read()
            cursor = DBManager.db.cursor()
            cursor.executescript(sql_script)  # Execute the entire script
            DBManager.db.commit()
            print(f"Executed SQL file: {file_path}")
            return True
        except Exception as e:
            print(f"Error executing SQL file: {e}")
            return False