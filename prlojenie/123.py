import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import sqlite3
import ttkbootstrap as ttkb

# Создание и подключение к базе данных
conn = sqlite3.connect('pc_shop.db')
cursor = conn.cursor()

# Создание таблиц
cursor.executescript('''
CREATE TABLE IF NOT EXISTS Role (
    Role_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Product_Types (
    Type_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS Users (
    User_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL,
    Password TEXT NOT NULL,
    Role_id INTEGER NOT NULL,
    FOREIGN KEY (Role_id) REFERENCES Role(Role_id)
);

CREATE TABLE IF NOT EXISTS Products (
    Product_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Price REAL NOT NULL,
    Quantity INTEGER NOT NULL,
    Type_id INTEGER NOT NULL,
    FOREIGN KEY (Type_id) REFERENCES Product_Types(Type_id)
);

CREATE TABLE IF NOT EXISTS Orders (
    Order_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Order_date DATE NOT NULL,
    Status TEXT NOT NULL,
    User_id INTEGER NOT NULL,
    FOREIGN KEY (User_id) REFERENCES Users(User_id)
);

CREATE TABLE IF NOT EXISTS Cart (
    Cart_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Product_id INTEGER NOT NULL,
    Quantity INTEGER NOT NULL,
    Order_id INTEGER NOT NULL,
    FOREIGN KEY (Product_id) REFERENCES Products(Product_id),
    FOREIGN KEY (Order_id) REFERENCES Orders(Order_id)
);

CREATE TABLE IF NOT EXISTS Payment (
    Payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Amount REAL NOT NULL,
    Payment_date DATE NOT NULL,
    Order_id INTEGER NOT NULL,
    FOREIGN KEY (Order_id) REFERENCES Orders(Order_id)
);

CREATE TABLE IF NOT EXISTS Reviews (
    Review_id INTEGER PRIMARY KEY AUTOINCREMENT,
    Product_id INTEGER NOT NULL,
    User_id INTEGER NOT NULL,
    Review TEXT NOT NULL,
    FOREIGN KEY (Product_id) REFERENCES Products(Product_id),
    FOREIGN KEY (User_id) REFERENCES Users(User_id)
);

INSERT INTO Role (Name) VALUES ('Administrator'), ('User');
INSERT INTO Product_Types (Name) VALUES ('Processor'), ('Motherboard'), ('RAM'), ('Graphics Card'), ('Hard Drive'), ('Power Supply'), ('Case');
INSERT INTO Users (Username, Password, Role_id) VALUES ('admin', 'admin123', 1), ('user1', 'password1', 2);

INSERT INTO Products (Name, Price, Quantity, Type_id) VALUES
('Intel Core i9', 45000.00, 10, 1),
('ASUS ROG STRIX', 15000.00, 5, 2),
('Corsair Vengeance 16GB', 8000.00, 20, 3),
('NVIDIA RTX 3080', 70000.00, 7, 4),
('Samsung 1TB SSD', 10000.00, 15, 5),
('Corsair 750W', 6000.00, 10, 6),
('NZXT H510', 7000.00, 8, 7);

INSERT INTO Orders (Order_date, Status, User_id) VALUES ('2023-06-01', 'New', 2);
INSERT INTO Cart (Product_id, Quantity, Order_id) VALUES (1, 1, 1), (2, 1, 1), (3, 2, 1), (4, 1, 1), (5, 1, 1), (6, 1, 1), (7, 1, 1);
INSERT INTO Payment (Amount, Payment_date, Order_id) VALUES (179000.00, '2023-06-02', 1);
''')

conn.commit()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Магазин ПК")
        self.root.geometry("800x600")
        
        self.create_login_page()

    def create_login_page(self):
        self.clear_frame()

        self.login_frame = ttkb.Frame(self.root, padding="10")
        self.login_frame.pack(expand=True)

        ttkb.Label(self.login_frame, text="Имя пользователя:", anchor="center").pack()
        self.username_entry = ttkb.Entry(self.login_frame)
        self.username_entry.pack()

        ttkb.Label(self.login_frame, text="Пароль:", anchor="center").pack()
        self.password_entry = ttkb.Entry(self.login_frame, show="*")
        self.password_entry.pack()

        self.login_button = ttkb.Button(self.login_frame, text="Войти", command=self.login)
        self.login_button.pack(pady=10)

        self.register_button = ttkb.Button(self.login_frame, text="Зарегистрироваться", command=self.create_register_page)
        self.register_button.pack()

    def create_register_page(self):
        self.clear_frame()

        self.register_frame = ttkb.Frame(self.root, padding="10")
        self.register_frame.pack(expand=True)

        ttkb.Label(self.register_frame, text="Имя пользователя:", anchor="center").pack()
        self.new_username_entry = ttkb.Entry(self.register_frame)
        self.new_username_entry.pack()

        ttkb.Label(self.register_frame, text="Пароль:", anchor="center").pack()
        self.new_password_entry = ttkb.Entry(self.register_frame, show="*")
        self.new_password_entry.pack()

        self.register_button = ttkb.Button(self.register_frame, text="Зарегистрироваться", command=self.register)
        self.register_button.pack(pady=10)

        self.back_button = ttkb.Button(self.register_frame, text="Назад", command=self.create_login_page)
        self.back_button.pack()

    def register(self):
        username = self.new_username_entry.get()
        password = self.new_password_entry.get()

        cursor.execute("SELECT * FROM Users WHERE Username = ?", (username,))
        if cursor.fetchone():
            messagebox.showerror("Ошибка", "Имя пользователя уже существует")
        else:
            cursor.execute("INSERT INTO Users (Username, Password, Role_id) VALUES (?, ?, 2)", (username, password))
            conn.commit()
            messagebox.showinfo("Успех", "Регистрация прошла успешно")
            self.create_login_page()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        cursor.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?", (username, password))
        user = cursor.fetchone()

        if user:
            self.user_id = user[0]
            self.user_role = user[3]
            if self.user_role == 1:
                self.create_admin_page()
            else:
                self.create_user_page()
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")

    def create_admin_page(self):
        self.clear_frame()

        self.admin_frame = ttkb.Frame(self.root, padding="10")
        self.admin_frame.pack(expand=True)

        self.manage_products_button = ttkb.Button(self.admin_frame, text="Управление товарами", command=self.manage_products)
        self.manage_products_button.pack(pady=10)

        self.manage_users_button = ttkb.Button(self.admin_frame, text="Управление пользователями", command=self.manage_users)
        self.manage_users_button.pack(pady=10)

        self.view_reviews_button = ttkb.Button(self.admin_frame, text="Просмотр отзывов", command=self.view_reviews)
        self.view_reviews_button.pack(pady=10)

        self.logout_button = ttkb.Button(self.admin_frame, text="Выйти", command=self.create_login_page)
        self.logout_button.pack(pady=10)

    def create_user_page(self):
        self.clear_frame()

        self.user_frame = ttkb.Frame(self.root, padding="10")
        self.user_frame.pack(expand=True)

        self.view_products_button = ttkb.Button(self.user_frame, text="Просмотр товаров", command=self.view_products)
        self.view_products_button.pack(pady=10)

        self.view_reviews_button = ttkb.Button(self.user_frame, text="Просмотр отзывов", command=self.view_reviews)
        self.view_reviews_button.pack(pady=10)

        self.leave_review_button = ttkb.Button(self.user_frame, text="Оставить отзыв", command=self.leave_review)
        self.leave_review_button.pack(pady=10)

        self.logout_button = ttkb.Button(self.user_frame, text="Выйти", command=self.create_login_page)
        self.logout_button.pack(pady=10)

    def manage_products(self):
        self.clear_frame()

        self.manage_products_frame = ttkb.Frame(self.root, padding="10")
        self.manage_products_frame.pack(expand=True)

        self.products_listbox = tk.Listbox(self.manage_products_frame)
        self.products_listbox.pack()

        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        for product in products:
            self.products_listbox.insert(tk.END, product)

        self.add_product_button = ttkb.Button(self.manage_products_frame, text="Добавить товар", command=self.add_product)
        self.add_product_button.pack(pady=10)

        self.edit_product_button = ttkb.Button(self.manage_products_frame, text="Изменить товар", command=self.edit_product)
        self.edit_product_button.pack(pady=10)

        self.delete_product_button = ttkb.Button(self.manage_products_frame, text="Удалить товар", command=self.delete_product)
        self.delete_product_button.pack(pady=10)

        self.back_button = ttkb.Button(self.manage_products_frame, text="Назад", command=self.create_admin_page)
        self.back_button.pack(pady=10)

    def add_product(self):
        self.clear_frame()

        self.add_product_frame = ttkb.Frame(self.root, padding="10")
        self.add_product_frame.pack(expand=True)

        ttkb.Label(self.add_product_frame, text="Название:", anchor="center").pack()
        self.product_name_entry = ttkb.Entry(self.add_product_frame)
        self.product_name_entry.pack()

        ttkb.Label(self.add_product_frame, text="Цена:", anchor="center").pack()
        self.product_price_entry = ttkb.Entry(self.add_product_frame)
        self.product_price_entry.pack()

        ttkb.Label(self.add_product_frame, text="Количество:", anchor="center").pack()
        self.product_quantity_entry = ttkb.Entry(self.add_product_frame)
        self.product_quantity_entry.pack()

        ttkb.Label(self.add_product_frame, text="Тип:", anchor="center").pack()
        self.product_type_entry = ttkb.Entry(self.add_product_frame)
        self.product_type_entry.pack()

        self.save_product_button = ttkb.Button(self.add_product_frame, text="Сохранить", command=self.save_product)
        self.save_product_button.pack(pady=10)

        self.back_button = ttkb.Button(self.add_product_frame, text="Назад", command=self.manage_products)
        self.back_button.pack(pady=10)

    def save_product(self):
        name = self.product_name_entry.get()
        price = float(self.product_price_entry.get())
        quantity = int(self.product_quantity_entry.get())
        type_id = int(self.product_type_entry.get())

        cursor.execute("INSERT INTO Products (Name, Price, Quantity, Type_id) VALUES (?, ?, ?, ?)", (name, price, quantity, type_id))
        conn.commit()
        messagebox.showinfo("Успех", "Товар добавлен успешно")
        self.manage_products()

    def edit_product(self):
        selected_product = self.products_listbox.curselection()
        if selected_product:
            product_id = self.products_listbox.get(selected_product[0])[0]
            self.clear_frame()

            self.edit_product_frame = ttkb.Frame(self.root, padding="10")
            self.edit_product_frame.pack(expand=True)

            cursor.execute("SELECT * FROM Products WHERE Product_id = ?", (product_id,))
            product = cursor.fetchone()

            ttkb.Label(self.edit_product_frame, text="Название:", anchor="center").pack()
            self.product_name_entry = ttkb.Entry(self.edit_product_frame)
            self.product_name_entry.insert(0, product[1])
            self.product_name_entry.pack()

            ttkb.Label(self.edit_product_frame, text="Цена:", anchor="center").pack()
            self.product_price_entry = ttkb.Entry(self.edit_product_frame)
            self.product_price_entry.insert(0, product[2])
            self.product_price_entry.pack()

            ttkb.Label(self.edit_product_frame, text="Количество:", anchor="center").pack()
            self.product_quantity_entry = ttkb.Entry(self.edit_product_frame)
            self.product_quantity_entry.insert(0, product[3])
            self.product_quantity_entry.pack()

            ttkb.Label(self.edit_product_frame, text="Тип:", anchor="center").pack()
            self.product_type_entry = ttkb.Entry(self.edit_product_frame)
            self.product_type_entry.insert(0, product[4])
            self.product_type_entry.pack()

            self.save_changes_button = ttkb.Button(self.edit_product_frame, text="Сохранить изменения", command=lambda: self.save_changes(product_id))
            self.save_changes_button.pack(pady=10)

            self.back_button = ttkb.Button(self.edit_product_frame, text="Назад", command=self.manage_products)
            self.back_button.pack(pady=10)
        else:
            messagebox.showerror("Ошибка", "Выберите товар для редактирования")

    def save_changes(self, product_id):
        name = self.product_name_entry.get()
        price = float(self.product_price_entry.get())
        quantity = int(self.product_quantity_entry.get())
        type_id = int(self.product_type_entry.get())

        cursor.execute("UPDATE Products SET Name = ?, Price = ?, Quantity = ?, Type_id = ? WHERE Product_id = ?", (name, price, quantity, type_id, product_id))
        conn.commit()
        messagebox.showinfo("Успех", "Товар изменен успешно")
        self.manage_products()

    def delete_product(self):
        selected_product = self.products_listbox.curselection()
        if selected_product:
            product_id = self.products_listbox.get(selected_product[0])[0]
            cursor.execute("DELETE FROM Products WHERE Product_id = ?", (product_id,))
            conn.commit()
            messagebox.showinfo("Успех", "Товар удален успешно")
            self.manage_products()
        else:
            messagebox.showerror("Ошибка", "Выберите товар для удаления")

    def manage_users(self):
        self.clear_frame()

        self.manage_users_frame = ttkb.Frame(self.root, padding="10")
        self.manage_users_frame.pack(expand=True)

        self.users_listbox = tk.Listbox(self.manage_users_frame)
        self.users_listbox.pack()

        cursor.execute("SELECT * FROM Users WHERE Role_id = 2")
        users = cursor.fetchall()
        for user in users:
            self.users_listbox.insert(tk.END, user)

        self.delete_user_button = ttkb.Button(self.manage_users_frame, text="Удалить пользователя", command=self.delete_user)
        self.delete_user_button.pack(pady=10)

        self.back_button = ttkb.Button(self.manage_users_frame, text="Назад", command=self.create_admin_page)
        self.back_button.pack(pady=10)

    def delete_user(self):
        selected_user = self.users_listbox.curselection()
        if selected_user:
            user_id = self.users_listbox.get(selected_user[0])[0]
            cursor.execute("DELETE FROM Users WHERE User_id = ?", (user_id,))
            conn.commit()
            messagebox.showinfo("Успех", "Пользователь удален успешно")
            self.manage_users()
        else:
            messagebox.showerror("Ошибка", "Выберите пользователя для удаления")

    def view_products(self):
        self.clear_frame()

        self.view_products_frame = ttkb.Frame(self.root, padding="10")
        self.view_products_frame.pack(expand=True)

        self.products_listbox = tk.Listbox(self.view_products_frame)
        self.products_listbox.pack()

        cursor.execute("SELECT * FROM Products")
        products = cursor.fetchall()
        for product in products:
            self.products_listbox.insert(tk.END, product)

        self.buy_product_button = ttkb.Button(self.view_products_frame, text="Купить товар", command=self.buy_product)
        self.buy_product_button.pack(pady=10)

        self.back_button = ttkb.Button(self.view_products_frame, text="Назад", command=self.create_user_page)
        self.back_button.pack(pady=10)

    def buy_product(self):
        selected_product = self.products_listbox.curselection()
        if selected_product:
            product = self.products_listbox.get(selected_product[0])
            self.clear_frame()

            self.buy_product_frame = ttkb.Frame(self.root, padding="10")
            self.buy_product_frame.pack(expand=True)

            ttkb.Label(self.buy_product_frame, text=f"Товар: {product[1]}", anchor="center").pack()
            ttkb.Label(self.buy_product_frame, text=f"Цена: {product[2]}", anchor="center").pack()
            ttkb.Label(self.buy_product_frame, text="Количество:", anchor="center").pack()
            self.product_quantity_entry = ttkb.Entry(self.buy_product_frame)
            self.product_quantity_entry.pack()

            ttkb.Label(self.buy_product_frame, text="Данные карты:", anchor="center").pack()
            self.card_data_entry = ttkb.Entry(self.buy_product_frame)
            self.card_data_entry.pack()

            self.confirm_purchase_button = ttkb.Button(self.buy_product_frame, text="Подтвердить покупку", command=lambda: self.confirm_purchase(product))
            self.confirm_purchase_button.pack(pady=10)

            self.back_button = ttkb.Button(self.buy_product_frame, text="Назад", command=self.view_products)
            self.back_button.pack(pady=10)
        else:
            messagebox.showerror("Ошибка", "Выберите товар для покупки")

    def confirm_purchase(self, product):
        quantity = int(self.product_quantity_entry.get())
        card_data = self.card_data_entry.get()

        if quantity <= product[3]:
            new_quantity = product[3] - quantity
            cursor.execute("UPDATE Products SET Quantity = ? WHERE Product_id = ?", (new_quantity, product[0]))
            conn.commit()

            cursor.execute("INSERT INTO Orders (Order_date, Status, User_id) VALUES (DATE('now'), 'New', ?)", (self.user_id,))
            order_id = cursor.lastrowid

            cursor.execute("INSERT INTO Cart (Product_id, Quantity, Order_id) VALUES (?, ?, ?)", (product[0], quantity, order_id))
            cursor.execute("INSERT INTO Payment (Amount, Payment_date, Order_id) VALUES (?, DATE('now'), ?)", (product[2] * quantity, order_id))
            conn.commit()

            messagebox.showinfo("Успех", "Покупка успешно завершена")
            self.view_products()
        else:
            messagebox.showerror("Ошибка", "Недостаточное количество товара")

    def view_reviews(self):
        self.clear_frame()

        self.view_reviews_frame = ttkb.Frame(self.root, padding="10")
        self.view_reviews_frame.pack(expand=True)

        self.reviews_listbox = tk.Listbox(self.view_reviews_frame)
        self.reviews_listbox.pack()

        cursor.execute("SELECT * FROM Reviews")
        reviews = cursor.fetchall()
        for review in reviews:
            self.reviews_listbox.insert(tk.END, review)

        self.back_button = ttkb.Button(self.view_reviews_frame, text="Назад", command=self.create_admin_page if self.user_role == 1 else self.create_user_page)
        self.back_button.pack(pady=10)

        if self.user_role == 1:
            self.delete_review_button = ttkb.Button(self.view_reviews_frame, text="Удалить отзыв", command=self.delete_review)
            self.delete_review_button.pack(pady=10)

    def delete_review(self):
        selected_review = self.reviews_listbox.curselection()
        if selected_review:
            review_id = self.reviews_listbox.get(selected_review[0])[0]
            cursor.execute("DELETE FROM Reviews WHERE Review_id = ?", (review_id,))
            conn.commit()
            messagebox.showinfo("Успех", "Отзыв удален успешно")
            self.view_reviews()
        else:
            messagebox.showerror("Ошибка", "Выберите отзыв для удаления")

    def leave_review(self):
        self.clear_frame()

        self.leave_review_frame = ttkb.Frame(self.root, padding="10")
        self.leave_review_frame.pack(expand=True)

        ttkb.Label(self.leave_review_frame, text="ID товара:", anchor="center").pack()
        self.product_id_entry = ttkb.Entry(self.leave_review_frame)
        self.product_id_entry.pack()

        ttkb.Label(self.leave_review_frame, text="Отзыв:", anchor="center").pack()
        self.review_entry = ttkb.Entry(self.leave_review_frame)
        self.review_entry.pack()

        self.submit_review_button = ttkb.Button(self.leave_review_frame, text="Оставить отзыв", command=self.submit_review)
        self.submit_review_button.pack(pady=10)

        self.back_button = ttkb.Button(self.leave_review_frame, text="Назад", command=self.create_user_page)
        self.back_button.pack(pady=10)

    def submit_review(self):
        product_id = int(self.product_id_entry.get())
        review = self.review_entry.get()

        cursor.execute("INSERT INTO Reviews (Product_id, User_id, Review) VALUES (?, ?, ?)", (product_id, self.user_id, review))
        conn.commit()
        messagebox.showinfo("Успех", "Отзыв оставлен успешно")
        self.create_user_page()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

root = ttkb.Window(themename="darkly")
app = App(root)
root.mainloop()