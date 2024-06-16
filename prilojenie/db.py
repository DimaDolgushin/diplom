import sqlite3

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

def get_user(username, password):
    cursor.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?", (username, password))
    return cursor.fetchone()

def create_user(username, password):
    cursor.execute("INSERT INTO Users (Username, Password, Role_id) VALUES (?, ?, 2)", (username, password))
    conn.commit()

def user_exists(username):
    cursor.execute("SELECT * FROM Users WHERE Username = ?", (username,))
    return cursor.fetchone()

def get_products():
    cursor.execute("SELECT * FROM Products")
    return cursor.fetchall()

def add_product(name, price, quantity, type_id):
    cursor.execute("INSERT INTO Products (Name, Price, Quantity, Type_id) VALUES (?, ?, ?, ?)", (name, price, quantity, type_id))
    conn.commit()

def get_product(product_id):
    cursor.execute("SELECT * FROM Products WHERE Product_id = ?", (product_id,))
    return cursor.fetchone()

def update_product(product_id, name, price, quantity, type_id):
    cursor.execute("UPDATE Products SET Name = ?, Price = ?, Quantity = ?, Type_id = ? WHERE Product_id = ?", (name, price, quantity, type_id, product_id))
    conn.commit()

def delete_product(product_id):
    cursor.execute("DELETE FROM Products WHERE Product_id = ?", (product_id,))
    conn.commit()

def get_users():
    cursor.execute("SELECT * FROM Users WHERE Role_id = 2")
    return cursor.fetchall()

def delete_user(user_id):
    cursor.execute("DELETE FROM Users WHERE User_id = ?", (user_id,))
    conn.commit()

def create_order(user_id):
    cursor.execute("INSERT INTO Orders (Order_date, Status, User_id) VALUES (DATE('now'), 'New', ?)", (user_id,))
    conn.commit()
    return cursor.lastrowid

def add_to_cart(product_id, quantity, order_id):
    cursor.execute("INSERT INTO Cart (Product_id, Quantity, Order_id) VALUES (?, ?, ?)", (product_id, quantity, order_id))
    conn.commit()

def create_payment(amount, order_id):
    cursor.execute("INSERT INTO Payment (Amount, Payment_date, Order_id) VALUES (?, DATE('now'), ?)", (amount, order_id))
    conn.commit()

def get_reviews():
    cursor.execute("SELECT * FROM Reviews")
    return cursor.fetchall()

def delete_review(review_id):
    cursor.execute("DELETE FROM Reviews WHERE Review_id = ?", (review_id,))
    conn.commit()

def add_review(product_id, user_id, review):
    cursor.execute("INSERT INTO Reviews (Product_id, User_id, Review) VALUES (?, ?, ?)", (product_id, user_id, review))
    conn.commit()
