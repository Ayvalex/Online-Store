class ReviewManager:
    def __init__(self, server):
        self.server = server

    def has_already_reviewed(self, item_id, username):
        query = "SELECT * FROM review WHERE itemID = %s AND username = %s"
        self.server.database_cursor.execute(query, (item_id, username))
        return bool(self.server.database_cursor.fetchone())

    def add_review(self, item_id, rating, description, username):
        query = """
        INSERT INTO review (remark, score, reviewDate, username, itemID)
        VALUES (%s, %s, CURRENT_DATE, %s, %s)
        """
        self.server.database_cursor.execute(query, (description, rating, username, item_id))
        self.server.database_connection.commit()

