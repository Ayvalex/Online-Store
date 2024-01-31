import re
from tkinter import messagebox


class UserManager:
    def __init__(self, server):
        self.server = server
        self.current_user = None

    def _helper_validate_registration(self, user):
        errors = []

        if len(user.username) == 0:
            errors.append("Username is required.")

        if len(user.password) == 0:
            errors.append("Password is required.")

        if len(user.confirm_password) == 0:
            errors.append("Please confirm password.")

        if len(user.first_name) == 0:
            errors.append("First name is required.")

        if len(user.last_name) == 0:
            errors.append("Last name is required.")

        if len(user.email) == 0:
            errors.append("Email is required.")
        else:
            # Check for valid email format
            if not re.match(r"[^@]+@[^@]+\.[^@]+", user.email):
                errors.append("Invalid email format.")

        if user.password != user.confirm_password:
            errors.append("Passwords do not match.")

        # Check for duplicate username
        self.server.database_cursor.execute("SELECT * FROM user WHERE username = %s", (user.username,))
        result = self.server.database_cursor.fetchone()
        if result:
            errors.append("Username already exists.")

        # Check for duplicate email
        self.server.database_cursor.execute("SELECT * FROM user WHERE email = %s", (user.email,))
        result = self.server.database_cursor.fetchone()
        if result:
            errors.append("Email already exists.")

        if len(errors) > 0:
            return errors
        else:
            return True

    def register(self, user):
        validation_result = self._helper_validate_registration(user)

        if isinstance(validation_result, bool) and validation_result:
            messagebox.showinfo("Success", "Registration successful.")
            query = "INSERT INTO user (username, password, firstName, lastName, email) VALUES (%s, %s, %s, %s, %s)"
            self.server.database_cursor.execute(query, (user.username, user.password, user.first_name, user.last_name,
                                                        user.email))
            self.server.database_connection.commit()
            return True
        else:
            messagebox.showerror("Registration Error", "\n".join(validation_result))

    def _helper_validate_login(self, user):
        errors = []

        if len(user.username) == 0:
            errors.append("Username is required.")

        if len(user.password) == 0:
            errors.append("Password is required.")

        # Check if there is a user that has such a username and password
        if not errors:
            self.server.database_cursor.execute("SELECT * FROM user WHERE username = %s and password = %s",
                                                (user.username, user.password,))
            result = self.server.database_cursor.fetchone()
            if not result:
                errors.append("Incorrect username or password.")

        if len(errors) > 0:
            return errors
        else:
            return True

    def login(self, user):
        validation_result = self._helper_validate_login(user)

        if isinstance(validation_result, bool) and validation_result:
            self.current_user = user
            return True
        else:
            messagebox.showerror("Login Error", "\n".join(validation_result))

    def initialize_database(self):
        self.server.initialize_database()

    def can_submit_review(self):
        if not self.current_user:
            return False
        self.server.database_cursor.execute(
            "SELECT COUNT(*) FROM review WHERE username = %s AND reviewDate = CURRENT_DATE",
            (self.current_user.username,))
        review_count = self.server.database_cursor.fetchone()[0]
        return review_count < 3

    def get_user_that_posted_the_most_times_since_date(self, start_date="2020-05-01"):
        query = f"""
               SELECT u.username
               FROM {self.server.database}.user AS u
               JOIN {self.server.database}.item AS i ON u.username = i.username
               WHERE i.postDate >= %s
               GROUP BY u.username
               HAVING COUNT(i.itemID) = (
                   SELECT COUNT(itemID) AS maxItemCount
                   FROM {self.server.database}.item
                   WHERE postDate >= %s
                   GROUP BY username
                   ORDER BY maxItemCount DESC
                   LIMIT 1
               )
               ORDER BY u.username
           """
        self.server.database_cursor.execute(query, (start_date, start_date))
        users = self.server.database_cursor.fetchall()
        return [user[0] for user in users]

    '''def get_user_that_posted_the_most_times_since_date(self):
        date = "2020-05-01"
        query = f"""
            SELECT u.username, COUNT(i.itemID) as num_items
            FROM {self.server.database}.user u
            JOIN {self.server.database}.item i ON u.username = i.username
            WHERE i.postDate >= %s
            GROUP BY u.username
            ORDER BY num_items DESC
        """
        self.server.database_cursor.execute(query, (date,))
        users_items = self.server.database_cursor.fetchall()

        top_users = []
        max_items = 0

        for user in users_items:
            username, num_items = user

            if num_items > max_items:
                top_users = [username]
                max_items = num_items
            elif num_items == max_items:
                top_users.append(username)
            else:
                break

        return top_users'''

    def get_mutual_favorites(self, user_x, user_y):
        query = f"""
            SELECT f1.favorite_seller
            FROM {self.server.database}.favorite f1
            JOIN {self.server.database}.favorite f2 ON f1.favorite_seller = f2.favorite_seller
            WHERE f1.username = %s AND f2.username = %s
        """
        self.server.database_cursor.execute(query, (user_x, user_y))
        mutual_favorites = self.server.database_cursor.fetchall()
        return [favorite[0] for favorite in mutual_favorites]

    def get_all_usernames(self):
        self.server.database_cursor.execute("SELECT username FROM user")
        usernames = self.server.database_cursor.fetchall()
        return [username[0] for username in usernames]

    def get_users_without_excellent_items(self):
        query = f"""
            SELECT u.username
            FROM {self.server.database}.user AS u
            WHERE NOT EXISTS (
                SELECT 1
                FROM {self.server.database}.item AS i
                JOIN {self.server.database}.review AS r ON i.itemID = r.itemID
                WHERE i.username = u.username AND r.score = 'Excellent'
                GROUP BY i.itemID
                HAVING COUNT(r.reviewID) >= 3
            )
        """
        self.server.database_cursor.execute(query)
        users = self.server.database_cursor.fetchall()
        return [user[0] for user in users]

    def get_users_without_poor_reviews(self):
        query = f"""
            SELECT u.username
            FROM {self.server.database}.user AS u
            WHERE NOT EXISTS (
                SELECT 1
                FROM {self.server.database}.review AS r
                WHERE r.username = u.username AND r.score = 'Poor'
            )
        """
        self.server.database_cursor.execute(query)
        users = self.server.database_cursor.fetchall()
        return [user[0] for user in users]

    def get_users_with_only_poor_reviews(self):
        query = f"""
            SELECT u.username
            FROM {self.server.database}.user AS u
            WHERE EXISTS (
                SELECT 1
                FROM {self.server.database}.review AS r
                WHERE r.username = u.username
            ) AND NOT EXISTS (
                SELECT 1
                FROM {self.server.database}.review AS r
                WHERE r.username = u.username AND r.score != 'Poor'
            )
        """
        self.server.database_cursor.execute(query)
        users = self.server.database_cursor.fetchall()
        return [user[0] for user in users]

    def get_users_with_no_poor_review_items(self):
        query = f"""
            SELECT u.username
            FROM {self.server.database}.user AS u
            WHERE EXISTS (
                SELECT 1
                FROM {self.server.database}.item AS i
                WHERE i.username = u.username
            ) AND NOT EXISTS (
                SELECT 1
                FROM {self.server.database}.item AS i
                JOIN {self.server.database}.review AS r ON i.itemID = r.itemID
                WHERE i.username = u.username AND r.score = 'Poor'
            )
        """
        self.server.database_cursor.execute(query)
        users = self.server.database_cursor.fetchall()
        return [user[0] for user in users]

    def get_excellent_review_pairs(self):
        query = f"""
                SELECT A.username, B.username
                FROM {self.server.database}.user AS A, {self.server.database}.user AS B
                WHERE A.username < B.username
                AND EXISTS (
                    SELECT 1
                    FROM {self.server.database}.item
                    WHERE username = A.username
                )
                AND EXISTS (
                    SELECT 1
                    FROM {self.server.database}.item
                    WHERE username = B.username
                )
                AND NOT EXISTS (
                    SELECT 1
                    FROM {self.server.database}.item AS i1
                    WHERE i1.username = A.username AND NOT EXISTS (
                        SELECT 1
                        FROM {self.server.database}.review AS r1
                        WHERE i1.itemID = r1.itemID AND r1.username = B.username AND r1.score = 'Excellent'
                    )
                )
                AND NOT EXISTS (
                    SELECT 1
                    FROM {self.server.database}.item AS i2
                    WHERE i2.username = B.username AND NOT EXISTS (
                        SELECT 1
                        FROM {self.server.database}.review AS r2
                        WHERE i2.itemID = r2.itemID AND r2.username = A.username AND r2.score = 'Excellent'
                    )
                )
            """
        self.server.database_cursor.execute(query)
        user_pairs = self.server.database_cursor.fetchall()
        keys = ["username_A", "username_B"]
        return [dict(zip(keys, user)) for user in user_pairs]











