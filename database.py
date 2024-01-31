import mysql.connector


class Server:
    def __init__(self, host, user, password, database=None):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.server_connection = None
        self.server_cursor = None
        self.database_connection = None
        self.database_cursor = None

    def connect_server(self):
        self.server_connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password
        )
        self.server_cursor = self.server_connection.cursor()

    def create_database(self, database_name):
        self.server_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        self.database = database_name

    def connect_database(self):
        self.database_connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.database_cursor = self.database_connection.cursor()

    def create_users_table(self):
        query = f"""
            CREATE TABLE IF NOT EXISTS {self.database}.users (
                username VARCHAR(255) PRIMARY KEY NOT NULL,
                password VARCHAR(255) NOT NULL,
                firstName VARCHAR(255) NOT NULL,
                lastName VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL
            );
            """
        self.database_cursor.execute(query)
        self.commit()

    def initialize_database(self):
        # drop_all_tables()
        self.database_cursor.execute("DROP TABLE IF EXISTS users")
        self.create_users_table()

        example_users = [
            ("user1", "password1", "John", "Doe", "john@example.com"),
            ("user2", "password2", "Jane", "Doe", "jane@example.com"),
            ("user3", "password3", "Michael", "Smith", "michael@example.com"),
            ("user4", "password4", "Emily", "Johnson", "emily@example.com"),
            ("user5", "password5", "David", "Williams", "david@example.com"),
        ]

        query = "INSERT INTO users (username, password, firstName, lastName, email) VALUES (%s, %s, %s, %s, %s)"
        for user in example_users:
            self.database_cursor.execute(query, user)
        self.commit()

    def commit(self):
        self.database_connection.commit()
