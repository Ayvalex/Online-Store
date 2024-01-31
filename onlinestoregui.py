import tkinter as tk
from tkinter import messagebox, ttk

from item import Item
from user import User


class OnlineStoreGUI:
    def __init__(self, root, user_manager, item_manager, review_manager):
        self.users_with_items_without_poor_reviews = None
        self.users_with_only_poor_reviews = None
        self.users_without_poor_reviews = None
        self.users_without_excellent_items = None
        self.users_that_are_favorited_by_x_and_y = None
        self.user_that_posted_the_most_items = None
        self.items_with_excellent_or_good_reviews = None
        self.users_with_same_day_posts = None
        self.most_expensive_items_table = None
        self.result_table = None
        self.root = root
        self.user_manager = user_manager
        self.item_manager = item_manager
        self.review_manager = review_manager
        self.root.title("Online Store")

        # Create frames
        self.frame_main = tk.Frame(self.root)
        self.frame_registration = tk.Frame(self.root)
        self.frame_login = tk.Frame(self.root)
        self.frame_store = tk.Frame(self.root)
        self.frame_post_item = tk.Frame(self.root)
        self.frame_search = tk.Frame(self.root)
        self.frame_review = tk.Frame(self.root)
        self.frame_part_three_one = tk.Frame(self.root)
        self.frame_part_three_two = tk.Frame(self.root)
        self.frame_part_three_three = tk.Frame(self.root)
        self.frame_part_three_four = tk.Frame(self.root)
        self.frame_part_three_five = tk.Frame(self.root)
        self.frame_part_three_six = tk.Frame(self.root)
        self.frame_part_three_seven = tk.Frame(self.root)
        self.frame_part_three_eight = tk.Frame(self.root)
        self.frame_part_three_nine = tk.Frame(self.root)
        self.frame_part_three_ten = tk.Frame(self.root)

        self.register_button = tk.Button(self.frame_main, text="Register", command=self.initialize_register)
        self.login_button = tk.Button(self.frame_main, text="Login", command=self.initialize_login)
        self.database_button = tk.Button(self.frame_main, text="Initialize Database", command=self.initialize_database)

        self.username_entry = tk.Entry(self.frame_registration)
        self.password_entry = tk.Entry(self.frame_registration, show="*")
        self.password_confirm_entry = tk.Entry(self.frame_registration, show="*")
        self.first_name_entry = tk.Entry(self.frame_registration)
        self.last_name_entry = tk.Entry(self.frame_registration)
        self.email_entry = tk.Entry(self.frame_registration)

        self.login_username_entry = tk.Entry(self.frame_login)
        self.login_password_entry = tk.Entry(self.frame_login, show="*")

        self.post_item_button = tk.Button(self.frame_store, text="Post an Item", command=self.initialize_post_item)
        self.search_by_category_button = tk.Button(self.frame_store, text="Search by Category",
                                                   command=self.initialize_search)

        self.expensive_item_by_category_button = tk.Button(self.frame_store,
                                                           text="Most Expensive Item in Each Category",
                                                           command=self.initialize_part_three_one)

        self.users_with_same_day_posts_different_category = tk.Button(self.frame_store,
                                                                      text="Users that posted two items on the same day"
                                                                           " with each item being in a different"
                                                                           " category",
                                                                      command=self.initialize_part_three_two)

        self.items_with_only_excellent_or_good_reviews = tk.Button(self.frame_store,
                                                                   text="Items that only received excellent or good"
                                                                        " reviews",
                                                                   command=self.initialize_part_three_three)

        self.user_that_posted_the_most_items_button = tk.Button(self.frame_store,
                                                                text="Users that posted the most number of items "
                                                                     "since 5/1/2020",
                                                                command=self.initialize_part_three_four)

        self.users_that_are_favorited_by_x_and_y_button = tk.Button(self.frame_store,
                                                                text="Users who are favorited by both users X and Y",
                                                                command=self.initialize_part_three_five)

        self.users_without_excellent_items_button = tk.Button(self.frame_store,
                                                                    text="Users who have never posted any excellent "
                                                                         "items",
                                                                    command=self.initialize_part_three_six)

        self.users_without_poor_reviews_button = tk.Button(self.frame_store,
                                                              text="Users who never posted a poor review",
                                                              command=self.initialize_part_three_seven)

        self.users_with_only_poor_reviews_button = tk.Button(self.frame_store,
                                                              text="Users who posted some reviews, but all of them are "
                                                                   "poor",
                                                              command=self.initialize_part_three_eight)

        self.users_with_items_without_poor_reviews_button = tk.Button(self.frame_store,
                                                             text="Users with no poor reivews for any of their items",
                                                             command=self.initialize_part_three_nine)

        self.users_with_always_excellent_reviews_for_each_other_button = tk.Button(self.frame_store,
                                                             text="Users pairs that have only given each other "
                                                                  "excellent reviews for each of their items",
                                                             command=self.initialize_part_three_ten)

        self.logout_button = tk.Button(self.frame_store, text="Logout", command=self.initialize_main)

        self.title_entry = tk.Entry(self.frame_post_item)
        self.description_entry = tk.Entry(self.frame_post_item)
        self.category_entry = tk.Entry(self.frame_post_item)
        self.price_entry = tk.Entry(self.frame_post_item)

        self.listbox = tk.Listbox(self.frame_part_three_one)

        self.category_input_one = tk.Entry(self.frame_part_three_two)
        self.category_input_two = tk.Entry(self.frame_part_three_two)

        self.user = tk.Entry(self.frame_part_three_three)

        self.initialize_main()

    def initialize_main(self):
        self.clear_frames()
        self.clear_entries()
        self.frame_main.pack()

        self.register_button.pack(padx=5, pady=5)
        self.login_button.pack(padx=5, pady=5)
        self.database_button.pack(padx=5, pady=5)

    def initialize_part_three_one(self):
        self.clear_frames()
        self.frame_part_three_one.pack()

        self.most_expensive_items_table = ttk.Treeview(self.frame_part_three_one,
                                                       columns=("Category", "Title", "Price"),
                                                       show='headings')
        self.most_expensive_items_table.heading("Category", text="Category")
        self.most_expensive_items_table.heading("Title", text="Title")
        self.most_expensive_items_table.heading("Price", text="Price")
        self.most_expensive_items_table.grid(row=0, column=0, pady=10)

        # Create a back button
        back_button = tk.Button(self.frame_part_three_one, text="Back", command=self.initialize_store)
        back_button.grid(row=1, column=0)

        self.display_most_expensive_items_by_category()

    def display_most_expensive_items_by_category(self):
        self.most_expensive_items_table.delete(*self.most_expensive_items_table.get_children())
        items = self.item_manager.most_expensive_items_by_category()

        for item in items:
            self.most_expensive_items_table.insert("", "end", values=(item["category"], item["title"], item["price"]))

    def initialize_part_three_two(self):
        self.clear_frames()
        self.frame_part_three_two.pack()

        # Create and place the first text field with a label
        category_one_label = ttk.Label(self.frame_part_three_two, text="First Category:")
        category_one_label.grid(row=0, column=0, padx=10, pady=5)
        self.category_input_one.grid(row=0, column=1, padx=10, pady=5)

        # Create and place the second text field with a label
        category_two_label = ttk.Label(self.frame_part_three_two, text="Second Category:")
        category_two_label.grid(row=1, column=0, padx=10, pady=5)
        self.category_input_two.grid(row=1, column=1, padx=10, pady=5)

        # Create and place the submit button
        submit_button = ttk.Button(self.frame_part_three_two, text="Submit",
                                   command=lambda: self.display_users(self.category_input_one.get(),
                                                                      self.category_input_two.get()))
        submit_button.grid(row=2, column=0, padx=10, pady=5)

        # Create and place the back button
        back_button = ttk.Button(self.frame_part_three_two, text="Back", command=self.initialize_store)
        back_button.grid(row=2, column=1, padx=10, pady=5)

        # Create and place the table
        self.users_with_same_day_posts = ttk.Treeview(self.frame_part_three_two, columns=("Username",), show='headings')
        self.users_with_same_day_posts.heading("Username", text="Username")
        self.users_with_same_day_posts.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    def display_users(self, category_x, category_y):
        self.users_with_same_day_posts.delete(*self.users_with_same_day_posts.get_children())
        users = self.item_manager.get_users_that_posted_two_items_same_day(category_x, category_y)

        for user in users:
            self.users_with_same_day_posts.insert("", "end", values=user)

    def initialize_part_three_three(self):
        self.clear_frames()
        self.frame_part_three_three.pack()

        # Create and place the first text field with a label
        user_label = ttk.Label(self.frame_part_three_three, text="Username:")
        user_label.grid(row=0, column=0, padx=10, pady=5)
        self.user.grid(row=0, column=1, padx=10, pady=5)

        # Create and place the submit button
        submit_button = ttk.Button(self.frame_part_three_three, text="Submit",
                                   command=lambda: self.display_items(self.user.get().strip()))
        submit_button.grid(row=2, column=0, padx=10, pady=5)

        # Create and place the back button
        back_button = ttk.Button(self.frame_part_three_three, text="Back", command=self.initialize_store)
        back_button.grid(row=2, column=1, padx=10, pady=5)

        # Create and place the table
        self.items_with_excellent_or_good_reviews = ttk.Treeview(self.frame_part_three_three, columns=("Item",),
                                                                 show='headings')
        self.items_with_excellent_or_good_reviews.heading("Item", text="Item")
        self.items_with_excellent_or_good_reviews.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

    def display_items(self, username):
        self.items_with_excellent_or_good_reviews.delete(*self.items_with_excellent_or_good_reviews.get_children())
        items = self.item_manager.get_items_with_excellent_or_good_reviews(username)

        for item in items:
            self.items_with_excellent_or_good_reviews.insert("", "end", values=(item,))

    def initialize_part_three_four(self):
        self.clear_frames()
        self.frame_part_three_four.pack()

        self.user_that_posted_the_most_items = ttk.Treeview(self.frame_part_three_four,
                                                            columns=("Username",),
                                                            show='headings')
        self.user_that_posted_the_most_items.heading("Username", text="Username")
        self.user_that_posted_the_most_items.grid(row=0, column=0, pady=10)

        back_button = ttk.Button(self.frame_part_three_four, text="Back", command=self.initialize_store)
        back_button.grid(row=1, column=0, pady=10)

        self.display_user_that_posted_the_most_items()

    def display_user_that_posted_the_most_items(self):
        self.user_that_posted_the_most_items.delete(*self.user_that_posted_the_most_items.get_children())
        items = self.user_manager.get_user_that_posted_the_most_times_since_date()

        for item in items:
            self.user_that_posted_the_most_items.insert("", "end", values=item)

    def initialize_part_three_five(self):
        self.clear_frames()
        self.frame_part_three_five.pack()

        # Create a label for the first dropdown menu
        tk.Label(self.frame_part_three_five, text="Select user X").grid(row=0, column=0)

        # Create the first dropdown menu
        self.selected_user_x = tk.StringVar()
        user_x_options = self.user_manager.get_all_usernames()
        tk.OptionMenu(self.frame_part_three_five, self.selected_user_x, *user_x_options).grid(row=0, column=1)

        # Create a label for the second dropdown menu
        tk.Label(self.frame_part_three_five, text="Select user Y").grid(row=1, column=0)

        # Create the second dropdown menu
        self.selected_user_y = tk.StringVar()
        user_y_options = self.user_manager.get_all_usernames()
        tk.OptionMenu(self.frame_part_three_five, self.selected_user_y, *user_y_options).grid(row=1, column=1)

        # Create the submit button
        tk.Button(self.frame_part_three_five, text="Submit",
                  command=self.display_users_that_are_favorited_by_x_and_y).grid(row=2, column=0, columnspan=2)

        # Create the treeview to display the mutual favorites
        self.users_that_are_favorited_by_x_and_y = ttk.Treeview(self.frame_part_three_five,
                                                                columns=("Username",),
                                                                show='headings')
        self.users_that_are_favorited_by_x_and_y.heading("Username", text="Username")
        self.users_that_are_favorited_by_x_and_y.grid(row=3, column=0, columnspan=2, pady=10)

        back_button = ttk.Button(self.frame_part_three_five, text="Back", command=self.initialize_store)
        back_button.grid(row=4, column=0, columnspan=2, pady=10)

    def display_users_that_are_favorited_by_x_and_y(self):
        self.users_that_are_favorited_by_x_and_y.delete(*self.users_that_are_favorited_by_x_and_y.get_children())
        user_x = self.selected_user_x.get()
        user_y = self.selected_user_y.get()

        if user_x != "" and user_y != "":
            users = self.user_manager.get_mutual_favorites(user_x, user_y)

            for user in users:
                self.users_that_are_favorited_by_x_and_y.insert("", "end", values=(user,))

    def initialize_part_three_six(self):
        self.clear_frames()
        self.frame_part_three_six.pack()

        self.users_without_excellent_items = ttk.Treeview(self.frame_part_three_six,
                                                          columns=("Username",),
                                                          show='headings')
        self.users_without_excellent_items.heading("Username", text="Username")
        self.users_without_excellent_items.grid(row=0, column=0, pady=10)

        self.display_users_without_excellent_items()

        back_button = ttk.Button(self.frame_part_three_six, text="Back", command=self.initialize_store)
        back_button.grid(row=1, column=0, pady=10)

    def display_users_without_excellent_items(self):
        self.users_without_excellent_items.delete(*self.users_without_excellent_items.get_children())
        users = self.user_manager.get_users_without_excellent_items()

        for user in users:
            self.users_without_excellent_items.insert("", "end", values=user)

    def initialize_part_three_seven(self):
        self.clear_frames()
        self.frame_part_three_seven.pack()

        self.users_without_poor_reviews = ttk.Treeview(self.frame_part_three_seven,
                                                       columns=("Username",),
                                                       show='headings')
        self.users_without_poor_reviews.heading("Username", text="Username")
        self.users_without_poor_reviews.grid(row=0, column=0, pady=10)

        self.display_users_without_poor_reviews()

        back_button = ttk.Button(self.frame_part_three_seven, text="Back", command=self.initialize_store)
        back_button.grid(row=1, column=0, pady=10)

    def display_users_without_poor_reviews(self):
        self.users_without_poor_reviews.delete(*self.users_without_poor_reviews.get_children())
        users = self.user_manager.get_users_without_poor_reviews()

        for user in users:
            self.users_without_poor_reviews.insert("", "end", values=user)

    def initialize_part_three_eight(self):
        self.clear_frames()
        self.frame_part_three_eight.pack()

        self.users_with_only_poor_reviews = ttk.Treeview(self.frame_part_three_eight,
                                                         columns=("Username",),
                                                         show='headings')
        self.users_with_only_poor_reviews.heading("Username", text="Username")
        self.users_with_only_poor_reviews.grid(row=0, column=0, pady=10)

        self.display_users_with_only_poor_reviews()

        back_button = ttk.Button(self.frame_part_three_eight, text="Back", command=self.initialize_store)
        back_button.grid(row=1, column=0, pady=10)

    def display_users_with_only_poor_reviews(self):
        self.users_with_only_poor_reviews.delete(*self.users_with_only_poor_reviews.get_children())
        users = self.user_manager.get_users_with_only_poor_reviews()

        for user in users:
            self.users_with_only_poor_reviews.insert("", "end", values=user)
            
    def initialize_part_three_nine(self):
        self.clear_frames()
        self.frame_part_three_nine.pack()

        self.users_with_items_without_poor_reviews = ttk.Treeview(self.frame_part_three_nine,
                                                                  columns=("Username",),
                                                                  show='headings')
        self.users_with_items_without_poor_reviews.heading("Username", text="Username")
        self.users_with_items_without_poor_reviews.grid(row=0, column=0, pady=10)

        self.display_users_with_items_without_poor_reviews()

        back_button = ttk.Button(self.frame_part_three_nine, text="Back", command=self.initialize_store)
        back_button.grid(row=1, column=0, pady=10)

    def display_users_with_items_without_poor_reviews(self):
        self.users_with_items_without_poor_reviews.delete(*self.users_with_items_without_poor_reviews.get_children())
        users = self.user_manager.get_users_with_no_poor_review_items()

        for user in users:
            self.users_with_items_without_poor_reviews.insert("", "end", values=user)

    def initialize_part_three_ten(self):
        self.clear_frames()
        self.frame_part_three_ten.pack()

        self.users_with_always_excellent_reviews_for_each_other = ttk.Treeview(
            self.frame_part_three_ten,
            columns=("User A", "User B"),
            show='headings'
        )
        self.users_with_always_excellent_reviews_for_each_other.heading("User A", text="User A")
        self.users_with_always_excellent_reviews_for_each_other.heading("User B", text="User B")

        self.users_with_always_excellent_reviews_for_each_other.grid(row=0, column=0, pady=10)

        self.display_users_with_always_excellent_reviews_for_each_other()

        back_button = ttk.Button(self.frame_part_three_ten, text="Back", command=self.initialize_store)
        back_button.grid(row=1, column=0, pady=10)

    def display_users_with_always_excellent_reviews_for_each_other(self):
        self.users_with_always_excellent_reviews_for_each_other.delete(*self.users_with_always_excellent_reviews_for_each_other.get_children())
        users = self.user_manager.get_excellent_review_pairs()
        print(users)
        for user in users:
            self.users_with_always_excellent_reviews_for_each_other.insert("", "end", values=(user["username_A"], user["username_B"]))

    def initialize_register(self):
        self.clear_frames()

        self.frame_registration.pack()

        username_label = tk.Label(self.frame_registration, text="Username")
        password_label = tk.Label(self.frame_registration, text="Password")
        password_confirm_label = tk.Label(self.frame_registration, text="Confirm Password")
        first_name_label = tk.Label(self.frame_registration, text="First Name")
        last_name_label = tk.Label(self.frame_registration, text="Last Name")
        email_label = tk.Label(self.frame_registration, text="Email")

        register_submit_button = tk.Button(self.frame_registration, text="Register", command=self.register_user)
        register_back_button = tk.Button(self.frame_registration, text="Back", command=self.initialize_main)

        username_label.grid(row=0, column=0)
        password_label.grid(row=1, column=0)
        password_confirm_label.grid(row=2, column=0)
        first_name_label.grid(row=3, column=0)
        last_name_label.grid(row=4, column=0)
        email_label.grid(row=5, column=0)

        self.username_entry.grid(row=0, column=1)
        self.password_entry.grid(row=1, column=1)
        self.password_confirm_entry.grid(row=2, column=1)
        self.first_name_entry.grid(row=3, column=1)
        self.last_name_entry.grid(row=4, column=1)
        self.email_entry.grid(row=5, column=1)

        register_submit_button.grid(row=6, column=1, pady=10)
        register_back_button.grid(row=6, column=0, pady=10)

    def register_user(self):
        user = User(username=self.username_entry.get(),
                    password=self.password_entry.get(),
                    confirm_password=self.password_confirm_entry.get(),
                    first_name=self.first_name_entry.get(),
                    last_name=self.last_name_entry.get(),
                    email=self.email_entry.get())

        if self.user_manager.register(user):
            self.initialize_main()

    def initialize_login(self):
        self.clear_frames()

        self.frame_login.pack()

        username_label = tk.Label(self.frame_login, text="Username")
        password_label = tk.Label(self.frame_login, text="Password")

        login_submit_button = tk.Button(self.frame_login, text="Login", command=self.login_user)
        login_back_button = tk.Button(self.frame_login, text="Back", command=self.initialize_main)

        username_label.grid(row=0, column=0)
        password_label.grid(row=1, column=0)

        self.login_username_entry.grid(row=0, column=1)
        self.login_password_entry.grid(row=1, column=1)
        login_submit_button.grid(row=2, column=1, pady=10)
        login_back_button.grid(row=2, column=0, pady=10)

    def login_user(self):
        user = User(username=self.login_username_entry.get(),
                    password=self.login_password_entry.get())

        if self.user_manager.login(user):
            self.initialize_store()

    def initialize_database(self):
        self.user_manager.initialize_database()
        messagebox.showinfo("Database Initialized", "All the tables have been reset with example data.")

    def clear_frames(self):
        for frame in [self.frame_main, self.frame_registration, self.frame_login, self.frame_store,
                      self.frame_post_item, self.frame_search, self.frame_review, self.frame_part_three_one,
                      self.frame_part_three_two, self.frame_part_three_three, self.frame_part_three_four,
                      self.frame_part_three_five, self.frame_part_three_six, self.frame_part_three_seven,
                      self.frame_part_three_eight, self.frame_part_three_nine, self.frame_part_three_ten]:
            frame.pack_forget()

    def clear_entries(self):
        # Clear all input fields
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.password_confirm_entry.delete(0, tk.END)
        self.first_name_entry.delete(0, tk.END)
        self.last_name_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.login_username_entry.delete(0, tk.END)
        self.login_password_entry.delete(0, tk.END)
        self.title_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)

    def initialize_store(self):
        self.clear_frames()

        self.frame_store.pack()
        self.clear_entries()

        self.post_item_button.pack(padx=5, pady=5)
        self.search_by_category_button.pack(padx=5, pady=5)
        self.expensive_item_by_category_button.pack(padx=5, pady=5)
        self.users_with_same_day_posts_different_category.pack(padx=5, pady=5)
        self.items_with_only_excellent_or_good_reviews.pack(padx=5, pady=5)
        self.user_that_posted_the_most_items_button.pack(padx=5, pady=5)
        self.users_that_are_favorited_by_x_and_y_button.pack(padx=5, pady=5)
        self.users_without_excellent_items_button.pack(padx=5, pady=5)
        self.users_without_poor_reviews_button.pack(padx=5, pady=5)
        self.users_with_only_poor_reviews_button.pack(padx=5, pady=5)
        self.users_with_items_without_poor_reviews_button.pack(padx=5, pady=5)
        self.users_with_always_excellent_reviews_for_each_other_button.pack(padx=5, pady=5)
        self.logout_button.pack(padx=5, pady=5)

    def initialize_post_item(self):
        self.clear_frames()

        self.frame_post_item.pack()

        title_label = tk.Label(self.frame_post_item, text="Title")
        description_label = tk.Label(self.frame_post_item, text="Description")
        category_label = tk.Label(self.frame_post_item, text="Category")
        price_label = tk.Label(self.frame_post_item, text="Price")

        post_item_submit_button = tk.Button(self.frame_post_item, text="Post Item", command=self.post_item)
        post_item_back_button = tk.Button(self.frame_post_item, text="Back", command=self.initialize_store)

        title_label.grid(row=0, column=0)
        description_label.grid(row=1, column=0)
        category_label.grid(row=2, column=0)
        price_label.grid(row=3, column=0)

        self.title_entry.grid(row=0, column=1)
        self.description_entry.grid(row=1, column=1)
        self.category_entry.grid(row=2, column=1)
        self.price_entry.grid(row=3, column=1)

        post_item_submit_button.grid(row=4, column=1, pady=10)
        post_item_back_button.grid(row=4, column=0, pady=10)

    def post_item(self):
        item = Item(title=self.title_entry.get(),
                    description=self.description_entry.get(),
                    category=self.category_entry.get(),
                    price=self.price_entry.get())

        if self.item_manager.post_item(item, self.user_manager):
            messagebox.showinfo("Item Posted", "Item has been added to the item table")
            self.clear_entries()

    '''def search_by_category(self):
        self.clear_frames()
        self.initialize_search()'''

    def logout_user(self):
        self.initialize_main()
        self.user_manager.current_user = None

    def initialize_search(self):
        self.clear_frames()
        self.frame_search.pack()

        search_label = tk.Label(self.frame_search, text="Search by Category:")
        search_entry = tk.Entry(self.frame_search)
        search_button = tk.Button(self.frame_search, text="Search",
                                  command=lambda: self.search_results(search_entry.get()))
        back_button = tk.Button(self.frame_search, text="Back", command=self.initialize_store)

        search_label.grid(row=0, column=0)
        search_entry.grid(row=0, column=1)
        search_button.grid(row=0, column=2)
        back_button.grid(row=0, column=3)

        self.result_table = ttk.Treeview(self.frame_search,
                                         columns=("Title", "Description", "Price", "Username", "Post Date"),
                                         show='headings')
        self.result_table.heading("Title", text="Title")
        self.result_table.heading("Description", text="Description")
        self.result_table.heading("Price", text="Price")
        self.result_table.heading("Username", text="Username")
        self.result_table.heading("Post Date", text="Post Date")
        self.result_table.grid(row=1, column=0, columnspan=4, pady=10)

    def search_results(self, category):
        self.result_table.delete(*self.result_table.get_children())
        items = self.item_manager.get_items_by_category(category)
        for item in items:
            self.result_table.insert("", "end", values=(item["title"], item["description"], item["price"],
                                                        item["username"], item["post_date"]), tags=(item["item_id"],))
        self.result_table.bind("<Double-1>", self.select_item)

    def select_item(self, event):
        selected_item = self.result_table.focus()
        item_data = self.result_table.item(selected_item, "values")
        item_id = self.result_table.item(selected_item, "tags")[0]

        if self.user_manager.current_user.username == item_data[3]:
            messagebox.showerror("Error", "You cannot review your own item.")
        elif self.review_manager.has_already_reviewed(item_id, self.user_manager.current_user.username):
            messagebox.showerror("Error", "You have already reviewed this item.")
        else:
            self.initialize_review(item_id, item_data)

    def initialize_review(self, item_id, item_data):
        self.clear_frames()
        self.frame_review.pack()

        def clean_string(text):
            return ''.join(c for c in text if c.isprintable() and c not in (';', ':', ',', '.'))

        cleaned_item_title = clean_string(item_data[0])

        review_label = tk.Label(self.frame_review, text=f"Reviewing Item: {cleaned_item_title}")

        rating_label = tk.Label(self.frame_review, text="Rating:")
        rating_var = tk.StringVar(self.frame_review)
        rating_var.set("Choose Rating")
        rating_dropdown = ttk.Combobox(self.frame_review, textvariable=rating_var,
                                       values=("excellent", "good", "fair", "poor"), state="readonly")
        description_label = tk.Label(self.frame_review, text="Description:")
        description_entry = tk.Entry(self.frame_review)
        submit_button = tk.Button(self.frame_review, text="Submit Review",
                                  command=lambda: self.submit_review(item_id, rating_var.get(),
                                                                     description_entry.get()))
        back_button = tk.Button(self.frame_review, text="Back", command=self.initialize_search)

        review_label.grid(row=0, column=0, columnspan=2, pady=10)
        rating_label.grid(row=1, column=0)
        rating_dropdown.grid(row=1, column=1)
        description_label.grid(row=2, column=0)
        description_entry.grid(row=2, column=1)
        submit_button.grid(row=3, column=0, columnspan=2, pady=10)
        back_button.grid(row=4, column=0, columnspan=2)

    def submit_review(self, item_id, rating, description):
        if self.user_manager.can_submit_review():
            if rating != "Choose Rating" and description:
                self.review_manager.add_review(item_id, rating, description,
                                               self.user_manager.current_user.username)
                messagebox.showinfo("Success", "Review submitted successfully.")
                self.initialize_search()
            else:
                messagebox.showerror("Error", "Please choose a rating and provide a description.")
        else:
            messagebox.showerror("Error", "You can only submit 3 reviews per day.")
