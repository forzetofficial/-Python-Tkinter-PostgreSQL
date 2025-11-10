from tkinter import *
from tkinter import ttk, messagebox
from auth import AuthManager
from datetime import datetime, timedelta
import tkinter as tk


class RegisterWindow:
    def __init__(self, parent, auth_manager):
        self.parent = parent
        self.auth = auth_manager
        self.create_window()

    def create_window(self):
        self.window = Toplevel(self.parent)
        self.window.title("Регистрация")
        self.window.geometry("500x300")
        self.window.resizable(False, False)
        self.window.grab_set()

        self.window.transient(self.parent)
        self.create_widgets()

    def create_widgets(self):
        main_frame = Frame(self.window)
        main_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        title_label = Label(main_frame, text = "Регистрация", font = ("Arial", 18, "bold"))
        title_label.pack(pady = (0, 20))

        input_frame = Frame(main_frame)
        input_frame.pack(pady = 10)

        login_label = Label(input_frame, text = "Логин:", font = ("Arial", 12))
        login_label.grid(row = 0, column = 0, padx = (0, 10), pady = 10, sticky = "e")

        self.login_entry = Entry(input_frame, font = ("Arial", 12), width = 20)
        self.login_entry.grid(row = 0, column = 1, pady = 10)

        password_label = Label(input_frame, text = "Пароль:", font = ("Arial", 12))
        password_label.grid(row = 1, column = 0, padx = (0, 10), pady = 10, sticky = "e")

        self.password_entry = Entry(input_frame, font = ("Arial", 12), width = 20, show = "*")
        self.password_entry.grid(row = 1, column = 1, pady = 10)

        confirm_label = Label(input_frame, text = "Подтвердите пароль:", font = ("Arial", 12))
        confirm_label.grid(row = 2, column = 0, padx = (0, 10), pady = 10, sticky = "e")

        self.confirm_entry = Entry(input_frame, font = ("Arial", 12), width = 20, show = "*")
        self.confirm_entry.grid(row = 2, column = 1, pady = 10)

        button_frame = Frame(main_frame)
        button_frame.pack(pady = 20)

        self.register_button = Button(button_frame, text = "Зарегистрироваться",
                                      font = ("Arial", 12), width = 20,
                                      command = self.handle_register)
        self.register_button.pack(pady = 5)

        self.cancel_button = Button(button_frame, text = "Отмена",
                                    font = ("Arial", 12), width = 20,
                                    command = self.window.destroy)
        self.cancel_button.pack(pady = 5)

        self.status_label = Label(main_frame, text = "", font = ("Arial", 10), fg = "red")
        self.status_label.pack(pady = 10)

        self.window.bind('<Return>', lambda event: self.handle_register())

    def handle_register(self):
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()
        confirm_password = self.confirm_entry.get().strip()

        self.status_label.config(text = "")

        if not login or not password:
            self.status_label.config(text = "Заполните все поля")
            return

        if len(login) < 3:
            self.status_label.config(text = "Логин должен быть не менее 3 символов")
            return

        if len(password) < 4:
            self.status_label.config(text = "Пароль должен быть не менее 4 символов")
            return

        if password != confirm_password:
            self.status_label.config(text = "Пароли не совпадают")
            return

        success, message = self.auth.register_user(login, password)

        if success:
            messagebox.showinfo("Успех", message)
            self.window.destroy()
        else:
            self.status_label.config(text = message)


class AdminMainWindow:
    def __init__(self, root, user_id, login):
        self.root = root
        self.user_id = user_id
        self.login = login
        self.auth = AuthManager()
        self.create_widgets()

    def create_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title(f"Библиотека - Администратор: {self.login}")
        self.root.geometry("1400x900")

        header_frame = Frame(self.root, bg = "gold", height = 80)
        header_frame.pack(fill = X, padx = 10, pady = 10)
        header_frame.pack_propagate(False)

        title_label = Label(header_frame, text = f"Панель администратора: {self.login}",
                            font = ("Arial", 16, "bold"), bg = "gold")
        title_label.pack(side = LEFT, padx = 20, pady = 20)

        logout_button = Button(header_frame, text = "Выйти", font = ("Arial", 12),
                               command = self.logout)
        logout_button.pack(side = RIGHT, padx = 20, pady = 20)

        main_frame = Frame(self.root)
        main_frame.pack(fill = BOTH, expand = True, padx = 10, pady = 10)

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill = BOTH, expand = True)


        self.create_catalog_tab()
        self.create_search_tab()
        self.create_current_books_tab()
        self.create_history_tab()
        self.create_issue_book_tab()
        self.create_return_book_tab()
        self.create_extend_book_tab()
        self.create_active_issues_tab()


        self.create_manage_books_tab()
        self.create_manage_users_tab()
        self.create_statistics_tab()
        self.create_debtors_tab()
        self.create_system_monitoring_tab()


    def create_catalog_tab(self):
        catalog_frame = Frame(self.notebook)
        self.notebook.add(catalog_frame, text = "Каталог книг")

        Label(catalog_frame, text = "Каталог всех книг", font = ("Arial", 14, "bold")).pack(pady = 10)

        filter_frame = Frame(catalog_frame)
        filter_frame.pack(fill = X, padx = 10, pady = 5)

        Label(filter_frame, text = "Сортировка:").pack(side = LEFT, padx = 5)
        self.sort_var = StringVar(value = "title")
        sort_combo = ttk.Combobox(filter_frame, textvariable = self.sort_var,
                                  values = ["title", "author", "genre"], state = "readonly")
        sort_combo.pack(side = LEFT, padx = 5)
        sort_combo.bind('<<ComboboxSelected>>', self.load_books_catalog)

        Button(filter_frame, text = "Обновить", command = self.load_books_catalog).pack(side = RIGHT, padx = 5)

        columns = ("ID", "Название", "Авторы", "Жанры", "Всего", "Доступно", "Описание")
        self.catalog_tree = ttk.Treeview(catalog_frame, columns = columns, show = "headings", height = 20)

        for col in columns:
            self.catalog_tree.heading(col, text = col)
            self.catalog_tree.column(col, width = 100)

        self.catalog_tree.column("Название", width = 200)
        self.catalog_tree.column("Авторы", width = 150)
        self.catalog_tree.column("Жанры", width = 150)
        self.catalog_tree.column("Описание", width = 300)

        scrollbar = ttk.Scrollbar(catalog_frame, orient = VERTICAL, command = self.catalog_tree.yview)
        self.catalog_tree.configure(yscrollcommand = scrollbar.set)

        self.catalog_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        self.load_books_catalog()

    def create_search_tab(self):
        search_frame = Frame(self.notebook)
        self.notebook.add(search_frame, text = "Поиск книг")

        search_top_frame = Frame(search_frame)
        search_top_frame.pack(fill = X, padx = 10, pady = 10)

        Label(search_top_frame, text = "Название:").grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "w")
        self.search_title = Entry(search_top_frame, width = 20)
        self.search_title.grid(row = 0, column = 1, padx = 5, pady = 5)

        Label(search_top_frame, text = "Автор:").grid(row = 0, column = 2, padx = 5, pady = 5, sticky = "w")
        self.search_author = Entry(search_top_frame, width = 20)
        self.search_author.grid(row = 0, column = 3, padx = 5, pady = 5)

        Label(search_top_frame, text = "Жанр:").grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "w")
        self.search_genre = Entry(search_top_frame, width = 20)
        self.search_genre.grid(row = 1, column = 1, padx = 5, pady = 5)

        Button(search_top_frame, text = "Найти", command = self.search_books).grid(row = 1, column = 2, padx = 5,
                                                                                   pady = 5)
        Button(search_top_frame, text = "Очистить", command = self.clear_search).grid(row = 1, column = 3, padx = 5,
                                                                                      pady = 5)

        columns = ("ID", "Название", "Авторы", "Жанры", "Всего", "Доступно", "Описание")
        self.search_tree = ttk.Treeview(search_frame, columns = columns, show = "headings", height = 20)

        for col in columns:
            self.search_tree.heading(col, text = col)
            self.search_tree.column(col, width = 100)

        self.search_tree.column("Название", width = 200)
        self.search_tree.column("Авторы", width = 150)
        self.search_tree.column("Жанры", width = 150)
        self.search_tree.column("Описание", width = 300)

        scrollbar = ttk.Scrollbar(search_frame, orient = VERTICAL, command = self.search_tree.yview)
        self.search_tree.configure(yscrollcommand = scrollbar.set)

        self.search_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

    def create_current_books_tab(self):
        current_frame = Frame(self.notebook)
        self.notebook.add(current_frame, text = "Мои текущие книги")

        Label(current_frame, text = "Книги, которые у меня сейчас", font = ("Arial", 14, "bold")).pack(pady = 10)

        columns = ("ID", "Название", "Авторы", "Дата взятия", "Статус")
        self.current_tree = ttk.Treeview(current_frame, columns = columns, show = "headings", height = 20)

        for col in columns:
            self.current_tree.heading(col, text = col)
            self.current_tree.column(col, width = 120)

        self.current_tree.column("Название", width = 200)
        self.current_tree.column("Авторы", width = 150)

        scrollbar = ttk.Scrollbar(current_frame, orient = VERTICAL, command = self.current_tree.yview)
        self.current_tree.configure(yscrollcommand = scrollbar.set)

        self.current_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        Button(current_frame, text = "Обновить", command = self.load_current_books).pack(pady = 5)

        self.load_current_books()

    def create_history_tab(self):
        history_frame = Frame(self.notebook)
        self.notebook.add(history_frame, text = "История книг")

        Label(history_frame, text = "История всех взятых мной книг", font = ("Arial", 14, "bold")).pack(pady = 10)

        columns = ("ID", "Название", "Авторы", "Дата взятия", "Дата возврата", "Статус")
        self.history_tree = ttk.Treeview(history_frame, columns = columns, show = "headings", height = 20)

        for col in columns:
            self.history_tree.heading(col, text = col)
            self.history_tree.column(col, width = 100)

        self.history_tree.column("Название", width = 200)
        self.history_tree.column("Авторы", width = 150)

        scrollbar = ttk.Scrollbar(history_frame, orient = VERTICAL, command = self.history_tree.yview)
        self.history_tree.configure(yscrollcommand = scrollbar.set)

        self.history_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        Button(history_frame, text = "Обновить", command = self.load_history_books).pack(pady = 5)

        self.load_history_books()

    def create_issue_book_tab(self):
        issue_frame = Frame(self.notebook)
        self.notebook.add(issue_frame, text = "Выдача книг")

        Label(issue_frame, text = "Выдача книги пользователю", font = ("Arial", 14, "bold")).pack(pady = 10)

        form_frame = Frame(issue_frame)
        form_frame.pack(fill = X, padx = 20, pady = 10)

        Label(form_frame, text = "Логин пользователя:", font = ("Arial", 12)).grid(row = 0, column = 0, padx = 5,
                                                                                   pady = 5, sticky = "w")
        self.user_login_entry = Entry(form_frame, font = ("Arial", 12), width = 20)
        self.user_login_entry.grid(row = 0, column = 1, padx = 5, pady = 5)

        Button(form_frame, text = "Найти пользователя", command = self.find_user).grid(row = 0, column = 2, padx = 5,
                                                                                       pady = 5)

        Label(form_frame, text = "ID книги:", font = ("Arial", 12)).grid(row = 1, column = 0, padx = 5, pady = 5,
                                                                         sticky = "w")
        self.book_id_entry = Entry(form_frame, font = ("Arial", 12), width = 20)
        self.book_id_entry.grid(row = 1, column = 1, padx = 5, pady = 5)

        Button(form_frame, text = "Найти книгу", command = self.find_book).grid(row = 1, column = 2, padx = 5, pady = 5)

        info_frame = Frame(issue_frame)
        info_frame.pack(fill = X, padx = 20, pady = 10)

        self.user_info_label = Label(info_frame, text = "Пользователь не найден", font = ("Arial", 10), fg = "red")
        self.user_info_label.pack(anchor = "w")

        self.book_info_label = Label(info_frame, text = "Книга не найдена", font = ("Arial", 10), fg = "red")
        self.book_info_label.pack(anchor = "w")

        Button(issue_frame, text = "Выдать книгу", font = ("Arial", 12),
               command = self.issue_book, bg = "lightgreen").pack(pady = 10)

        self.issue_status_label = Label(issue_frame, text = "", font = ("Arial", 10))
        self.issue_status_label.pack(pady = 5)

    def create_return_book_tab(self):
        return_frame = Frame(self.notebook)
        self.notebook.add(return_frame, text = "Прием книг")

        Label(return_frame, text = "Прием возвращенных книг", font = ("Arial", 14, "bold")).pack(pady = 10)

        search_frame = Frame(return_frame)
        search_frame.pack(fill = X, padx = 20, pady = 10)

        Label(search_frame, text = "ID выдачи:", font = ("Arial", 12)).grid(row = 0, column = 0, padx = 5, pady = 5,
                                                                            sticky = "w")
        self.return_issue_id_entry = Entry(search_frame, font = ("Arial", 12), width = 20)
        self.return_issue_id_entry.grid(row = 0, column = 1, padx = 5, pady = 5)

        Button(search_frame, text = "Найти выдачу", command = self.find_issue_for_return).grid(row = 0, column = 2,
                                                                                               padx = 5, pady = 5)

        self.return_info_frame = Frame(return_frame)
        self.return_info_frame.pack(fill = X, padx = 20, pady = 10)

        self.return_info_label = Label(self.return_info_frame, text = "Введите ID выдачи", font = ("Arial", 10))
        self.return_info_label.pack(anchor = "w")

        Button(return_frame, text = "Принять книгу", font = ("Arial", 12),
               command = self.return_book, bg = "lightcoral").pack(pady = 10)

        self.return_status_label = Label(return_frame, text = "", font = ("Arial", 10))
        self.return_status_label.pack(pady = 5)

    def create_extend_book_tab(self):
        extend_frame = Frame(self.notebook)
        self.notebook.add(extend_frame, text = "Продление книг")

        Label(extend_frame, text = "Продление срока возврата книги", font = ("Arial", 14, "bold")).pack(pady = 10)

        search_frame = Frame(extend_frame)
        search_frame.pack(fill = X, padx = 20, pady = 10)

        Label(search_frame, text = "ID выдачи:", font = ("Arial", 12)).grid(row = 0, column = 0, padx = 5, pady = 5,
                                                                            sticky = "w")
        self.extend_issue_id_entry = Entry(search_frame, font = ("Arial", 12), width = 20)
        self.extend_issue_id_entry.grid(row = 0, column = 1, padx = 5, pady = 5)

        Button(search_frame, text = "Найти выдачу", command = self.find_issue_for_extend).grid(row = 0, column = 2,
                                                                                               padx = 5, pady = 5)

        self.extend_info_frame = Frame(extend_frame)
        self.extend_info_frame.pack(fill = X, padx = 20, pady = 10)

        self.extend_info_label = Label(self.extend_info_frame, text = "Введите ID выдачи", font = ("Arial", 10))
        self.extend_info_label.pack(anchor = "w")

        Button(extend_frame, text = "Продлить на 14 дней", font = ("Arial", 12),
               command = self.extend_book, bg = "lightyellow").pack(pady = 10)

        self.extend_status_label = Label(extend_frame, text = "", font = ("Arial", 10))
        self.extend_status_label.pack(pady = 5)

    def create_active_issues_tab(self):
        active_frame = Frame(self.notebook)
        self.notebook.add(active_frame, text = "Активные выдачи")

        Label(active_frame, text = "Все активные выдачи книг", font = ("Arial", 14, "bold")).pack(pady = 10)

        columns = ("ID выдачи", "Книга", "Пользователь", "Дата выдачи", "Статус")
        self.active_issues_tree = ttk.Treeview(active_frame, columns = columns, show = "headings", height = 20)

        for col in columns:
            self.active_issues_tree.heading(col, text = col)
            self.active_issues_tree.column(col, width = 120)

        self.active_issues_tree.column("Книга", width = 200)
        self.active_issues_tree.column("Пользователь", width = 150)

        scrollbar = ttk.Scrollbar(active_frame, orient = VERTICAL, command = self.active_issues_tree.yview)
        self.active_issues_tree.configure(yscrollcommand = scrollbar.set)

        self.active_issues_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        Button(active_frame, text = "Обновить", command = self.load_active_issues).pack(pady = 5)

        self.load_active_issues()

    def create_manage_books_tab(self):
        """Вкладка управления книгами"""
        manage_frame = Frame(self.notebook)
        self.notebook.add(manage_frame, text = "Управление книгами")

        Label(manage_frame, text = "Управление каталогом книг", font = ("Arial", 14, "bold")).pack(pady = 10)

        # Форма добавления/редактирования книги
        form_frame = Frame(manage_frame)
        form_frame.pack(fill = X, padx = 20, pady = 10)

        Label(form_frame, text = "Название:", font = ("Arial", 12)).grid(row = 0, column = 0, padx = 5, pady = 5,
                                                                         sticky = "w")
        self.book_title_entry = Entry(form_frame, font = ("Arial", 12), width = 30)
        self.book_title_entry.grid(row = 0, column = 1, padx = 5, pady = 5)

        Label(form_frame, text = "Описание:", font = ("Arial", 12)).grid(row = 1, column = 0, padx = 5, pady = 5,
                                                                         sticky = "w")
        self.book_desc_entry = Text(form_frame, font = ("Arial", 12), width = 30, height = 4)
        self.book_desc_entry.grid(row = 1, column = 1, padx = 5, pady = 5)

        Label(form_frame, text = "Всего экземпляров:", font = ("Arial", 12)).grid(row = 2, column = 0, padx = 5,
                                                                                  pady = 5, sticky = "w")
        self.book_copies_entry = Entry(form_frame, font = ("Arial", 12), width = 10)
        self.book_copies_entry.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = "w")

        button_frame = Frame(manage_frame)
        button_frame.pack(pady = 10)

        Button(button_frame, text = "Добавить книгу", command = self.add_book, bg = "lightgreen").pack(side = LEFT,
                                                                                                       padx = 5)
        Button(button_frame, text = "Обновить книгу", command = self.update_book, bg = "lightblue").pack(side = LEFT,
                                                                                                         padx = 5)
        Button(button_frame, text = "Удалить книгу", command = self.delete_book, bg = "lightcoral").pack(side = LEFT,
                                                                                                         padx = 5)

        # Таблица книг для управления
        columns = ("ID", "Название", "Описание", "Всего", "Доступно")
        self.manage_books_tree = ttk.Treeview(manage_frame, columns = columns, show = "headings", height = 15)

        for col in columns:
            self.manage_books_tree.heading(col, text = col)
            self.manage_books_tree.column(col, width = 100)

        self.manage_books_tree.column("Название", width = 200)
        self.manage_books_tree.column("Описание", width = 300)

        scrollbar = ttk.Scrollbar(manage_frame, orient = VERTICAL, command = self.manage_books_tree.yview)
        self.manage_books_tree.configure(yscrollcommand = scrollbar.set)

        self.manage_books_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        self.manage_books_tree.bind('<<TreeviewSelect>>', self.on_book_select)

        self.load_manage_books()

    def create_manage_users_tab(self):
        """Вкладка управления пользователями"""
        users_frame = Frame(self.notebook)
        self.notebook.add(users_frame, text = "Управление пользователями")

        Label(users_frame, text = "Управление пользователями системы", font = ("Arial", 14, "bold")).pack(pady = 10)

        # Форма управления пользователями
        form_frame = Frame(users_frame)
        form_frame.pack(fill = X, padx = 20, pady = 10)

        Label(form_frame, text = "Роль:", font = ("Arial", 12)).grid(row = 0, column = 0, padx = 5, pady = 5,
                                                                     sticky = "w")
        self.user_role_var = StringVar(value = "user")
        role_combo = ttk.Combobox(form_frame, textvariable = self.user_role_var,
                                  values = ["user", "worker", "admin"], state = "readonly")
        role_combo.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = "w")

        button_frame = Frame(users_frame)
        button_frame.pack(pady = 10)

        Button(button_frame, text = "Изменить роль", command = self.change_user_role, bg = "lightblue").pack(
            side = LEFT, padx = 5)
        Button(button_frame, text = "Удалить пользователя", command = self.delete_user, bg = "lightcoral").pack(
            side = LEFT, padx = 5)

        # Таблица пользователей
        columns = ("ID", "Логин", "Роль", "Дата регистрации")
        self.users_tree = ttk.Treeview(users_frame, columns = columns, show = "headings", height = 15)

        for col in columns:
            self.users_tree.heading(col, text = col)
            self.users_tree.column(col, width = 120)

        self.users_tree.column("Логин", width = 150)

        scrollbar = ttk.Scrollbar(users_frame, orient = VERTICAL, command = self.users_tree.yview)
        self.users_tree.configure(yscrollcommand = scrollbar.set)

        self.users_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        self.users_tree.bind('<<TreeviewSelect>>', self.on_user_select)

        self.load_users()

    def create_statistics_tab(self):
        """Вкладка статистики"""
        stats_frame = Frame(self.notebook)
        self.notebook.add(stats_frame, text = "Статистика")

        Label(stats_frame, text = "Статистика библиотеки", font = ("Arial", 14, "bold")).pack(pady = 10)

        # Период для статистики
        period_frame = Frame(stats_frame)
        period_frame.pack(fill = X, padx = 20, pady = 10)

        Label(period_frame, text = "С:", font = ("Arial", 12)).grid(row = 0, column = 0, padx = 5, pady = 5)
        self.start_date_entry = Entry(period_frame, font = ("Arial", 12), width = 12)
        self.start_date_entry.grid(row = 0, column = 1, padx = 5, pady = 5)
        self.start_date_entry.insert(0, (datetime.now() - timedelta(days = 30)).strftime("%Y-%m-%d"))

        Label(period_frame, text = "По:", font = ("Arial", 12)).grid(row = 0, column = 2, padx = 5, pady = 5)
        self.end_date_entry = Entry(period_frame, font = ("Arial", 12), width = 12)
        self.end_date_entry.grid(row = 0, column = 3, padx = 5, pady = 5)
        self.end_date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))

        Button(period_frame, text = "Обновить статистику", command = self.load_statistics).grid(row = 0, column = 4,
                                                                                                padx = 5, pady = 5)

        # Общая статистика
        stats_info_frame = Frame(stats_frame)
        stats_info_frame.pack(fill = X, padx = 20, pady = 10)

        self.stats_label = Label(stats_info_frame, text = "", font = ("Arial", 11), justify = LEFT)
        self.stats_label.pack(anchor = "w")

        # Таблица статистики по книгам
        columns = ("Книга", "Количество выдач")
        self.stats_tree = ttk.Treeview(stats_frame, columns = columns, show = "headings", height = 15)

        for col in columns:
            self.stats_tree.heading(col, text = col)
            self.stats_tree.column(col, width = 200)

        scrollbar = ttk.Scrollbar(stats_frame, orient = VERTICAL, command = self.stats_tree.yview)
        self.stats_tree.configure(yscrollcommand = scrollbar.set)

        self.stats_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        self.load_statistics()

    def create_debtors_tab(self):
        """Вкладка задолжников"""
        debtors_frame = Frame(self.notebook)
        self.notebook.add(debtors_frame, text = "Задолжники")

        Label(debtors_frame, text = "Список задолжников", font = ("Arial", 14, "bold")).pack(pady = 10)

        columns = ("Пользователь", "Книга", "Дата выдачи", "Дней просрочки")
        self.debtors_tree = ttk.Treeview(debtors_frame, columns = columns, show = "headings", height = 20)

        for col in columns:
            self.debtors_tree.heading(col, text = col)
            self.debtors_tree.column(col, width = 150)

        scrollbar = ttk.Scrollbar(debtors_frame, orient = VERTICAL, command = self.debtors_tree.yview)
        self.debtors_tree.configure(yscrollcommand = scrollbar.set)

        self.debtors_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        Button(debtors_frame, text = "Обновить список", command = self.load_debtors).pack(pady = 5)

        self.load_debtors()

    def create_system_monitoring_tab(self):
        """Вкладка мониторинга системы"""
        monitor_frame = Frame(self.notebook)
        self.notebook.add(monitor_frame, text = "Мониторинг")

        Label(monitor_frame, text = "Мониторинг активности системы", font = ("Arial", 14, "bold")).pack(pady = 10)

        # Создаем вложенные вкладки для разных отчетов
        monitor_notebook = ttk.Notebook(monitor_frame)
        monitor_notebook.pack(fill = BOTH, expand = True, padx = 10, pady = 10)

        # Отчет по месяцам
        monthly_frame = Frame(monitor_notebook)
        monitor_notebook.add(monthly_frame, text = "По месяцам")

        columns = ("Месяц", "Количество выдач")
        self.monthly_tree = ttk.Treeview(monthly_frame, columns = columns, show = "headings", height = 15)

        for col in columns:
            self.monthly_tree.heading(col, text = col)
            self.monthly_tree.column(col, width = 200)

        scrollbar = ttk.Scrollbar(monthly_frame, orient = VERTICAL, command = self.monthly_tree.yview)
        self.monthly_tree.configure(yscrollcommand = scrollbar.set)

        self.monthly_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        # Популярные книги
        popular_frame = Frame(monitor_notebook)
        monitor_notebook.add(popular_frame, text = "Популярные книги")

        columns = ("Книга", "Количество выдач")
        self.popular_tree = ttk.Treeview(popular_frame, columns = columns, show = "headings", height = 15)

        for col in columns:
            self.popular_tree.heading(col, text = col)
            self.popular_tree.column(col, width = 250)

        scrollbar = ttk.Scrollbar(popular_frame, orient = VERTICAL, command = self.popular_tree.yview)
        self.popular_tree.configure(yscrollcommand = scrollbar.set)

        self.popular_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        # Активные читатели
        readers_frame = Frame(monitor_notebook)
        monitor_notebook.add(readers_frame, text = "Активные читатели")

        columns = ("Читатель", "Количество книг")
        self.readers_tree = ttk.Treeview(readers_frame, columns = columns, show = "headings", height = 15)

        for col in columns:
            self.readers_tree.heading(col, text = col)
            self.readers_tree.column(col, width = 200)

        scrollbar = ttk.Scrollbar(readers_frame, orient = VERTICAL, command = self.readers_tree.yview)
        self.readers_tree.configure(yscrollcommand = scrollbar.set)

        self.readers_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        Button(monitor_frame, text = "Обновить отчеты", command = self.load_monitoring_reports).pack(pady = 5)

        self.load_monitoring_reports()

    # Методы администратора
    def add_book(self):
        title = self.book_title_entry.get().strip()
        description = self.book_desc_entry.get("1.0", END).strip()
        copies = self.book_copies_entry.get().strip()

        if not title or not copies:
            messagebox.showwarning("Ошибка", "Заполните название и количество экземпляров")
            return

        try:
            copies = int(copies)
            query = "INSERT INTO books (title, description, all_copies, last_copies) VALUES (%s, %s, %s, %s)"
            self.auth.db.cursor.execute(query, (title, description, copies, copies))
            self.auth.db.connection.commit()

            messagebox.showinfo("Успех", "Книга успешно добавлена")
            self.clear_book_form()
            self.load_manage_books()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка добавления книги: {e}")

    def update_book(self):
        selection = self.manage_books_tree.selection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите книгу для редактирования")
            return

        book_id = self.manage_books_tree.item(selection[0])['values'][0]
        title = self.book_title_entry.get().strip()
        description = self.book_desc_entry.get("1.0", END).strip()
        copies = self.book_copies_entry.get().strip()

        if not title or not copies:
            messagebox.showwarning("Ошибка", "Заполните название и количество экземпляров")
            return

        try:
            copies = int(copies)
            # Получаем текущее количество доступных книг
            query = "SELECT last_copies FROM books WHERE id = %s"
            self.auth.db.cursor.execute(query, (book_id,))
            current_last = self.auth.db.cursor.fetchone()[0]

            # Вычисляем разницу для обновления last_copies
            diff = copies - (self.manage_books_tree.item(selection[0])['values'][3])  # all_copies из таблицы
            new_last = current_last + diff

            query = "UPDATE books SET title = %s, description = %s, all_copies = %s, last_copies = %s WHERE id = %s"
            self.auth.db.cursor.execute(query, (title, description, copies, new_last, book_id))
            self.auth.db.connection.commit()

            messagebox.showinfo("Успех", "Книга успешно обновлена")
            self.clear_book_form()
            self.load_manage_books()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка обновления книги: {e}")

    def delete_book(self):
        selection = self.manage_books_tree.selection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите книгу для удаления")
            return

        book_id = self.manage_books_tree.item(selection[0])['values'][0]
        book_title = self.manage_books_tree.item(selection[0])['values'][1]

        if messagebox.askyesno("Подтверждение", f"Удалить книгу '{book_title}'?"):
            try:
                query = "DELETE FROM books WHERE id = %s"
                self.auth.db.cursor.execute(query, (book_id,))
                self.auth.db.connection.commit()

                messagebox.showinfo("Успех", "Книга успешно удалена")
                self.clear_book_form()
                self.load_manage_books()

            except Exception as e:
                messagebox.showerror("Ошибка", f"Ошибка удаления книги: {e}")

    def change_user_role(self):
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите пользователя")
            return

        user_id = self.users_tree.item(selection[0])['values'][0]
        username = self.users_tree.item(selection[0])['values'][1]
        new_role = self.user_role_var.get()

        role_id_map = {"user": 1, "worker": 2, "admin": 3}
        new_role_id = role_id_map[new_role]

        try:
            query = "UPDATE users SET role_id = %s WHERE id = %s"
            self.auth.db.cursor.execute(query, (new_role_id, user_id))
            self.auth.db.connection.commit()

            messagebox.showinfo("Успех", f"Роль пользователя {username} изменена на {new_role}")
            self.load_users()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка изменения роли: {e}")

    def delete_user(self):
        selection = self.users_tree.selection()
        if not selection:
            messagebox.showwarning("Ошибка", "Выберите пользователя")
            return

        user_id = self.users_tree.item(selection[0])['values'][0]
        username = self.users_tree.item(selection[0])['values'][1]

        if user_id == self.user_id:
            messagebox.showerror("Ошибка", "Нельзя удалить самого себя")
            return

        if messagebox.askyesno("Подтверждение", f"Удалить пользователя '{username}'?"):
            try:
                # Проверяем, есть ли у пользователя НЕвозвращенные книги
                check_books_query = """
                    SELECT COUNT(*) FROM book_dist 
                    WHERE user_id = %s AND status != 'return'
                """
                self.auth.db.cursor.execute(check_books_query, (user_id,))
                active_books_count = self.auth.db.cursor.fetchone()[0]

                if active_books_count > 0:
                    messagebox.showerror(
                        "Ошибка",
                        f"Нельзя удалить пользователя: у него {active_books_count} не возвращенных книг"
                    )
                    return

                # Удаляем только возвращенные книги из book_dist
                delete_book_dist_query = "DELETE FROM book_dist WHERE user_id = %s AND status = 'return'"
                self.auth.db.cursor.execute(delete_book_dist_query, (user_id,))

                # Удаляем пользователя
                delete_user_query = "DELETE FROM users WHERE id = %s"
                self.auth.db.cursor.execute(delete_user_query, (user_id,))

                self.auth.db.connection.commit()

                messagebox.showinfo("Успех", "Пользователь успешно удален")
                self.load_users()

            except Exception as e:
                self.auth.db.connection.rollback()
                messagebox.showerror("Ошибка", f"Ошибка удаления пользователя: {e}")

    def load_manage_books(self):
        try:
            for item in self.manage_books_tree.get_children():
                self.manage_books_tree.delete(item)

            query = "SELECT id, title, description, all_copies, last_copies FROM books ORDER BY title"
            self.auth.db.cursor.execute(query)
            books = self.auth.db.cursor.fetchall()

            for book in books:
                self.manage_books_tree.insert("", "end", values = book)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить книги: {e}")

    def load_users(self):
        try:
            for item in self.users_tree.get_children():
                self.users_tree.delete(item)

            query = """
            SELECT u.id, u.login, r.name
            FROM users u
            JOIN roles r ON u.role_id = r.id
            ORDER BY u.login
            """
            self.auth.db.cursor.execute(query)
            users = self.auth.db.cursor.fetchall()

            for user in users:
                self.users_tree.insert("", "end", values = user)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить пользователей: {e}")

    def load_statistics(self):
        try:
            start_date = self.start_date_entry.get().strip()
            end_date = self.end_date_entry.get().strip()

            # Общая статистика
            query = """
            SELECT 
                COUNT(*) as total_books,
                SUM(all_copies) as total_copies,
                SUM(last_copies) as available_copies,
                (SELECT COUNT(*) FROM users) as total_users,
                (SELECT COUNT(*) FROM book_dist WHERE vz_date BETWEEN %s AND %s) as total_issues
            FROM books
            """
            self.auth.db.cursor.execute(query, (start_date, end_date))
            stats = self.auth.db.cursor.fetchone()

            stats_text = f"""
            Общая статистика за период с {start_date} по {end_date}:
            • Всего книг в каталоге: {stats[0]}
            • Всего экземпляров: {stats[1]}
            • Доступно экземпляров: {stats[2]}
            • Всего пользователей: {stats[3]}
            • Выдач за период: {stats[4]}
            """
            self.stats_label.config(text = stats_text)

            # Статистика по популярности книг
            for item in self.stats_tree.get_children():
                self.stats_tree.delete(item)

            query = """
            SELECT b.title, COUNT(bd.id) as issue_count
            FROM book_dist bd
            JOIN books b ON bd.book_id = b.id
            WHERE bd.vz_date BETWEEN %s AND %s
            GROUP BY b.id, b.title
            ORDER BY issue_count DESC
            LIMIT 20
            """
            self.auth.db.cursor.execute(query, (start_date, end_date))
            popular_books = self.auth.db.cursor.fetchall()

            for book in popular_books:
                self.stats_tree.insert("", "end", values = book)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить статистику: {e}")

    def load_debtors(self):
        try:
            for item in self.debtors_tree.get_children():
                self.debtors_tree.delete(item)

            query = """
            SELECT u.login, b.title, bd.vz_date, 
                   (CURRENT_DATE - bd.vz_date) as days_overdue
            FROM book_dist bd
            JOIN books b ON bd.book_id = b.id
            JOIN users u ON bd.user_id = u.id
            WHERE bd.status = 'active' 
            AND (CURRENT_DATE - bd.vz_date) > 30
            ORDER BY days_overdue DESC
            """
            self.auth.db.cursor.execute(query)
            debtors = self.auth.db.cursor.fetchall()

            for debtor in debtors:
                self.debtors_tree.insert("", "end", values = debtor)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить список задолжников: {e}")

    def load_monitoring_reports(self):
        try:
            # Статистика по месяцам
            for item in self.monthly_tree.get_children():
                self.monthly_tree.delete(item)

            query = """
            SELECT TO_CHAR(vz_date, 'YYYY-MM') as month, COUNT(*) as issue_count
            FROM book_dist
            GROUP BY TO_CHAR(vz_date, 'YYYY-MM')
            ORDER BY month DESC
            LIMIT 12
            """
            self.auth.db.cursor.execute(query)
            monthly_stats = self.auth.db.cursor.fetchall()

            for stat in monthly_stats:
                self.monthly_tree.insert("", "end", values = stat)

            # Популярные книги
            for item in self.popular_tree.get_children():
                self.popular_tree.delete(item)

            query = """
            SELECT b.title, COUNT(bd.id) as issue_count
            FROM book_dist bd
            JOIN books b ON bd.book_id = b.id
            GROUP BY b.id, b.title
            ORDER BY issue_count DESC
            LIMIT 20
            """
            self.auth.db.cursor.execute(query)
            popular_books = self.auth.db.cursor.fetchall()

            for book in popular_books:
                self.popular_tree.insert("", "end", values = book)

            # Активные читатели
            for item in self.readers_tree.get_children():
                self.readers_tree.delete(item)

            query = """
            SELECT u.login, COUNT(bd.id) as book_count
            FROM book_dist bd
            JOIN users u ON bd.user_id = u.id
            WHERE bd.vz_date >= CURRENT_DATE - INTERVAL '30 days'
            GROUP BY u.id, u.login
            ORDER BY book_count DESC
            LIMIT 20
            """
            self.auth.db.cursor.execute(query)
            active_readers = self.auth.db.cursor.fetchall()

            for reader in active_readers:
                self.readers_tree.insert("", "end", values = reader)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить отчеты: {e}")

    def on_book_select(self, event):
        selection = self.manage_books_tree.selection()
        if selection:
            book_data = self.manage_books_tree.item(selection[0])['values']
            self.book_title_entry.delete(0, END)
            self.book_title_entry.insert(0, book_data[1])
            self.book_desc_entry.delete("1.0", END)
            self.book_desc_entry.insert("1.0", book_data[2] if book_data[2] else "")
            self.book_copies_entry.delete(0, END)
            self.book_copies_entry.insert(0, str(book_data[3]))

    def on_user_select(self, event):
        selection = self.users_tree.selection()
        if selection:
            user_data = self.users_tree.item(selection[0])['values']
            current_role = user_data[2]
            role_map = {"user": "user", "worker": "worker", "admin": "admin"}
            self.user_role_var.set(role_map.get(current_role, "user"))

    def clear_book_form(self):
        self.book_title_entry.delete(0, END)
        self.book_desc_entry.delete("1.0", END)
        self.book_copies_entry.delete(0, END)

    # Остальные методы работника (копируются из WorkerMainWindow)
    def find_user(self):
        login = self.user_login_entry.get().strip()
        if not login:
            messagebox.showwarning("Ошибка", "Введите логин пользователя")
            return

        try:
            query = "SELECT id, login FROM users WHERE login = %s"
            self.auth.db.cursor.execute(query, (login,))
            user = self.auth.db.cursor.fetchone()

            if user:
                self.found_user_id = user[0]
                self.user_info_label.config(text = f"Найден пользователь: {user[1]} (ID: {user[0]})", fg = "green")
            else:
                self.found_user_id = None
                self.user_info_label.config(text = "Пользователь не найден", fg = "red")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска пользователя: {e}")

    def find_book(self):
        book_id = self.book_id_entry.get().strip()
        if not book_id:
            messagebox.showwarning("Ошибка", "Введите ID книги")
            return

        try:
            query = "SELECT id, title, last_copies FROM books WHERE id = %s"
            self.auth.db.cursor.execute(query, (book_id,))
            book = self.auth.db.cursor.fetchone()

            if book:
                self.found_book_id = book[0]
                available = "Доступна" if book[2] > 0 else "Нет в наличии"
                self.book_info_label.config(text = f"Найдена книга: '{book[1]}' (ID: {book[0]}), {available}",
                                            fg = "green" if book[2] > 0 else "red")
            else:
                self.found_book_id = None
                self.book_info_label.config(text = "Книга не найдена", fg = "red")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска книги: {e}")

    def issue_book(self):
        if not hasattr(self, 'found_user_id') or not self.found_user_id:
            messagebox.showwarning("Ошибка", "Сначала найдите пользователя")
            return

        if not hasattr(self, 'found_book_id') or not self.found_book_id:
            messagebox.showwarning("Ошибка", "Сначала найдите книгу")
            return

        try:
            query = "SELECT last_copies FROM books WHERE id = %s"
            self.auth.db.cursor.execute(query, (self.found_book_id,))
            book = self.auth.db.cursor.fetchone()

            if not book or book[0] <= 0:
                messagebox.showerror("Ошибка", "Книга недоступна для выдачи")
                return

            issue_date = datetime.now().date()
            query = """
            INSERT INTO book_dist (book_id, user_id, libuser_id, vz_date, status) 
            VALUES (%s, %s, %s, %s, 'active')
            """
            self.auth.db.cursor.execute(query, (self.found_book_id, self.found_user_id, self.user_id, issue_date))

            query = "UPDATE books SET last_copies = last_copies - 1 WHERE id = %s"
            self.auth.db.cursor.execute(query, (self.found_book_id,))

            self.auth.db.connection.commit()

            self.issue_status_label.config(text = "Книга успешно выдана!", fg = "green")
            self.user_login_entry.delete(0, END)
            self.book_id_entry.delete(0, END)
            self.user_info_label.config(text = "Пользователь не найден", fg = "red")
            self.book_info_label.config(text = "Книга не найдена", fg = "red")

        except Exception as e:
            self.auth.db.connection.rollback()
            messagebox.showerror("Ошибка", f"Ошибка выдачи книги: {e}")

    def find_issue_for_return(self):
        issue_id = self.return_issue_id_entry.get().strip()
        if not issue_id:
            messagebox.showwarning("Ошибка", "Введите ID выдачи")
            return

        try:
            query = """
            SELECT bd.id, b.title, u.login, bd.vz_date, bd.status 
            FROM book_dist bd
            JOIN books b ON bd.book_id = b.id
            JOIN users u ON bd.user_id = u.id
            WHERE bd.id = %s AND bd.status = 'active'
            """
            self.auth.db.cursor.execute(query, (issue_id,))
            issue = self.auth.db.cursor.fetchone()

            if issue:
                self.return_issue_id = issue[0]
                info_text = f"Книга: '{issue[1]}', Пользователь: {issue[2]}, Дата выдачи: {issue[3]}"
                self.return_info_label.config(text = info_text, fg = "green")
            else:
                self.return_issue_id = None
                self.return_info_label.config(text = "Активная выдача не найдена", fg = "red")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска выдачи: {e}")

    def return_book(self):
        if not hasattr(self, 'return_issue_id') or not self.return_issue_id:
            messagebox.showwarning("Ошибка", "Сначала найдите активную выдачу")
            return

        try:
            return_date = datetime.now().date()

            query = "SELECT book_id FROM book_dist WHERE id = %s"
            self.auth.db.cursor.execute(query, (self.return_issue_id,))
            result = self.auth.db.cursor.fetchone()
            book_id = result[0]

            query = "UPDATE book_dist SET status = 'return', ot_date = %s WHERE id = %s"
            self.auth.db.cursor.execute(query, (return_date, self.return_issue_id))

            query = "UPDATE books SET last_copies = last_copies + 1 WHERE id = %s"
            self.auth.db.cursor.execute(query, (book_id,))

            self.auth.db.connection.commit()

            self.return_status_label.config(text = "Книга успешно принята!", fg = "green")
            self.return_issue_id_entry.delete(0, END)
            self.return_info_label.config(text = "Введите ID выдачи", fg = "black")

        except Exception as e:
            self.auth.db.connection.rollback()
            messagebox.showerror("Ошибка", f"Ошибка приема книги: {e}")

    def find_issue_for_extend(self):
        issue_id = self.extend_issue_id_entry.get().strip()
        if not issue_id:
            messagebox.showwarning("Ошибка", "Введите ID выдачи")
            return

        try:
            query = """
            SELECT bd.id, b.title, u.login, bd.vz_date 
            FROM book_dist bd
            JOIN books b ON bd.book_id = b.id
            JOIN users u ON bd.user_id = u.id
            WHERE bd.id = %s AND bd.status = 'active'
            """
            self.auth.db.cursor.execute(query, (issue_id,))
            issue = self.auth.db.cursor.fetchone()

            if issue:
                self.extend_issue_id = issue[0]
                info_text = f"Книга: '{issue[1]}', Пользователь: {issue[2]}, Дата выдачи: {issue[3]}"
                self.extend_info_label.config(text = info_text, fg = "green")
            else:
                self.extend_issue_id = None
                self.extend_info_label.config(text = "Активная выдача не найдена", fg = "red")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска выдачи: {e}")

    def extend_book(self):
        if not hasattr(self, 'extend_issue_id') or not self.extend_issue_id:
            messagebox.showwarning("Ошибка", "Сначала найдите активную выдачу")
            return

        try:
            query = "UPDATE book_dist SET status = 'active' WHERE id = %s"
            self.auth.db.cursor.execute(query, (self.extend_issue_id,))
            self.auth.db.connection.commit()

            self.extend_status_label.config(text = "Срок возврата продлен на 14 дней!", fg = "green")
            self.extend_issue_id_entry.delete(0, END)
            self.extend_info_label.config(text = "Введите ID выдачи", fg = "black")

        except Exception as e:
            self.auth.db.connection.rollback()
            messagebox.showerror("Ошибка", f"Ошибка продления срока: {e}")

    def load_active_issues(self):
        try:
            for item in self.active_issues_tree.get_children():
                self.active_issues_tree.delete(item)

            query = """
            SELECT bd.id, b.title, u.login, bd.vz_date, bd.status
            FROM book_dist bd
            JOIN books b ON bd.book_id = b.id
            JOIN users u ON bd.user_id = u.id
            WHERE bd.status = 'active'
            ORDER BY bd.vz_date DESC
            """

            self.auth.db.cursor.execute(query)
            issues = self.auth.db.cursor.fetchall()

            for issue in issues:
                self.active_issues_tree.insert("", "end", values = issue)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить активные выдачи: {e}")

    def load_books_catalog(self, event = None):
        try:
            for item in self.catalog_tree.get_children():
                self.catalog_tree.delete(item)

            sort_by = self.sort_var.get()
            query = """
            SELECT b.id, b.title, b.description, b.all_copies, b.last_copies,
                   STRING_AGG(DISTINCT a.first_name || ' ' || a.last_name, ', ') as authors,
                   STRING_AGG(DISTINCT g.name, ', ') as genres
            FROM books b
            LEFT JOIN book_authors ba ON b.id = ba.book_id
            LEFT JOIN authors a ON ba.author_id = a.id
            LEFT JOIN book_genres bg ON b.id = bg.book_id
            LEFT JOIN genres g ON bg.genre_id = g.id
            GROUP BY b.id, b.title, b.description, b.all_copies, b.last_copies
            ORDER BY 
                CASE %s 
                    WHEN 'title' THEN b.title
                    WHEN 'author' THEN STRING_AGG(DISTINCT a.first_name || ' ' || a.last_name, ', ')
                    WHEN 'genre' THEN STRING_AGG(DISTINCT g.name, ', ')
                    ELSE b.title
                END
            """

            self.auth.db.cursor.execute(query, (sort_by,))
            books = self.auth.db.cursor.fetchall()

            for book in books:
                self.catalog_tree.insert("", "end", values = book)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить каталог: {e}")

    def search_books(self):
        try:
            for item in self.search_tree.get_children():
                self.search_tree.delete(item)

            title = self.search_title.get().strip()
            author = self.search_author.get().strip()
            genre = self.search_genre.get().strip()

            query = """
            SELECT b.id, b.title, b.description, b.all_copies, b.last_copies,
                   STRING_AGG(DISTINCT a.first_name || ' ' || a.last_name, ', ') as authors,
                   STRING_AGG(DISTINCT g.name, ', ') as genres
            FROM books b
            LEFT JOIN book_authors ba ON b.id = ba.book_id
            LEFT JOIN authors a ON ba.author_id = a.id
            LEFT JOIN book_genres bg ON b.id = bg.book_id
            LEFT JOIN genres g ON bg.genre_id = g.id
            WHERE 1=1
            """

            params = []

            if title:
                query += " AND LOWER(b.title) LIKE LOWER(%s)"
                params.append(f"%{title}%")

            if author:
                query += " AND (LOWER(a.first_name) LIKE LOWER(%s) OR LOWER(a.last_name) LIKE LOWER(%s))"
                params.append(f"%{author}%")
                params.append(f"%{author}%")

            if genre:
                query += " AND LOWER(g.name) LIKE LOWER(%s)"
                params.append(f"%{genre}%")

            query += " GROUP BY b.id, b.title, b.description, b.all_copies, b.last_copies"
            query += " ORDER BY b.title"

            self.auth.db.cursor.execute(query, params)
            books = self.auth.db.cursor.fetchall()

            for book in books:
                self.search_tree.insert("", "end", values = book)

            if not books:
                messagebox.showinfo("Поиск", "Книги по заданным критериям не найдены")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска: {e}")

    def clear_search(self):
        self.search_title.delete(0, END)
        self.search_author.delete(0, END)
        self.search_genre.delete(0, END)
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)

    def load_current_books(self):
        try:
            for item in self.current_tree.get_children():
                self.current_tree.delete(item)

            query = """
            SELECT bd.id, b.title, 
                   STRING_AGG(DISTINCT a.first_name || ' ' || a.last_name, ', ') as authors,
                   bd.vz_date, bd.status
            FROM book_dist bd
            JOIN books b ON bd.book_id = b.id
            LEFT JOIN book_authors ba ON b.id = ba.book_id
            LEFT JOIN authors a ON ba.author_id = a.id
            WHERE bd.user_id = %s AND bd.status IN ('active', 'overdue')
            GROUP BY bd.id, b.title, bd.vz_date, bd.status
            ORDER BY bd.vz_date DESC
            """

            self.auth.db.cursor.execute(query, (self.user_id,))
            books = self.auth.db.cursor.fetchall()

            for book in books:
                self.current_tree.insert("", "end", values = book)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить текущие книги: {e}")

    def load_history_books(self):
        try:
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)

            query = """
            SELECT bd.id, b.title, 
                   STRING_AGG(DISTINCT a.first_name || ' ' || a.last_name, ', ') as authors,
                   bd.vz_date, bd.ot_date, bd.status
            FROM book_dist bd
            JOIN books b ON bd.book_id = b.id
            LEFT JOIN book_authors ba ON b.id = ba.book_id
            LEFT JOIN authors a ON ba.author_id = a.id
            WHERE bd.user_id = %s
            GROUP BY bd.id, b.title, bd.vz_date, bd.ot_date, bd.status
            ORDER BY bd.vz_date DESC
            """

            self.auth.db.cursor.execute(query, (self.user_id,))
            books = self.auth.db.cursor.fetchall()

            for book in books:
                self.history_tree.insert("", "end", values = book)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {e}")

    def logout(self):
        self.auth.close_connection()
        self.root.destroy()


# Классы WorkerMainWindow и UserMainWindow остаются без изменений
# (они уже были в предыдущем коде)

class WorkerMainWindow:
    def __init__(self, root, user_id, login):
        self.root = root
        self.user_id = user_id
        self.login = login
        self.auth = AuthManager()
        self.create_widgets()

    def create_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title(f"Библиотека - Работник: {self.login}")
        self.root.geometry("1200x800")

        header_frame = Frame(self.root, bg = "lightgreen", height = 80)
        header_frame.pack(fill = X, padx = 10, pady = 10)
        header_frame.pack_propagate(False)

        title_label = Label(header_frame, text = f"Рабочее место: {self.login}",
                            font = ("Arial", 16, "bold"), bg = "lightgreen")
        title_label.pack(side = LEFT, padx = 20, pady = 20)

        logout_button = Button(header_frame, text = "Выйти", font = ("Arial", 12),
                               command = self.logout)
        logout_button.pack(side = RIGHT, padx = 20, pady = 20)

        main_frame = Frame(self.root)
        main_frame.pack(fill = BOTH, expand = True, padx = 10, pady = 10)

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill = BOTH, expand = True)

        # Все вкладки пользователя
        self.create_catalog_tab()
        self.create_search_tab()
        self.create_current_books_tab()
        self.create_history_tab()

        # Дополнительные вкладки работника
        self.create_issue_book_tab()
        self.create_return_book_tab()
        self.create_extend_book_tab()
        self.create_active_issues_tab()

    def create_catalog_tab(self):
        catalog_frame = Frame(self.notebook)
        self.notebook.add(catalog_frame, text = "Каталог книг")

        Label(catalog_frame, text = "Каталог всех книг", font = ("Arial", 14, "bold")).pack(pady = 10)

        filter_frame = Frame(catalog_frame)
        filter_frame.pack(fill = X, padx = 10, pady = 5)

        Label(filter_frame, text = "Сортировка:").pack(side = LEFT, padx = 5)
        self.sort_var = StringVar(value = "title")
        sort_combo = ttk.Combobox(filter_frame, textvariable = self.sort_var,
                                  values = ["title", "author", "genre"], state = "readonly")
        sort_combo.pack(side = LEFT, padx = 5)
        sort_combo.bind('<<ComboboxSelected>>', self.load_books_catalog)

        Button(filter_frame, text = "Обновить", command = self.load_books_catalog).pack(side = RIGHT, padx = 5)

        columns = ("ID", "Название", "Авторы", "Жанры", "Всего", "Доступно", "Описание")
        self.catalog_tree = ttk.Treeview(catalog_frame, columns = columns, show = "headings", height = 20)

        for col in columns:
            self.catalog_tree.heading(col, text = col)
            self.catalog_tree.column(col, width = 100)

        self.catalog_tree.column("Название", width = 200)
        self.catalog_tree.column("Авторы", width = 150)
        self.catalog_tree.column("Жанры", width = 150)
        self.catalog_tree.column("Описание", width = 300)

        scrollbar = ttk.Scrollbar(catalog_frame, orient = VERTICAL, command = self.catalog_tree.yview)
        self.catalog_tree.configure(yscrollcommand = scrollbar.set)

        self.catalog_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        self.load_books_catalog()

    def create_search_tab(self):
        search_frame = Frame(self.notebook)
        self.notebook.add(search_frame, text = "Поиск книг")

        search_top_frame = Frame(search_frame)
        search_top_frame.pack(fill = X, padx = 10, pady = 10)

        Label(search_top_frame, text = "Название:").grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "w")
        self.search_title = Entry(search_top_frame, width = 20)
        self.search_title.grid(row = 0, column = 1, padx = 5, pady = 5)

        Label(search_top_frame, text = "Автор:").grid(row = 0, column = 2, padx = 5, pady = 5, sticky = "w")
        self.search_author = Entry(search_top_frame, width = 20)
        self.search_author.grid(row = 0, column = 3, padx = 5, pady = 5)

        Label(search_top_frame, text = "Жанр:").grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "w")
        self.search_genre = Entry(search_top_frame, width = 20)
        self.search_genre.grid(row = 1, column = 1, padx = 5, pady = 5)

        Button(search_top_frame, text = "Найти", command = self.search_books).grid(row = 1, column = 2, padx = 5,
                                                                                   pady = 5)
        Button(search_top_frame, text = "Очистить", command = self.clear_search).grid(row = 1, column = 3, padx = 5,
                                                                                      pady = 5)

        columns = ("ID", "Название", "Авторы", "Жанры", "Всего", "Доступно", "Описание")
        self.search_tree = ttk.Treeview(search_frame, columns = columns, show = "headings", height = 20)

        for col in columns:
            self.search_tree.heading(col, text = col)
            self.search_tree.column(col, width = 100)

        self.search_tree.column("Название", width = 200)
        self.search_tree.column("Авторы", width = 150)
        self.search_tree.column("Жанры", width = 150)
        self.search_tree.column("Описание", width = 300)

        scrollbar = ttk.Scrollbar(search_frame, orient = VERTICAL, command = self.search_tree.yview)
        self.search_tree.configure(yscrollcommand = scrollbar.set)

        self.search_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

    def create_current_books_tab(self):
        current_frame = Frame(self.notebook)
        self.notebook.add(current_frame, text = "Мои текущие книги")

        Label(current_frame, text = "Книги, которые у меня сейчас", font = ("Arial", 14, "bold")).pack(pady = 10)

        columns = ("ID", "Название", "Авторы", "Дата взятия", "Статус")
        self.current_tree = ttk.Treeview(current_frame, columns = columns, show = "headings", height = 20)

        for col in columns:
            self.current_tree.heading(col, text = col)
            self.current_tree.column(col, width = 120)

        self.current_tree.column("Название", width = 200)
        self.current_tree.column("Авторы", width = 150)

        scrollbar = ttk.Scrollbar(current_frame, orient = VERTICAL, command = self.current_tree.yview)
        self.current_tree.configure(yscrollcommand = scrollbar.set)

        self.current_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        Button(current_frame, text = "Обновить", command = self.load_current_books).pack(pady = 5)

        self.load_current_books()

    def create_history_tab(self):
        history_frame = Frame(self.notebook)
        self.notebook.add(history_frame, text = "История книг")

        Label(history_frame, text = "История всех взятых мной книг", font = ("Arial", 14, "bold")).pack(pady = 10)

        columns = ("ID", "Название", "Авторы", "Дата взятия", "Дата возврата", "Статус")
        self.history_tree = ttk.Treeview(history_frame, columns = columns, show = "headings", height = 20)

        for col in columns:
            self.history_tree.heading(col, text = col)
            self.history_tree.column(col, width = 100)

        self.history_tree.column("Название", width = 200)
        self.history_tree.column("Авторы", width = 150)

        scrollbar = ttk.Scrollbar(history_frame, orient = VERTICAL, command = self.history_tree.yview)
        self.history_tree.configure(yscrollcommand = scrollbar.set)

        self.history_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        Button(history_frame, text = "Обновить", command = self.load_history_books).pack(pady = 5)

        self.load_history_books()

    def create_issue_book_tab(self):
        """Вкладка выдачи книг"""
        issue_frame = Frame(self.notebook)
        self.notebook.add(issue_frame, text = "Выдача книг")

        Label(issue_frame, text = "Выдача книги пользователю", font = ("Arial", 14, "bold")).pack(pady = 10)

        form_frame = Frame(issue_frame)
        form_frame.pack(fill = X, padx = 20, pady = 10)

        # Пользователь
        Label(form_frame, text = "Логин пользователя:", font = ("Arial", 12)).grid(row = 0, column = 0, padx = 5,
                                                                                   pady = 5, sticky = "w")
        self.user_login_entry = Entry(form_frame, font = ("Arial", 12), width = 20)
        self.user_login_entry.grid(row = 0, column = 1, padx = 5, pady = 5)

        Button(form_frame, text = "Найти пользователя", command = self.find_user).grid(row = 0, column = 2, padx = 5,
                                                                                       pady = 5)

        # ID книги
        Label(form_frame, text = "ID книги:", font = ("Arial", 12)).grid(row = 1, column = 0, padx = 5, pady = 5,
                                                                         sticky = "w")
        self.book_id_entry = Entry(form_frame, font = ("Arial", 12), width = 20)
        self.book_id_entry.grid(row = 1, column = 1, padx = 5, pady = 5)

        Button(form_frame, text = "Найти книгу", command = self.find_book).grid(row = 1, column = 2, padx = 5, pady = 5)

        # Информация о найденных данных
        info_frame = Frame(issue_frame)
        info_frame.pack(fill = X, padx = 20, pady = 10)

        self.user_info_label = Label(info_frame, text = "Пользователь не найден", font = ("Arial", 10), fg = "red")
        self.user_info_label.pack(anchor = "w")

        self.book_info_label = Label(info_frame, text = "Книга не найдена", font = ("Arial", 10), fg = "red")
        self.book_info_label.pack(anchor = "w")

        # Кнопка выдачи
        Button(issue_frame, text = "Выдать книгу", font = ("Arial", 12),
               command = self.issue_book, bg = "lightgreen").pack(pady = 10)

        self.issue_status_label = Label(issue_frame, text = "", font = ("Arial", 10))
        self.issue_status_label.pack(pady = 5)

    def create_return_book_tab(self):
        """Вкладка приема возвращенных книг"""
        return_frame = Frame(self.notebook)
        self.notebook.add(return_frame, text = "Прием книг")

        Label(return_frame, text = "Прием возвращенных книг", font = ("Arial", 14, "bold")).pack(pady = 10)

        # Поиск активных выдач
        search_frame = Frame(return_frame)
        search_frame.pack(fill = X, padx = 20, pady = 10)

        Label(search_frame, text = "ID выдачи:", font = ("Arial", 12)).grid(row = 0, column = 0, padx = 5, pady = 5,
                                                                            sticky = "w")
        self.return_issue_id_entry = Entry(search_frame, font = ("Arial", 12), width = 20)
        self.return_issue_id_entry.grid(row = 0, column = 1, padx = 5, pady = 5)

        Button(search_frame, text = "Найти выдачу", command = self.find_issue_for_return).grid(row = 0, column = 2,
                                                                                               padx = 5, pady = 5)

        # Информация о выдаче
        self.return_info_frame = Frame(return_frame)
        self.return_info_frame.pack(fill = X, padx = 20, pady = 10)

        self.return_info_label = Label(self.return_info_frame, text = "Введите ID выдачи", font = ("Arial", 10))
        self.return_info_label.pack(anchor = "w")

        # Кнопка приема
        Button(return_frame, text = "Принять книгу", font = ("Arial", 12),
               command = self.return_book, bg = "lightcoral").pack(pady = 10)

        self.return_status_label = Label(return_frame, text = "", font = ("Arial", 10))
        self.return_status_label.pack(pady = 5)

    def create_extend_book_tab(self):
        """Вкладка продления срока возврата"""
        extend_frame = Frame(self.notebook)
        self.notebook.add(extend_frame, text = "Продление книг")

        Label(extend_frame, text = "Продление срока возврата книги", font = ("Arial", 14, "bold")).pack(pady = 10)

        search_frame = Frame(extend_frame)
        search_frame.pack(fill = X, padx = 20, pady = 10)

        Label(search_frame, text = "ID выдачи:", font = ("Arial", 12)).grid(row = 0, column = 0, padx = 5, pady = 5,
                                                                            sticky = "w")
        self.extend_issue_id_entry = Entry(search_frame, font = ("Arial", 12), width = 20)
        self.extend_issue_id_entry.grid(row = 0, column = 1, padx = 5, pady = 5)

        Button(search_frame, text = "Найти выдачу", command = self.find_issue_for_extend).grid(row = 0, column = 2,
                                                                                               padx = 5, pady = 5)

        self.extend_info_frame = Frame(extend_frame)
        self.extend_info_frame.pack(fill = X, padx = 20, pady = 10)

        self.extend_info_label = Label(self.extend_info_frame, text = "Введите ID выдачи", font = ("Arial", 10))
        self.extend_info_label.pack(anchor = "w")

        Button(extend_frame, text = "Продлить на 14 дней", font = ("Arial", 12),
               command = self.extend_book, bg = "lightyellow").pack(pady = 10)

        self.extend_status_label = Label(extend_frame, text = "", font = ("Arial", 10))
        self.extend_status_label.pack(pady = 5)

    def create_active_issues_tab(self):
        """Вкладка просмотра активных выдач"""
        active_frame = Frame(self.notebook)
        self.notebook.add(active_frame, text = "Активные выдачи")

        Label(active_frame, text = "Все активные выдачи книг", font = ("Arial", 14, "bold")).pack(pady = 10)

        columns = ("ID выдачи", "Книга", "Пользователь", "Дата выдачи", "Статус")
        self.active_issues_tree = ttk.Treeview(active_frame, columns = columns, show = "headings", height = 20)

        for col in columns:
            self.active_issues_tree.heading(col, text = col)
            self.active_issues_tree.column(col, width = 120)

        self.active_issues_tree.column("Книга", width = 200)
        self.active_issues_tree.column("Пользователь", width = 150)

        scrollbar = ttk.Scrollbar(active_frame, orient = VERTICAL, command = self.active_issues_tree.yview)
        self.active_issues_tree.configure(yscrollcommand = scrollbar.set)

        self.active_issues_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        Button(active_frame, text = "Обновить", command = self.load_active_issues).pack(pady = 5)

        self.load_active_issues()

    # Методы для работника
    def find_user(self):
        login = self.user_login_entry.get().strip()
        if not login:
            messagebox.showwarning("Ошибка", "Введите логин пользователя")
            return

        try:
            query = "SELECT id, login FROM users WHERE login = %s"
            self.auth.db.cursor.execute(query, (login,))
            user = self.auth.db.cursor.fetchone()

            if user:
                self.found_user_id = user[0]
                self.user_info_label.config(text = f"Найден пользователь: {user[1]} (ID: {user[0]})", fg = "green")
            else:
                self.found_user_id = None
                self.user_info_label.config(text = "Пользователь не найден", fg = "red")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска пользователя: {e}")

    def find_book(self):
        book_id = self.book_id_entry.get().strip()
        if not book_id:
            messagebox.showwarning("Ошибка", "Введите ID книги")
            return

        try:
            query = "SELECT id, title, last_copies FROM books WHERE id = %s"
            self.auth.db.cursor.execute(query, (book_id,))
            book = self.auth.db.cursor.fetchone()

            if book:
                self.found_book_id = book[0]
                available = "Доступна" if book[2] > 0 else "Нет в наличии"
                self.book_info_label.config(text = f"Найдена книга: '{book[1]}' (ID: {book[0]}), {available}",
                                            fg = "green" if book[2] > 0 else "red")
            else:
                self.found_book_id = None
                self.book_info_label.config(text = "Книга не найдена", fg = "red")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска книги: {e}")

    def issue_book(self):
        if not hasattr(self, 'found_user_id') or not self.found_user_id:
            messagebox.showwarning("Ошибка", "Сначала найдите пользователя")
            return

        if not hasattr(self, 'found_book_id') or not self.found_book_id:
            messagebox.showwarning("Ошибка", "Сначала найдите книгу")
            return

        try:
            # Проверяем доступность книги
            query = "SELECT last_copies FROM books WHERE id = %s"
            self.auth.db.cursor.execute(query, (self.found_book_id,))
            book = self.auth.db.cursor.fetchone()

            if not book or book[0] <= 0:
                messagebox.showerror("Ошибка", "Книга недоступна для выдачи")
                return

            # Создаем запись о выдаче
            issue_date = datetime.now().date()
            query = """
            INSERT INTO book_dist (book_id, user_id, libuser_id, vz_date, status) 
            VALUES (%s, %s, %s, %s, 'active')
            """
            self.auth.db.cursor.execute(query, (self.found_book_id, self.found_user_id, self.user_id, issue_date))

            # Уменьшаем количество доступных книг
            query = "UPDATE books SET last_copies = last_copies - 1 WHERE id = %s"
            self.auth.db.cursor.execute(query, (self.found_book_id,))

            self.auth.db.connection.commit()

            self.issue_status_label.config(text = "Книга успешно выдана!", fg = "green")
            self.user_login_entry.delete(0, END)
            self.book_id_entry.delete(0, END)
            self.user_info_label.config(text = "Пользователь не найден", fg = "red")
            self.book_info_label.config(text = "Книга не найдена", fg = "red")

        except Exception as e:
            self.auth.db.connection.rollback()
            messagebox.showerror("Ошибка", f"Ошибка выдачи книги: {e}")

    def find_issue_for_return(self):
        issue_id = self.return_issue_id_entry.get().strip()
        if not issue_id:
            messagebox.showwarning("Ошибка", "Введите ID выдачи")
            return

        try:
            query = """
            SELECT bd.id, b.title, u.login, bd.vz_date, bd.status 
            FROM book_dist bd
            JOIN books b ON bd.book_id = b.id
            JOIN users u ON bd.user_id = u.id
            WHERE bd.id = %s AND bd.status = 'active'
            """
            self.auth.db.cursor.execute(query, (issue_id,))
            issue = self.auth.db.cursor.fetchone()

            if issue:
                self.return_issue_id = issue[0]
                info_text = f"Книга: '{issue[1]}', Пользователь: {issue[2]}, Дата выдачи: {issue[3]}"
                self.return_info_label.config(text = info_text, fg = "green")
            else:
                self.return_issue_id = None
                self.return_info_label.config(text = "Активная выдача не найдена", fg = "red")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска выдачи: {e}")

    def return_book(self):
        if not hasattr(self, 'return_issue_id') or not self.return_issue_id:
            messagebox.showwarning("Ошибка", "Сначала найдите активную выдачу")
            return

        try:
            return_date = datetime.now().date()

            # Получаем book_id для обновления количества
            query = "SELECT book_id FROM book_dist WHERE id = %s"
            self.auth.db.cursor.execute(query, (self.return_issue_id,))
            result = self.auth.db.cursor.fetchone()
            book_id = result[0]

            # Обновляем статус выдачи
            query = "UPDATE book_dist SET status = 'return', ot_date = %s WHERE id = %s"
            self.auth.db.cursor.execute(query, (return_date, self.return_issue_id))

            # Увеличиваем количество доступных книг
            query = "UPDATE books SET last_copies = last_copies + 1 WHERE id = %s"
            self.auth.db.cursor.execute(query, (book_id,))

            self.auth.db.connection.commit()

            self.return_status_label.config(text = "Книга успешно принята!", fg = "green")
            self.return_issue_id_entry.delete(0, END)
            self.return_info_label.config(text = "Введите ID выдачи", fg = "black")

        except Exception as e:
            self.auth.db.connection.rollback()
            messagebox.showerror("Ошибка", f"Ошибка приема книги: {e}")

    def find_issue_for_extend(self):
        issue_id = self.extend_issue_id_entry.get().strip()
        if not issue_id:
            messagebox.showwarning("Ошибка", "Введите ID выдачи")
            return

        try:
            query = """
            SELECT bd.id, b.title, u.login, bd.vz_date 
            FROM book_dist bd
            JOIN books b ON bd.book_id = b.id
            JOIN users u ON bd.user_id = u.id
            WHERE bd.id = %s AND bd.status = 'active'
            """
            self.auth.db.cursor.execute(query, (issue_id,))
            issue = self.auth.db.cursor.fetchone()

            if issue:
                self.extend_issue_id = issue[0]
                info_text = f"Книга: '{issue[1]}', Пользователь: {issue[2]}, Дата выдачи: {issue[3]}"
                self.extend_info_label.config(text = info_text, fg = "green")
            else:
                self.extend_issue_id = None
                self.extend_info_label.config(text = "Активная выдача не найдена", fg = "red")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска выдачи: {e}")

    def extend_book(self):
        if not hasattr(self, 'extend_issue_id') or not self.extend_issue_id:
            messagebox.showwarning("Ошибка", "Сначала найдите активную выдачу")
            return

        try:
            query = "UPDATE book_dist SET status = 'active' WHERE id = %s"
            self.auth.db.cursor.execute(query, (self.extend_issue_id,))
            self.auth.db.connection.commit()

            self.extend_status_label.config(text = "Срок возврата продлен на 14 дней!", fg = "green")
            self.extend_issue_id_entry.delete(0, END)
            self.extend_info_label.config(text = "Введите ID выдачи", fg = "black")

        except Exception as e:
            self.auth.db.connection.rollback()
            messagebox.showerror("Ошибка", f"Ошибка продления срока: {e}")

    def load_active_issues(self):
        try:
            for item in self.active_issues_tree.get_children():
                self.active_issues_tree.delete(item)

            query = """
            SELECT bd.id, b.title, u.login, bd.vz_date, bd.status
            FROM book_dist bd
            JOIN books b ON bd.book_id = b.id
            JOIN users u ON bd.user_id = u.id
            WHERE bd.status = 'active'
            ORDER BY bd.vz_date DESC
            """

            self.auth.db.cursor.execute(query)
            issues = self.auth.db.cursor.fetchall()

            for issue in issues:
                self.active_issues_tree.insert("", "end", values = issue)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить активные выдачи: {e}")

    # Общие методы (такие же как в UserMainWindow)
    def load_books_catalog(self, event = None):
        try:
            for item in self.catalog_tree.get_children():
                self.catalog_tree.delete(item)

            sort_by = self.sort_var.get()
            query = """
            SELECT b.id, b.title, b.description, b.all_copies, b.last_copies,
                   STRING_AGG(DISTINCT a.first_name || ' ' || a.last_name, ', ') as authors,
                   STRING_AGG(DISTINCT g.name, ', ') as genres
            FROM books b
            LEFT JOIN book_authors ba ON b.id = ba.book_id
            LEFT JOIN authors a ON ba.author_id = a.id
            LEFT JOIN book_genres bg ON b.id = bg.book_id
            LEFT JOIN genres g ON bg.genre_id = g.id
            GROUP BY b.id, b.title, b.description, b.all_copies, b.last_copies
            ORDER BY 
                CASE %s 
                    WHEN 'title' THEN b.title
                    WHEN 'author' THEN STRING_AGG(DISTINCT a.first_name || ' ' || a.last_name, ', ')
                    WHEN 'genre' THEN STRING_AGG(DISTINCT g.name, ', ')
                    ELSE b.title
                END
            """

            self.auth.db.cursor.execute(query, (sort_by,))
            books = self.auth.db.cursor.fetchall()

            for book in books:
                self.catalog_tree.insert("", "end", values = book)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить каталог: {e}")

    def search_books(self):
        try:
            for item in self.search_tree.get_children():
                self.search_tree.delete(item)

            title = self.search_title.get().strip()
            author = self.search_author.get().strip()
            genre = self.search_genre.get().strip()

            query = """
            SELECT b.id, b.title, b.description, b.all_copies, b.last_copies,
                   STRING_AGG(DISTINCT a.first_name || ' ' || a.last_name, ', ') as authors,
                   STRING_AGG(DISTINCT g.name, ', ') as genres
            FROM books b
            LEFT JOIN book_authors ba ON b.id = ba.book_id
            LEFT JOIN authors a ON ba.author_id = a.id
            LEFT JOIN book_genres bg ON b.id = bg.book_id
            LEFT JOIN genres g ON bg.genre_id = g.id
            WHERE 1=1
            """

            params = []

            if title:
                query += " AND LOWER(b.title) LIKE LOWER(%s)"
                params.append(f"%{title}%")

            if author:
                query += " AND (LOWER(a.first_name) LIKE LOWER(%s) OR LOWER(a.last_name) LIKE LOWER(%s))"
                params.append(f"%{author}%")
                params.append(f"%{author}%")

            if genre:
                query += " AND LOWER(g.name) LIKE LOWER(%s)"
                params.append(f"%{genre}%")

            query += " GROUP BY b.id, b.title, b.description, b.all_copies, b.last_copies"
            query += " ORDER BY b.title"

            self.auth.db.cursor.execute(query, params)
            books = self.auth.db.cursor.fetchall()

            for book in books:
                self.search_tree.insert("", "end", values = book)

            if not books:
                messagebox.showinfo("Поиск", "Книги по заданным критериям не найдены")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска: {e}")

    def clear_search(self):
        self.search_title.delete(0, END)
        self.search_author.delete(0, END)
        self.search_genre.delete(0, END)
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)

    def load_current_books(self):
        try:
            for item in self.current_tree.get_children():
                self.current_tree.delete(item)

            query = """
            SELECT bd.id, b.title, 
                   STRING_AGG(DISTINCT a.first_name || ' ' || a.last_name, ', ') as authors,
                   bd.vz_date, bd.status
            FROM book_dist bd
            JOIN books b ON bd.book_id = b.id
            LEFT JOIN book_authors ba ON b.id = ba.book_id
            LEFT JOIN authors a ON ba.author_id = a.id
            WHERE bd.user_id = %s AND bd.status IN ('active', 'overdue')
            GROUP BY bd.id, b.title, bd.vz_date, bd.status
            ORDER BY bd.vz_date DESC
            """

            self.auth.db.cursor.execute(query, (self.user_id,))
            books = self.auth.db.cursor.fetchall()

            for book in books:
                self.current_tree.insert("", "end", values = book)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить текущие книги: {e}")

    def load_history_books(self):
        try:
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)

            query = """
            SELECT bd.id, b.title, 
                   STRING_AGG(DISTINCT a.first_name || ' ' || a.last_name, ', ') as authors,
                   bd.vz_date, bd.ot_date, bd.status
            FROM book_dist bd
            JOIN books b ON bd.book_id = b.id
            LEFT JOIN book_authors ba ON b.id = ba.book_id
            LEFT JOIN authors a ON ba.author_id = a.id
            WHERE bd.user_id = %s
            GROUP BY bd.id, b.title, bd.vz_date, bd.ot_date, bd.status
            ORDER BY bd.vz_date DESC
            """

            self.auth.db.cursor.execute(query, (self.user_id,))
            books = self.auth.db.cursor.fetchall()

            for book in books:
                self.history_tree.insert("", "end", values = book)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {e}")

    def logout(self):
        self.auth.close_connection()
        self.root.destroy()


class UserMainWindow:
    def __init__(self, root, user_id, login):
        self.root = root
        self.user_id = user_id
        self.login = login
        self.auth = AuthManager()
        self.create_widgets()

    def create_widgets(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.title(f"Библиотека - Пользователь: {self.login}")
        self.root.geometry("1000x700")

        header_frame = Frame(self.root, bg = "lightblue", height = 80)
        header_frame.pack(fill = X, padx = 10, pady = 10)
        header_frame.pack_propagate(False)

        title_label = Label(header_frame, text = f"Добро пожаловать, {self.login}!",
                            font = ("Arial", 16, "bold"), bg = "lightblue")
        title_label.pack(side = LEFT, padx = 20, pady = 20)

        logout_button = Button(header_frame, text = "Выйти", font = ("Arial", 12),
                               command = self.logout)
        logout_button.pack(side = RIGHT, padx = 20, pady = 20)

        main_frame = Frame(self.root)
        main_frame.pack(fill = BOTH, expand = True, padx = 10, pady = 10)

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill = BOTH, expand = True)

        self.create_catalog_tab()
        self.create_search_tab()
        self.create_current_books_tab()
        self.create_history_tab()

    def create_catalog_tab(self):
        catalog_frame = Frame(self.notebook)
        self.notebook.add(catalog_frame, text = "Каталог книг")

        Label(catalog_frame, text = "Каталог всех книг", font = ("Arial", 14, "bold")).pack(pady = 10)

        filter_frame = Frame(catalog_frame)
        filter_frame.pack(fill = X, padx = 10, pady = 5)

        Label(filter_frame, text = "Сортировка:").pack(side = LEFT, padx = 5)
        self.sort_var = StringVar(value = "title")
        sort_combo = ttk.Combobox(filter_frame, textvariable = self.sort_var,
                                  values = ["title", "author", "genre"], state = "readonly")
        sort_combo.pack(side = LEFT, padx = 5)
        sort_combo.bind('<<ComboboxSelected>>', self.load_books_catalog)

        Button(filter_frame, text = "Обновить", command = self.load_books_catalog).pack(side = RIGHT, padx = 5)

        columns = ("ID", "Название", "Авторы", "Жанры", "Всего", "Доступно", "Описание")
        self.catalog_tree = ttk.Treeview(catalog_frame, columns = columns, show = "headings", height = 20)

        for col in columns:
            self.catalog_tree.heading(col, text = col)
            self.catalog_tree.column(col, width = 100)

        self.catalog_tree.column("Название", width = 200)
        self.catalog_tree.column("Авторы", width = 150)
        self.catalog_tree.column("Жанры", width = 150)
        self.catalog_tree.column("Описание", width = 300)

        scrollbar = ttk.Scrollbar(catalog_frame, orient = VERTICAL, command = self.catalog_tree.yview)
        self.catalog_tree.configure(yscrollcommand = scrollbar.set)

        self.catalog_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        self.load_books_catalog()

    def create_search_tab(self):
        search_frame = Frame(self.notebook)
        self.notebook.add(search_frame, text = "Поиск книг")

        search_top_frame = Frame(search_frame)
        search_top_frame.pack(fill = X, padx = 10, pady = 10)

        Label(search_top_frame, text = "Название:").grid(row = 0, column = 0, padx = 5, pady = 5, sticky = "w")
        self.search_title = Entry(search_top_frame, width = 20)
        self.search_title.grid(row = 0, column = 1, padx = 5, pady = 5)

        Label(search_top_frame, text = "Автор:").grid(row = 0, column = 2, padx = 5, pady = 5, sticky = "w")
        self.search_author = Entry(search_top_frame, width = 20)
        self.search_author.grid(row = 0, column = 3, padx = 5, pady = 5)

        Label(search_top_frame, text = "Жанр:").grid(row = 1, column = 0, padx = 5, pady = 5, sticky = "w")
        self.search_genre = Entry(search_top_frame, width = 20)
        self.search_genre.grid(row = 1, column = 1, padx = 5, pady = 5)

        Button(search_top_frame, text = "Найти", command = self.search_books).grid(row = 1, column = 2, padx = 5,
                                                                                   pady = 5)
        Button(search_top_frame, text = "Очистить", command = self.clear_search).grid(row = 1, column = 3, padx = 5,
                                                                                      pady = 5)

        columns = ("ID", "Название", "Авторы", "Жанры", "Всего", "Доступно", "Описание")
        self.search_tree = ttk.Treeview(search_frame, columns = columns, show = "headings", height = 20)

        for col in columns:
            self.search_tree.heading(col, text = col)
            self.search_tree.column(col, width = 100)

        self.search_tree.column("Название", width = 200)
        self.search_tree.column("Авторы", width = 150)
        self.search_tree.column("Жанры", width = 150)
        self.search_tree.column("Описание", width = 300)

        scrollbar = ttk.Scrollbar(search_frame, orient = VERTICAL, command = self.search_tree.yview)
        self.search_tree.configure(yscrollcommand = scrollbar.set)

        self.search_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

    def create_current_books_tab(self):
        current_frame = Frame(self.notebook)
        self.notebook.add(current_frame, text = "Мои текущие книги")

        Label(current_frame, text = "Книги, которые у меня сейчас", font = ("Arial", 14, "bold")).pack(pady = 10)

        columns = ("ID", "Название", "Авторы", "Дата взятия", "Статус")
        self.current_tree = ttk.Treeview(current_frame, columns = columns, show = "headings", height = 20)

        for col in columns:
            self.current_tree.heading(col, text = col)
            self.current_tree.column(col, width = 120)

        self.current_tree.column("Название", width = 200)
        self.current_tree.column("Авторы", width = 150)

        scrollbar = ttk.Scrollbar(current_frame, orient = VERTICAL, command = self.current_tree.yview)
        self.current_tree.configure(yscrollcommand = scrollbar.set)

        self.current_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        Button(current_frame, text = "Обновить", command = self.load_current_books).pack(pady = 5)

        self.load_current_books()

    def create_history_tab(self):
        history_frame = Frame(self.notebook)
        self.notebook.add(history_frame, text = "История книг")

        Label(history_frame, text = "История всех взятых мной книг", font = ("Arial", 14, "bold")).pack(pady = 10)

        columns = ("ID", "Название", "Авторы", "Дата взятия", "Дата возврата", "Статус")
        self.history_tree = ttk.Treeview(history_frame, columns = columns, show = "headings", height = 20)

        for col in columns:
            self.history_tree.heading(col, text = col)
            self.history_tree.column(col, width = 100)

        self.history_tree.column("Название", width = 200)
        self.history_tree.column("Авторы", width = 150)

        scrollbar = ttk.Scrollbar(history_frame, orient = VERTICAL, command = self.history_tree.yview)
        self.history_tree.configure(yscrollcommand = scrollbar.set)

        self.history_tree.pack(side = LEFT, fill = BOTH, expand = True, padx = (10, 0), pady = 10)
        scrollbar.pack(side = RIGHT, fill = Y, padx = (0, 10), pady = 10)

        Button(history_frame, text = "Обновить", command = self.load_history_books).pack(pady = 5)

        self.load_history_books()

    def load_books_catalog(self, event = None):
        try:
            for item in self.catalog_tree.get_children():
                self.catalog_tree.delete(item)

            sort_by = self.sort_var.get()
            query = """
            SELECT b.id, b.title, b.description, b.all_copies, b.last_copies,
                   STRING_AGG(DISTINCT a.first_name || ' ' || a.last_name, ', ') as authors,
                   STRING_AGG(DISTINCT g.name, ', ') as genres
            FROM books b
            LEFT JOIN book_authors ba ON b.id = ba.book_id
            LEFT JOIN authors a ON ba.author_id = a.id
            LEFT JOIN book_genres bg ON b.id = bg.book_id
            LEFT JOIN genres g ON bg.genre_id = g.id
            GROUP BY b.id, b.title, b.description, b.all_copies, b.last_copies
            ORDER BY 
                CASE %s 
                    WHEN 'title' THEN b.title
                    WHEN 'author' THEN STRING_AGG(DISTINCT a.first_name || ' ' || a.last_name, ', ')
                    WHEN 'genre' THEN STRING_AGG(DISTINCT g.name, ', ')
                    ELSE b.title
                END
            """

            self.auth.db.cursor.execute(query, (sort_by,))
            books = self.auth.db.cursor.fetchall()

            for book in books:
                self.catalog_tree.insert("", "end", values = book)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить каталог: {e}")

    def search_books(self):
        try:
            for item in self.search_tree.get_children():
                self.search_tree.delete(item)

            title = self.search_title.get().strip()
            author = self.search_author.get().strip()
            genre = self.search_genre.get().strip()

            query = """
            SELECT b.id, b.title, b.description, b.all_copies, b.last_copies,
                   STRING_AGG(DISTINCT a.first_name || ' ' || a.last_name, ', ') as authors,
                   STRING_AGG(DISTINCT g.name, ', ') as genres
            FROM books b
            LEFT JOIN book_authors ba ON b.id = ba.book_id
            LEFT JOIN authors a ON ba.author_id = a.id
            LEFT JOIN book_genres bg ON b.id = bg.book_id
            LEFT JOIN genres g ON bg.genre_id = g.id
            WHERE 1=1
            """

            params = []

            if title:
                query += " AND LOWER(b.title) LIKE LOWER(%s)"
                params.append(f"%{title}%")

            if author:
                query += " AND (LOWER(a.first_name) LIKE LOWER(%s) OR LOWER(a.last_name) LIKE LOWER(%s))"
                params.append(f"%{author}%")
                params.append(f"%{author}%")

            if genre:
                query += " AND LOWER(g.name) LIKE LOWER(%s)"
                params.append(f"%{genre}%")

            query += " GROUP BY b.id, b.title, b.description, b.all_copies, b.last_copies"
            query += " ORDER BY b.title"

            self.auth.db.cursor.execute(query, params)
            books = self.auth.db.cursor.fetchall()

            for book in books:
                self.search_tree.insert("", "end", values = book)

            if not books:
                messagebox.showinfo("Поиск", "Книги по заданным критериям не найдены")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка поиска: {e}")

    def clear_search(self):
        self.search_title.delete(0, END)
        self.search_author.delete(0, END)
        self.search_genre.delete(0, END)
        for item in self.search_tree.get_children():
            self.search_tree.delete(item)

    def load_current_books(self):
        try:
            for item in self.current_tree.get_children():
                self.current_tree.delete(item)

            query = """
            SELECT bd.id, b.title, 
                   STRING_AGG(DISTINCT a.first_name || ' ' || a.last_name, ', ') as authors,
                   bd.vz_date, bd.status
            FROM book_dist bd
            JOIN books b ON bd.book_id = b.id
            LEFT JOIN book_authors ba ON b.id = ba.book_id
            LEFT JOIN authors a ON ba.author_id = a.id
            WHERE bd.user_id = %s AND bd.status IN ('active', 'overdue')
            GROUP BY bd.id, b.title, bd.vz_date, bd.status
            ORDER BY bd.vz_date DESC
            """

            self.auth.db.cursor.execute(query, (self.user_id,))
            books = self.auth.db.cursor.fetchall()

            for book in books:
                self.current_tree.insert("", "end", values = book)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить текущие книги: {e}")

    def load_history_books(self):
        try:
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)

            query = """
            SELECT bd.id, b.title, 
                   STRING_AGG(DISTINCT a.first_name || ' ' || a.last_name, ', ') as authors,
                   bd.vz_date, bd.ot_date, bd.status
            FROM book_dist bd
            JOIN books b ON bd.book_id = b.id
            LEFT JOIN book_authors ba ON b.id = ba.book_id
            LEFT JOIN authors a ON ba.author_id = a.id
            WHERE bd.user_id = %s
            GROUP BY bd.id, b.title, bd.vz_date, bd.ot_date, bd.status
            ORDER BY bd.vz_date DESC
            """

            self.auth.db.cursor.execute(query, (self.user_id,))
            books = self.auth.db.cursor.fetchall()

            for book in books:
                self.history_tree.insert("", "end", values = book)

        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить историю: {e}")

    def logout(self):
        self.auth.close_connection()
        self.root.destroy()


class MainApp:
    def __init__(self, root, user_id, login, role_id):
        self.root = root
        self.user_id = user_id
        self.login = login
        self.role_id = role_id

        if role_id == 1:  # user
            self.app = UserMainWindow(root, user_id, login)
        elif role_id == 2:  # worker
            self.app = WorkerMainWindow(root, user_id, login)
        elif role_id == 3:  # admin
            self.app = AdminMainWindow(root, user_id, login)
        else:
            messagebox.showwarning("Предупреждение", "Роль не распознана")
            self.logout()

    def logout(self):
        self.root.destroy()


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.auth = AuthManager()
        self.create_widgets()
        self.setup_bindings()

    def create_widgets(self):
        self.main_frame = Frame(self.root)
        self.main_frame.place(relx = 0.5, rely = 0.5, anchor = CENTER)

        self.title_label = Label(self.main_frame, text = "Библиотека", font = ("Arial", 24, "bold"))
        self.title_label.pack(pady = (0, 30))

        self.input_frame = Frame(self.main_frame)
        self.input_frame.pack(pady = 10)

        self.login_label = Label(self.input_frame, text = "Логин:", font = ("Arial", 12))
        self.login_label.grid(row = 0, column = 0, padx = (0, 10), pady = 5, sticky = "e")

        self.login_entry = Entry(self.input_frame, font = ("Arial", 12), width = 20)
        self.login_entry.grid(row = 0, column = 1, pady = 5)

        self.password_label = Label(self.input_frame, text = "Пароль:", font = ("Arial", 12))
        self.password_label.grid(row = 1, column = 0, padx = (0, 10), pady = 5, sticky = "e")

        self.password_entry = Entry(self.input_frame, font = ("Arial", 12), width = 20, show = "*")
        self.password_entry.grid(row = 1, column = 1, pady = 5)

        self.button_frame = Frame(self.main_frame)
        self.button_frame.pack(pady = 20)

        self.login_button = Button(self.button_frame, text = "Войти", font = ("Arial", 12), width = 12,
                                   command = self.handle_login)
        self.login_button.grid(row = 0, column = 0, padx = (0, 10))

        self.register_button = Button(self.button_frame, text = "Регистрация", font = ("Arial", 12), width = 12,
                                      command = self.handle_register)
        self.register_button.grid(row = 0, column = 1, padx = (10, 0))

        self.status_label = Label(self.main_frame, text = "", font = ("Arial", 10), fg = "red")
        self.status_label.pack(pady = 10)

    def setup_bindings(self):
        self.root.bind('<Return>', lambda event: self.handle_login())

    def handle_login(self):
        login = self.login_entry.get().strip()
        password = self.password_entry.get().strip()

        self.status_label.config(text = "")

        success, message = self.auth.login_user(login, password)

        if success:
            query = "SELECT id, role_id FROM users WHERE login = %s"
            self.auth.db.cursor.execute(query, (login,))
            user_data = self.auth.db.cursor.fetchone()

            if user_data:
                user_id, role_id = user_data
                role_name = "пользователь" if role_id == 1 else "работник" if role_id == 2 else "администратор"
                messagebox.showinfo("Успех", f"Добро пожаловать, {login}!\nВаша роль: {role_name}")
                self.clear_fields()
                MainApp(self.root, user_id, login, role_id)
            else:
                self.status_label.config(text = "Ошибка получения данных пользователя")
        else:
            self.status_label.config(text = message)

    def handle_register(self):
        RegisterWindow(self.root, self.auth)

    def clear_fields(self):
        self.login_entry.delete(0, END)
        self.password_entry.delete(0, END)

    def on_closing(self):
        self.auth.close_connection()
        self.root.destroy()


if __name__ == "__main__":
    root = Tk()
    root.title("Библиотека - Вход")
    root.geometry("1280x720")
    root.resizable(False, False)

    app = LoginWindow(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()