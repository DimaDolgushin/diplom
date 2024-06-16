import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
import ttkbootstrap as ttkb
import db

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
        if db.user_exists(username):
            messagebox.showerror("Ошибка", "Имя пользователя уже существует")
        else:
            db.create_user(username, password)
            messagebox.showinfo("Успех", "Регистрация прошла успешно")
            self.create_login_page()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user = db.get_user(username, password)
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
        self.logout_button = ttkb.Button(self.admin_frame, text="Выйти", command=self.create_login_page)
        self.logout_button.pack(pady=10)
        self.manage_products_button = ttkb.Button(self.admin_frame, text="Управление товарами", command=self.create_manage_products_page)
        self.manage_products_button.pack(pady=10)
        self.manage_users_button = ttkb.Button(self.admin_frame, text="Управление пользователями", command=self.create_manage_users_page)
        self.manage_users_button.pack(pady=10)
        self.manage_reviews_button = ttkb.Button(self.admin_frame, text="Управление отзывами", command=self.create_manage_reviews_page)
        self.manage_reviews_button.pack(pady=10)

    def create_user_page(self):
        self.clear_frame()
        self.user_frame = ttkb.Frame(self.root, padding="10")
        self.user_frame.pack(expand=True)
        self.logout_button = ttkb.Button(self.user_frame, text="Выйти", command=self.create_login_page)
        self.logout_button.pack(pady=10)
        self.view_products_button = ttkb.Button(self.user_frame, text="Просмотр товаров", command=self.create_view_products_page)
        self.view_products_button.pack(pady=10)
        self.create_order_button = ttkb.Button(self.user_frame, text="Создать заказ", command=self.create_order)
        self.create_order_button.pack(pady=10)

    def create_manage_products_page(self):
        self.clear_frame()
        self.manage_products_frame = ttkb.Frame(self.root, padding="10")
        self.manage_products_frame.pack(expand=True)
        self.products_listbox = tk.Listbox(self.manage_products_frame)
        self.products_listbox.pack(fill=tk.BOTH, expand=True)
        self.load_products()
        self.add_product_button = ttkb.Button(self.manage_products_frame, text="Добавить товар", command=self.add_product)
        self.add_product_button.pack(pady=10)
        self.edit_product_button = ttkb.Button(self.manage_products_frame, text="Редактировать товар", command=self.edit_product)
        self.edit_product_button.pack(pady=10)
        self.delete_product_button = ttkb.Button(self.manage_products_frame, text="Удалить товар", command=self.delete_product)
        self.delete_product_button.pack(pady=10)
        self.back_button = ttkb.Button(self.manage_products_frame, text="Назад", command=self.create_admin_page)
        self.back_button.pack(pady=10)

    def create_manage_users_page(self):
        self.clear_frame()
        self.manage_users_frame = ttkb.Frame(self.root, padding="10")
        self.manage_users_frame.pack(expand=True)
        self.users_listbox = tk.Listbox(self.manage_users_frame)
        self.users_listbox.pack(fill=tk.BOTH, expand=True)
        self.load_users()
        self.delete_user_button = ttkb.Button(self.manage_users_frame, text="Удалить пользователя", command=self.delete_user)
        self.delete_user_button.pack(pady=10)
        self.back_button = ttkb.Button(self.manage_users_frame, text="Назад", command=self.create_admin_page)
        self.back_button.pack(pady=10)

    def create_manage_reviews_page(self):
        self.clear_frame()
        self.manage_reviews_frame = ttkb.Frame(self.root, padding="10")
        self.manage_reviews_frame.pack(expand=True)
        self.reviews_listbox = tk.Listbox(self.manage_reviews_frame)
        self.reviews_listbox.pack(fill=tk.BOTH, expand=True)
        self.load_reviews()
        self.delete_review_button = ttkb.Button(self.manage_reviews_frame, text="Удалить отзыв", command=self.delete_review)
        self.delete_review_button.pack(pady=10)
        self.back_button = ttkb.Button(self.manage_reviews_frame, text="Назад", command=self.create_admin_page)
        self.back_button.pack(pady=10)

    def create_view_products_page(self):
        self.clear_frame()
        self.view_products_frame = ttkb.Frame(self.root, padding="10")
        self.view_products_frame.pack(expand=True)
        self.products_listbox = tk.Listbox(self.view_products_frame)
        self.products_listbox.pack(fill=tk.BOTH, expand=True)
        self.load_products()
        self.order_product_button = ttkb.Button(self.view_products_frame, text="Заказать", command=self.order_product)
        self.order_product_button.pack(pady=10)
        self.add_review_button = ttkb.Button(self.view_products_frame, text="Оставить отзыв", command=self.add_review)
        self.add_review_button.pack(pady=10)
        self.back_button = ttkb.Button(self.view_products_frame, text="Назад", command=self.create_user_page)
        self.back_button.pack(pady=10)

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def load_products(self):
        self.products_listbox.delete(0, tk.END)
        products = db.get_products()
        for product in products:
            self.products_listbox.insert(tk.END, f"{product[0]}. {product[1]} - {product[2]} - {product[3]} шт.")

    def load_users(self):
        self.users_listbox.delete(0, tk.END)
        users = db.get_users()
        for user in users:
            self.users_listbox.insert(tk.END, f"{user[0]}. {user[1]}")

    def load_reviews(self):
        self.reviews_listbox.delete(0, tk.END)
        reviews = db.get_reviews()
        for review in reviews:
            self.reviews_listbox.insert(tk.END, f"{review[0]}. Product ID: {review[1]}, User ID: {review[2]} - {review[3]}")

    def add_product(self):
        name = tk.simpledialog.askstring("Название товара", "Введите название товара")
        price = tk.simpledialog.askfloat("Цена товара", "Введите цену товара")
        quantity = tk.simpledialog.askinteger("Количество товара", "Введите количество товара")
        type_id = tk.simpledialog.askinteger("Тип товара", "Введите ID типа товара")
        if name and price and quantity and type_id:
            db.add_product(name, price, quantity, type_id)
            self.load_products()

    def edit_product(self):
        selected_product = self.products_listbox.get(tk.ACTIVE)
        product_id = int(selected_product.split('.')[0])
        name = tk.simpledialog.askstring("Название товара", "Введите новое название товара")
        price = tk.simpledialog.askfloat("Цена товара", "Введите новую цену товара")
        quantity = tk.simpledialog.askinteger("Количество товара", "Введите новое количество товара")
        type_id = tk.simpledialog.askinteger("Тип товара", "Введите новый ID типа товара")
        if name and price and quantity and type_id:
            db.update_product(product_id, name, price, quantity, type_id)
            self.load_products()

    def delete_product(self):
        selected_product = self.products_listbox.get(tk.ACTIVE)
        product_id = int(selected_product.split('.')[0])
        db.delete_product(product_id)
        self.load_products()

    def delete_user(self):
        selected_user = self.users_listbox.get(tk.ACTIVE)
        user_id = int(selected_user.split('.')[0])
        db.delete_user(user_id)
        self.load_users()

    def delete_review(self):
        selected_review = self.reviews_listbox.get(tk.ACTIVE)
        review_id = int(selected_review.split('.')[0])
        db.delete_review(review_id)
        self.load_reviews()

    def create_order(self):
        order_id = db.create_order(self.user_id)
        messagebox.showinfo("Успех", f"Заказ создан. ID заказа: {order_id}")

    def order_product(self):
        selected_product = self.products_listbox.get(tk.ACTIVE)
        product_id = int(selected_product.split('.')[0])
        quantity = tk.simpledialog.askinteger("Количество", "Введите количество")
        if quantity:
            order_id = db.create_order(self.user_id)
            db.add_to_cart(product_id, quantity, order_id)
            messagebox.showinfo("Успех", "Товар добавлен в корзину")

    def add_review(self):
        selected_product = self.products_listbox.get(tk.ACTIVE)
        product_id = int(selected_product.split('.')[0])
        review = tk.simpledialog.askstring("Отзыв", "Введите ваш отзыв")
        if review:
            db.add_review(product_id, self.user_id, review)
            messagebox.showinfo("Успех", "Отзыв добавлен")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()