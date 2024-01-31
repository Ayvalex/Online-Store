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

    def create_user_table(self):
        query = f"""
            CREATE TABLE IF NOT EXISTS {self.database}.user (
                username VARCHAR(255) PRIMARY KEY NOT NULL,
                password VARCHAR(255) NOT NULL,
                firstName VARCHAR(255) NOT NULL,
                lastName VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL
            );
            """
        self.database_cursor.execute(query)
        self.commit()

    def create_item_table(self):
        query = f"""
            CREATE TABLE IF NOT EXISTS {self.database}.item (
                itemID INT AUTO_INCREMENT PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                description TEXT NOT NULL,
                price DECIMAL(10, 2) UNSIGNED NOT NULL,
                username VARCHAR(255) NOT NULL,
                postDate DATE NOT NULL,
                FOREIGN KEY (username) REFERENCES {self.database}.user(username)
            );
            """
        self.database_cursor.execute(query)
        self.commit()

    def create_item_category_table(self):
        query = f"""
               CREATE TABLE IF NOT EXISTS {self.database}.item_category (
                   itemID INT NOT NULL,
                   category VARCHAR(50) NOT NULL,
                   FOREIGN KEY (itemID) REFERENCES {self.database}.item(itemID)
               );
               """
        self.database_cursor.execute(query)
        self.commit()

    def create_review_table(self):
        query = f"""
               CREATE TABLE IF NOT EXISTS {self.database}.review (
                   reviewID INT AUTO_INCREMENT PRIMARY KEY,
                   remark TEXT,
                   score ENUM('Excellent', 'Good', 'Fair', 'Poor') NOT NULL,
                   reviewDate DATE NOT NULL,
                   username VARCHAR(255) NOT NULL,
                   itemID INT NOT NULL,
                   FOREIGN KEY (username) REFERENCES {self.database}.user(username),
                   FOREIGN KEY (itemID) REFERENCES {self.database}.item(itemID)
               );
               """
        self.database_cursor.execute(query)
        self.commit()

    def create_favorite_table(self):
        query = f"""
            CREATE TABLE IF NOT EXISTS {self.database}.favorite (
                username VARCHAR(255) NOT NULL,
                favorite_seller VARCHAR(255) NOT NULL,
                FOREIGN KEY (username) REFERENCES {self.database}.user(username) ON DELETE CASCADE,
                FOREIGN KEY (favorite_seller) REFERENCES {self.database}.user(username) ON DELETE CASCADE
            );
            """
        self.database_cursor.execute(query)
        self.commit()

    def initialize_database(self):
        # Drop all tables
        self.database_cursor.execute("DROP TABLE IF EXISTS favorite")
        self.database_cursor.execute("DROP TABLE IF EXISTS review")
        self.database_cursor.execute("DROP TABLE IF EXISTS item_category")
        self.database_cursor.execute("DROP TABLE IF EXISTS item")
        self.database_cursor.execute("DROP TABLE IF EXISTS user")

        # Create all tables
        self.create_user_table()
        self.create_item_table()
        self.create_item_category_table()
        self.create_review_table()
        self.create_favorite_table()

        # Populate the user table
        example_users = [
            ("user1", "password1", "John", "Doe", "john@example.com"),
            ("user2", "password2", "Jane", "Doe", "jane@example.com"),
            ("user3", "password3", "Michael", "Smith", "michael@example.com"),
            ("user4", "password4", "Emily", "Johnson", "emily@example.com"),
            ("user5", "password5", "David", "Williams", "david@example.com"),
            ("user6", "password6", "Jennifer", "Smith", "jennifer@example.com"),
            ("user7", "password7", "Samuel", "Lee", "samuel@example.com"),
            ("user8", "password8", "Sophie", "Nguyen", "sophie@example.com"),
            ("user9", "password9", "William", "Taylor", "william@example.com"),
            ("user10", "password10", "Olivia", "Brown", "olivia@example.com"),
            ("user11", "password11", "Ethan", "Garcia", "ethan@example.com"),
            ("user12", "password12", "Emma", "Gonzalez", "emma@example.com"),
            ("user13", "password13", "Avery", "Perez", "avery@example.com"),
            ("user14", "password14", "Benjamin", "Robinson", "benjamin@example.com"),
            ("user15", "password15", "Chloe", "Clark", "chloe@example.com"),
        ]

        user_query = "INSERT INTO user (username, password, firstName, lastName, email) VALUES (%s, %s, %s, %s, %s)"
        for user in example_users:
            self.database_cursor.execute(user_query, user)

        # Populate the item table
        example_items = [
            ("Apple iPhone 14 Pro", "Brand new Apple iPhone 14 Pro, 256GB, Gold color, factory unlocked.", 1200.00,
             "user3", "2022-09-15"),
            ("Vintage Guitar", "Vintage electric guitar from the 80s, great sound and condition.", 900.00, "user7",
             "2021-06-12"),
            ("Mountain Bike", "Mountain bike in great condition, 27-speed, hydraulic disc brakes.", 400.00, "user4",
             "2020-03-21"),
            ("Nintendo Switch", "Nintendo Switch gaming console, great condition, includes two games.", 275.00, "user2",
             "2022-02-25"),
            ("Gaming Chair", "Comfortable gaming chair with adjustable features and lumbar support.", 150.00, "user5",
             "2019-07-10"),
            ("Instant Pot", "Instant Pot 6-quart, 7-in-1 multi-use programmable pressure cooker.", 60.00, "user6",
             "2022-11-15"),
            ("Yoga Mat", "Eco-friendly yoga mat, 4mm thickness, excellent condition.", 20.00, "user8", "2018-05-01"),
            (
            "Canon EOS 5D Mark IV", "Canon EOS 5D Mark IV DSLR camera with 24-70mm lens, excellent condition.", 2500.00,
            "user9", "2022-01-30"),
            (
            "Electric Scooter", "Electric scooter with a range of 25 miles and a top speed of 18 mph.", 350.00, "user1",
            "2021-08-15"),
            ("Designer Handbag", "Designer handbag from a luxury brand, gently used, includes dust bag.", 850.00,
             "user10", "2019-12-01"),
            ("Harry Potter Box Set", "Complete Harry Potter book series box set in hardcover, excellent condition.",
             120.00, "user3", "2020-05-01"),
            ("Smart TV", "55-inch 4K Ultra HD Smart LED TV with HDR, great condition.", 450.00, "user12", "2021-03-28"),
            ("Dining Table Set", "Wooden dining table set with 6 chairs, gently used, some minor scratches.", 600.00,
             "user13", "2018-12-05"),
            ("LEGO Creator Set", "LEGO Creator Expert set, 2500 pieces, new in sealed box.", 175.00, "user1",
             "2021-08-15"),
            ("Basketball Hoop", "Adjustable outdoor basketball hoop system, in-ground installation required.", 250.00,
             "user15", "2021-09-18"),

        ]
        item_query = "INSERT INTO item (title, description, price, username, postDate) VALUES (%s, %s, %s, %s, %s)"
        for item in example_items:
            self.database_cursor.execute(item_query, item)

        # Populate the item_category table
        example_item_categories = [
            (1, "Electronics"),
            (2, "Music"),
            (3, "Sports"),
            (4, "Electronics"),
            (5, "Furniture"),
            (6, "Kitchen"),
            (7, "Sports"),
            (8, "Electronics"),
            (9, "Sports"),
            (10, "Fashion"),
            (11, "Books"),
            (12, "Electronics"),
            (13, "Furniture"),
            (14, "Toys"),
            (15, "Sports"),
        ]

        item_category_query = "INSERT INTO item_category (itemID, category) VALUES (%s, %s)"
        for item_category in example_item_categories:
            self.database_cursor.execute(item_category_query, item_category)

        # Populate the review table
        example_reviews = [
            ("Great product!", "Poor", "2023-04-02", "user13", 1),
            ("I love this guitar!", "Excellent", "2021-07-02", "user1", 2),
            ("Smooth ride and great brakes.", "Poor", "2020-04-15", "user3", 9),
            ("The console is perfect for gaming.", "Excellent", "2022-03-10", "user4", 4),
            ("So uncomfortable!", "Poor", "2019-08-01", "user6", 5),
            ("Makes cooking much easier.", "Good", "2022-12-01", "user7", 6),
            ("Nice material and perfect thickness.", "Fair", "2018-06-15", "user5", 7),
            ("Impressive image quality.", "Excellent", "2022-02-10", "user2", 8),
            ("Not very fun to ride.", "Excellent", "2021-09-05", "user10", 9),
            ("Stylish and great quality.", "Excellent", "2020-01-15", "user11", 10),
            ("This iPhone is amazing!", "Excellent", "2022-09-20", "user12", 1),
            ("Stunning camera, great purchase!", "Excellent", "2022-02-05", "user13", 1),
            ("Love my new electric scooter!", "Excellent", "2021-08-25", "user14", 9),
            ("Incredible sound on the vintage guitar!", "Excellent", "2021-07-10", "user15", 2),
            ("Best gaming console ever!", "Fair", "2022-01-20", "user1", 4),
            ("High-quality Instant Pot, very happy with it!", "Poor", "2021-12-05", "user3", 13),
            ("The yoga mat is eco-friendly and comfortable!", "Excellent", "2018-05-10", "user4", 7),
            ("Love it!", "Excellent", "2018-05-10", "user9", 4),
        ]
        review_query = "INSERT INTO review (remark, score, reviewDate, username, itemID) VALUES (%s, %s, %s, %s, %s)"
        for review in example_reviews:
            self.database_cursor.execute(review_query, review)

        example_favorites = [
            ("user1", "user5"),
            ("user2", "user4"),
            ("user3", "user1"),
            ("user4", "user3"),
            ("user5", "user2"),
            ("user3", "user2"),
            ("user1", "user4"),
            ("user2", "user6"),
            ("user3", "user7"),
            ("user4", "user8"),
            ("user5", "user9"),
            ("user6", "user10"),
            ("user7", "user11"),
            ("user8", "user12"),
            ("user9", "user13"),
            ("user10", "user14"),
            ("user11", "user15"),
            ("user12", "user1"),
            ("user13", "user2"),
            ("user14", "user3"),
            ("user15", "user4"),
        ]

        favorite_query = "INSERT INTO favorite (username, favorite_seller) VALUES (%s, %s)"
        for favorite in example_favorites:
            self.database_cursor.execute(favorite_query, favorite)

        self.commit()

    def commit(self):
        self.database_connection.commit()
