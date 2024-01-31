from tkinter import messagebox


class ItemManager:
    def __init__(self, server):
        self.server = server
        # self.user_manager = user_manager

    def _count_items_posted_today(self, username):
        query = "SELECT COUNT(*) FROM item WHERE username = %s AND postDate = CURRENT_DATE"
        self.server.database_cursor.execute(query, (username,))
        count = self.server.database_cursor.fetchone()[0]
        return count

    def _insert_item(self, item, user_manager):
        query = "INSERT INTO item (title, description, price, username, postDate) " \
                "VALUES (%s, %s, %s, %s, CURRENT_DATE)"
        self.server.database_cursor.execute(query, (item.title, item.description, item.price,user_manager.current_user.
                                                    username))
        self.server.database_connection.commit()
        return self.server.database_cursor.lastrowid

    def _insert_item_categories(self, item_id, categories):
        for category in categories:
            query = "SELECT COUNT(*) FROM item_category WHERE itemID = %s AND LOWER(category) = %s"
            self.server.database_cursor.execute(query, (item_id, category))
            count = self.server.database_cursor.fetchone()[0]
            if count == 0:
                query = "INSERT INTO item_category (itemID, category) VALUES (%s, %s)"
                self.server.database_cursor.execute(query, (item_id, category))
        self.server.database_connection.commit()

    @staticmethod
    def _get_unique_categories(category_string):
        category_list = category_string.split(',')
        categories = []
        for category in category_list:
            stripped_category = category.strip()
            if stripped_category not in categories:
                categories.append(stripped_category)
        return categories

    def post_item(self, item, user_manager):
        if user_manager.current_user:
            items_posted_today = self._count_items_posted_today(user_manager.current_user.username)
            if items_posted_today == 3:
                messagebox.showerror("Post Item Error", "You can only post 3 items per day.")
                return False

            # Insert item into the item table and get the itemID
            item_id = self._insert_item(item, user_manager)

            # Get unique categories and insert them into the item_category table
            categories = ItemManager._get_unique_categories(item.category)
            self._insert_item_categories(item_id, categories)

            return True
        else:
            return False

    def get_items_by_category(self, category):
        query = f"""
            SELECT i.itemID, i.title, i.description, i.price, i.username, i.postDate
            FROM item i
            JOIN item_category ic ON i.itemID = ic.itemID
            WHERE LOWER(ic.category) = %s
            """
        self.server.database_cursor.execute(query, (category.lower(),))
        items = self.server.database_cursor.fetchall()
        keys = ["item_id", "title", "description", "price", "username", "post_date"]
        return [dict(zip(keys, item)) for item in items]

    def most_expensive_items_by_category(self):
        query = f"""
            SELECT ic.category, i.title, i.price
            FROM {self.server.database}.item AS i
            INNER JOIN {self.server.database}.item_category AS ic ON i.itemID = ic.itemID
            WHERE (
                SELECT COUNT(*)
                FROM {self.server.database}.item AS i2
                INNER JOIN {self.server.database}.item_category AS ic2 ON i2.itemID = ic2.itemID
                WHERE ic2.category = ic.category AND i2.price > i.price
            ) = 0
            ORDER BY ic.category, i.price DESC;
            """
        self.server.database_cursor.execute(query)
        results = self.server.database_cursor.fetchall()
        keys = ["category", "title", "price"]
        return [dict(zip(keys, result)) for result in results]

    def get_users_that_posted_two_items_same_day(self, category_x, category_y):
        query = f"""
            SELECT u.username
            FROM {self.server.database}.item i1
            JOIN {self.server.database}.item_category ic1 ON i1.itemID = ic1.itemID
            JOIN {self.server.database}.item i2 ON i1.username = i2.username AND i1.postDate = i2.postDate AND i1.itemID != i2.itemID
            JOIN {self.server.database}.item_category ic2 ON i2.itemID = ic2.itemID
            JOIN {self.server.database}.user u ON i1.username = u.username
            WHERE LOWER(ic1.category) = %s AND LOWER(ic2.category) = %s AND LOWER(ic1.category) != LOWER(ic2.category)
            GROUP BY i1.username
            HAVING COUNT(DISTINCT i1.itemID) >= 1 AND COUNT(DISTINCT i2.itemID) >= 1
            """
        self.server.database_cursor.execute(query, (category_x.lower(), category_y.lower()))
        users = self.server.database_cursor.fetchall()
        return [user[0] for user in users]

    def get_items_with_excellent_or_good_reviews(self, username):
        query = f"""
            SELECT i.title
            FROM {self.server.database}.item AS i
            JOIN {self.server.database}.user AS u ON i.username = u.username
            LEFT JOIN {self.server.database}.review AS r ON r.itemID = i.itemID
            WHERE u.username = %s
            GROUP BY i.itemID, i.title
            HAVING COUNT(r.itemID) > 0 AND SUM(r.score NOT IN ('Excellent', 'Good')) = 0
        """
        self.server.database_cursor.execute(query, (username,))
        items = self.server.database_cursor.fetchall()
        return [item[0] for item in items]

















