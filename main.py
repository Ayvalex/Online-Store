import tkinter as tk

from server import Server
from onlinestoregui import OnlineStoreGUI
from usermanager import UserManager
from itemmanager import ItemManager
from reviewmanager import ReviewManager


def main():
    # Initialize the database
    server = Server(host="localhost", user="root", password="Python440!")
    server.connect_server()
    server.create_database("440project")
    server.connect_database()
    server.create_user_table()
    server.create_item_table()
    server.create_item_category_table()
    server.create_review_table()
    server.create_favorite_table()

    # Create the user manager and item manager
    user_manager = UserManager(server)
    item_manager = ItemManager(server)
    review_manager = ReviewManager(server)

    # Create the GUI and start the application
    root = tk.Tk()
    app = OnlineStoreGUI(root, user_manager, item_manager, review_manager)
    root.mainloop()

    # Close the database connection
    # server.close()


if __name__ == "__main__":
    main()
