"""
АСУ ПСП "Чистая Планета" - Главный модуль
Автоматизированная система управления производственно-сервисным предприятием
"""

import tkinter as tk
from tkinter import ttk, messagebox
import hashlib
import re

# Заглушки для отсутствующих модулей
class MaterialCalculator:
    def calculate_material_required(self, service_id, material_id, quantity, param, coef, waste):
        """Упрощенный расчет материалов"""
        try:
            base_need = quantity * param * coef
            total_need = base_need * (1 + waste / 100)
            return round(total_need, 2)
        except:
            return -1

class HelpSystem:
    def __init__(self, root):
        self.root = root
    
    def show_quick_start(self):
        messagebox.showinfo("Быстрый старт", 
                           "Руководство по быстрому старту:\n\n"
                           "1. Войдите в систему используя тестовые учетные данные\n"
                           "2. Используйте вкладки для навигации по модулям\n"
                           "3. Для администраторов доступно управление пользователями")
    
    def show_user_manual(self):
        messagebox.showinfo("Руководство пользователя", 
                           "Полное руководство пользователя АСУ ПСП 'Чистая Планета'\n\n"
                           "Модули системы:\n"
                           "- Управление партнерами: работа с клиентами и поставщиками\n"
                           "- Управление поставщиками: ведение базы поставщиков\n"
                           "- Управление поставками: отслеживание поставок материалов\n"
                           "- Калькулятор материалов: расчет потребности в материалах")
    
    def show_about(self):
        messagebox.showinfo("О программе", 
                           "АСУ ПСП 'Чистая Планета' v1.0\n\n"
                           "Автоматизированная система управления\n"
                           "производственно-сервисным предприятием\n\n"
                           "Разработчик: Команда 'Чистая Планета'")

class AuthSystem:
    """Система авторизации и управления пользователями"""
    
    def __init__(self):
        self.current_user = None
        self.current_role = None
        # Простые тестовые пользователи
        self.users = {
            'admin': {
                'password': self.hash_password('admin123'), 
                'full_name': 'Администратор Системы', 
                'role': 'admin'
            },
            'manager': {
                'password': self.hash_password('manager123'), 
                'full_name': 'Менеджер Производства', 
                'role': 'manager'
            },
            'ivanov': {
                'password': self.hash_password('ivanov123'), 
                'full_name': 'Иванов А.С.', 
                'role': 'manager'
            }
        }
    
    def hash_password(self, password):
        """Простое хеширование пароля"""
        return hashlib.sha256(password.encode('utf-8')).hexdigest()
    
    def authenticate(self, username, password):
        """Аутентификация пользователя"""
        if username in self.users:
            user = self.users[username]
            if user['password'] == self.hash_password(password):
                self.current_user = {
                    'username': username,
                    'full_name': user['full_name'],
                    'role': user['role']
                }
                self.current_role = user['role']
                return True
        return False
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
        self.current_role = None
    
    def has_permission(self, required_role):
        """Проверка прав доступа"""
        if not self.current_role:
            return False
        if required_role == 'admin':
            return self.current_role == 'admin'
        elif required_role == 'manager':
            return self.current_role in ['admin', 'manager']
        return False
    
    def get_user_display_name(self):
        """Получение отображаемого имени пользователя"""
        if self.current_user:
            return f"{self.current_user['full_name']} ({self.current_user['role']})"
        return "Не авторизован"

class CleanPlanetApp:
    def __init__(self, root):
        self.root = root
        self.root.title("АСУ ПСП «Чистая Планета» - Система управления предприятием")
        self.root.geometry("1200x700")
        self.root.configure(bg='white')
        
        # Цветовая схема
        self.colors = {
            'primary_bg': 'white',
            'secondary_bg': '#E0FFFF',
            'accent': '#00CED1',
            'text_dark': '#2F4F4F',
            'text_light': 'white',
            'border': '#B0E0E6'
        }
        
        # Инициализация системы авторизации
        self.auth_system = AuthSystem()
        
        # Инициализация системы справки
        self.help_system = HelpSystem(root)
        
        # Показываем окно авторизации
        self.show_login()
    
    def show_login(self):
        """Показать окно авторизации"""
        self.login_window = tk.Toplevel(self.root)
        self.login_window.title("АСУ ПСП «Чистая Планета» - Авторизация")
        self.login_window.geometry("400x350")
        self.login_window.configure(bg='white')
        self.login_window.resizable(False, False)
        self.login_window.transient(self.root)
        self.login_window.grab_set()
        
        # Центрирование окна
        self.login_window.update_idletasks()
        x = (self.login_window.winfo_screenwidth() - self.login_window.winfo_width()) // 2
        y = (self.login_window.winfo_screenheight() - self.login_window.winfo_height()) // 2
        self.login_window.geometry(f"+{x}+{y}")
        
        # Стили
        style = ttk.Style()
        style.configure("Login.TFrame", background='white')
        style.configure("Login.TLabel", background='white', foreground='#2F4F4F', font=('Arial', 10))
        style.configure("Login.TButton", font=('Arial', 10, 'bold'), padding=(10, 5))
        
        main_frame = ttk.Frame(self.login_window, style="Login.TFrame", padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, 
                               text="Авторизация в системе",
                               font=('Arial', 14, 'bold'),
                               foreground='#00CED1',
                               background='white')
        title_label.pack(pady=20)
        
        # Форма ввода
        form_frame = ttk.Frame(main_frame, style="Login.TFrame")
        form_frame.pack(pady=20)
        
        ttk.Label(form_frame, text="Логин:", style="Login.TLabel").grid(row=0, column=0, sticky=tk.W, pady=10, padx=5)
        self.username_entry = ttk.Entry(form_frame, width=20, font=('Arial', 10))
        self.username_entry.grid(row=0, column=1, pady=10, padx=5)
        self.username_entry.focus_set()
        
        ttk.Label(form_frame, text="Пароль:", style="Login.TLabel").grid(row=1, column=0, sticky=tk.W, pady=10, padx=5)
        self.password_entry = ttk.Entry(form_frame, width=20, show="*", font=('Arial', 10))
        self.password_entry.grid(row=1, column=1, pady=10, padx=5)
        
        # Кнопка входа
        ttk.Button(main_frame, text="Войти", 
                  command=self.authenticate,
                  style="Login.TButton").pack(pady=20)
        
        # Подсказка
        hint_frame = ttk.Frame(main_frame, style="Login.TFrame")
        hint_frame.pack(pady=10)
        
        hint_text = """Тестовые пользователи:
• admin / admin123
• manager / manager123  
• ivanov / ivanov123"""
        
        ttk.Label(hint_frame, 
                 text=hint_text,
                 style="Login.TLabel",
                 justify=tk.CENTER).pack()
        
        # Обработка нажатия Enter
        self.login_window.bind('<Return>', lambda event: self.authenticate())
        
        # Обработка закрытия окна
        self.login_window.protocol("WM_DELETE_WINDOW", self.root.quit)
    
    def authenticate(self):
        """Аутентификация пользователя"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль")
            return
        
        if self.auth_system.authenticate(username, password):
            self.login_window.destroy()
            self.on_login_success()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
            self.password_entry.delete(0, tk.END)
            self.username_entry.focus_set()
    
    def on_login_success(self):
        """Действия после успешной авторизации"""
        print(f"Пользователь {self.auth_system.get_user_display_name()} успешно авторизован")
        
        # Настройка стилей
        self.configure_styles()
        # Создание интерфейса
        self.create_interface()
        
        # Обновление заголовка с информацией о пользователе
        user_info = self.auth_system.get_user_display_name()
        self.root.title(f"АСУ ПСП «Чистая Планета» - {user_info}")
    
    def configure_styles(self):
        """Настройка стилей с новой цветовой схемой"""
        style = ttk.Style()
        
        # Настройка темы
        style.theme_use('clam')
        
        # Стиль для акцентных кнопок
        style.configure("Accent.TButton", 
                       font=("Arial", 10, "bold"),
                       padding=(10, 5),
                       background=self.colors['accent'],
                       foreground=self.colors['text_light'],
                       borderwidth=1,
                       focuscolor='none')
        
        style.map("Accent.TButton",
                 background=[('active', self.colors['accent']),
                           ('pressed', self.colors['accent'])],
                 foreground=[('active', self.colors['text_light']),
                           ('pressed', self.colors['text_light'])])
        
        # Стиль для обычных кнопок
        style.configure("TButton",
                       font=("Arial", 9),
                       padding=(8, 4),
                       background=self.colors['secondary_bg'],
                       foreground=self.colors['text_dark'],
                       borderwidth=1)
        
        style.map("TButton",
                 background=[('active', self.colors['accent']),
                           ('pressed', self.colors['accent'])],
                 foreground=[('active', self.colors['text_light']),
                           ('pressed', self.colors['text_light'])])
        
        # Стиль для заголовков
        style.configure("Title.TLabel",
                       font=("Arial", 14, "bold"),
                       foreground=self.colors['accent'],
                       background=self.colors['primary_bg'])
        
        # Стиль для обычных меток
        style.configure("TLabel",
                       font=("Arial", 9),
                       foreground=self.colors['text_dark'],
                       background=self.colors['primary_bg'])
        
        # Стиль для фреймов
        style.configure("TFrame",
                       background=self.colors['primary_bg'])
        
        style.configure("Secondary.TFrame",
                       background=self.colors['secondary_bg'])
        
        # Стиль для панели вкладок
        style.configure("TNotebook",
                       background=self.colors['primary_bg'],
                       borderwidth=0)
        
        style.configure("TNotebook.Tab",
                       font=("Arial", 10, "bold"),
                       padding=(15, 8),
                       background=self.colors['secondary_bg'],
                       foreground=self.colors['text_dark'])
        
        style.map("TNotebook.Tab",
                 background=[('selected', self.colors['accent']),
                           ('active', self.colors['accent'])],
                 foreground=[('selected', self.colors['text_light']),
                           ('active', self.colors['text_light'])])
        
        # Стиль для полей ввода
        style.configure("TEntry",
                       fieldbackground='white',
                       foreground=self.colors['text_dark'],
                       borderwidth=1,
                       relief='solid')
        
        # Стиль для выпадающих списков
        style.configure("TCombobox",
                       fieldbackground='white',
                       foreground=self.colors['text_dark'],
                       background=self.colors['primary_bg'])
        
        # Стиль для Treeview (таблиц)
        style.configure("Treeview",
                       background='white',
                       foreground=self.colors['text_dark'],
                       fieldbackground='white',
                       rowheight=25)
        
        style.configure("Treeview.Heading",
                       font=("Arial", 9, "bold"),
                       background=self.colors['accent'],
                       foreground=self.colors['text_light'],
                       relief='flat')
        
        style.map("Treeview.Heading",
                 background=[('active', self.colors['accent'])])
    
    def create_main_menu(self):
        """Создание главного меню программы с учетом ролей"""
        menubar = tk.Menu(self.root, 
                         bg=self.colors['primary_bg'],
                         fg=self.colors['text_dark'],
                         activebackground=self.colors['accent'],
                         activeforeground=self.colors['text_light'])
        self.root.config(menu=menubar)
        
        # Меню "Файл"
        file_menu = tk.Menu(menubar, tearoff=0,
                           bg=self.colors['primary_bg'],
                           fg=self.colors['text_dark'],
                           activebackground=self.colors['accent'],
                           activeforeground=self.colors['text_light'])
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Обновить данные", command=self.load_partners)
        
        # Только для администратора
        if self.auth_system.has_permission('admin'):
            file_menu.add_command(label="Управление пользователями", command=self.manage_users)
        
        file_menu.add_separator()
        file_menu.add_command(label="Сменить пользователя", command=self.logout)
        file_menu.add_command(label="Выход", command=self.root.quit)
        
        # Меню "Справка"
        help_menu = tk.Menu(menubar, tearoff=0,
                           bg=self.colors['primary_bg'],
                           fg=self.colors['text_dark'],
                           activebackground=self.colors['accent'],
                           activeforeground=self.colors['text_light'])
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="Быстрый старт", command=self.help_system.show_quick_start)
        help_menu.add_command(label="Руководство пользователя", command=self.help_system.show_user_manual)
        help_menu.add_separator()
        help_menu.add_command(label="О программе", command=self.help_system.show_about)
    
    def create_interface(self):
        """Создание основного интерфейса системы с учетом прав доступа"""
        # Создаем главное меню
        self.create_main_menu()
        
        # Главный фрейм
        main_frame = ttk.Frame(self.root, padding="10", style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок системы с информацией о пользователе
        user_info = self.auth_system.get_user_display_name()
        title_text = f"Автоматизированная система управления 'Чистая Планета' - {user_info}"
        title_label = ttk.Label(main_frame, 
                               text=title_text,
                               style="Title.TLabel")
        title_label.pack(pady=10)
        
        # Панель вкладок для модулей системы
        self.notebook = ttk.Notebook(main_frame, style="TNotebook")
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Вкладка управления партнерами (доступна всем)
        partners_frame = ttk.Frame(self.notebook, padding="10", style="Secondary.TFrame")
        self.notebook.add(partners_frame, text="Управление партнерами")
        
        # Вкладка управления поставщиками (доступна всем)
        suppliers_frame = ttk.Frame(self.notebook, padding="10", style="Secondary.TFrame")
        self.notebook.add(suppliers_frame, text="Управление поставщиками")
        
        # Вкладка управления поставками (доступна менеджерам и администраторам)
        if self.auth_system.has_permission('manager'):
            deliveries_frame = ttk.Frame(self.notebook, padding="10", style="Secondary.TFrame")
            self.notebook.add(deliveries_frame, text="Управление поставками")
        
        # Вкладка калькулятора материалов (доступна всем)
        calculator_frame = ttk.Frame(self.notebook, padding="10", style="Secondary.TFrame")
        self.notebook.add(calculator_frame, text="Калькулятор материалов")
        
        # Создание интерфейса для вкладок
        self.create_partners_interface(partners_frame)
        self.create_suppliers_interface(suppliers_frame)
        if self.auth_system.has_permission('manager'):
            self.create_deliveries_interface(deliveries_frame)
        self.create_calculator_interface(calculator_frame)
        
        # Статусная строка
        status_frame = ttk.Frame(main_frame, style="Secondary.TFrame")
        status_frame.pack(fill=tk.X, pady=5)
        
        self.status_label = ttk.Label(status_frame, 
                                     text=f"Система готова к работе. Пользователь: {user_info}", 
                                     relief=tk.SUNKEN,
                                     style="TLabel")
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Кнопка выхода
        ttk.Button(status_frame, text="Сменить пользователя", 
                  command=self.logout,
                  style="TButton").pack(side=tk.RIGHT, padx=5)
    
    def create_partners_interface(self, parent):
        """Создание интерфейса управления партнерами"""
        # Панель управления
        control_frame = ttk.Frame(parent, style="TFrame")
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(control_frame, text="Добавить партнера", 
                  command=self.add_partner,
                  style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Обновить список", 
                  command=self.load_partners,
                  style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="История услуг", 
                  command=self.show_history,
                  style="TButton").pack(side=tk.LEFT, padx=5)
        
        # Таблица партнеров
        table_frame = ttk.Frame(parent, style="TFrame")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ("ID", "Тип", "Название", "Телефон", "Email", "Рейтинг", "Статус")
        self.partners_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Настройка колонок
        column_widths = {"ID": 50, "Тип": 100, "Название": 200, "Телефон": 120, 
                        "Email": 200, "Рейтинг": 80, "Статус": 100}
        
        for col in columns:
            self.partners_tree.heading(col, text=col)
            self.partners_tree.column(col, width=column_widths.get(col, 100))
        
        self.partners_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.partners_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.partners_tree.configure(yscrollcommand=scrollbar.set)
        
        # Двойной клик для редактирования
        self.partners_tree.bind("<Double-1>", self.edit_partner)
    
    def create_suppliers_interface(self, parent):
        """Создание интерфейса управления поставщиками"""
        # Панель управления
        control_frame = ttk.Frame(parent, style="TFrame")
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(control_frame, text="Добавить поставщика", 
                  command=self.add_supplier,
                  style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Обновить список", 
                  command=self.load_suppliers,
                  style="TButton").pack(side=tk.LEFT, padx=5)
        
        # Дополнительные кнопки для поставщиков
        ttk.Button(control_frame, text="Просмотреть контакты", 
                  command=self.view_supplier_contacts,
                  style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Анализ поставщиков", 
                  command=self.analyze_suppliers,
                  style="TButton").pack(side=tk.LEFT, padx=5)
        
        # Таблица поставщиков
        table_frame = ttk.Frame(parent, style="TFrame")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ("ID", "Тип", "Название", "ИНН", "Контактное лицо", "Телефон", "Рейтинг")
        self.suppliers_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Настройка колонок
        column_widths = {"ID": 50, "Тип": 100, "Название": 200, "ИНН": 100, 
                        "Контактное лицо": 150, "Телефон": 120, "Рейтинг": 80}
        
        for col in columns:
            self.suppliers_tree.heading(col, text=col)
            self.suppliers_tree.column(col, width=column_widths.get(col, 100))
        
        self.suppliers_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.suppliers_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.suppliers_tree.configure(yscrollcommand=scrollbar.set)
        
        # Двойной клик для редактирования
        self.suppliers_tree.bind("<Double-1>", self.edit_supplier)
    
    def create_deliveries_interface(self, parent):
        """Создание интерфейса управления поставками"""
        # Панель управления
        control_frame = ttk.Frame(parent, style="TFrame")
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(control_frame, text="Добавить поставку", 
                  command=self.add_delivery,
                  style="Accent.TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Обновить список", 
                  command=self.load_deliveries,
                  style="TButton").pack(side=tk.LEFT, padx=5)
        
        # Дополнительные кнопки для поставок
        ttk.Button(control_frame, text="Отчет по поставкам", 
                  command=self.delivery_report,
                  style="TButton").pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Статус поставок", 
                  command=self.delivery_status,
                  style="TButton").pack(side=tk.LEFT, padx=5)
        
        # Таблица поставок
        table_frame = ttk.Frame(parent, style="TFrame")
        table_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        columns = ("ID", "Поставщик", "Сотрудник", "Услуга", "Размер материала", "Дата", "Статус")
        self.deliveries_tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=15)
        
        # Настройка колонок
        column_widths = {"ID": 50, "Поставщик": 150, "Сотрудник": 120, "Услуга": 150, 
                        "Размер материала": 120, "Дата": 100, "Статус": 100}
        
        for col in columns:
            self.deliveries_tree.heading(col, text=col)
            self.deliveries_tree.column(col, width=column_widths.get(col, 100))
        
        self.deliveries_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Полоса прокрутки
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.deliveries_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.deliveries_tree.configure(yscrollcommand=scrollbar.set)
        
        # Двойной клик для редактирования
        self.deliveries_tree.bind("<Double-1>", self.edit_delivery)
    
    def create_calculator_interface(self, parent):
        """Создание интерфейса калькулятора материалов"""
        # Заголовок
        ttk.Label(parent, 
                 text="Калькулятор расхода материалов для производственных услуг",
                 style="Title.TLabel").pack(pady=10)
        
        # Фрейм для ввода данных
        input_frame = ttk.LabelFrame(parent, text="Параметры расчета", padding="10", style="TFrame")
        input_frame.pack(fill=tk.X, pady=10)
        
        # Поля ввода
        self.calc_entries = {}
        fields = [
            ("Тип услуги (ID):", "service_type"),
            ("Тип материала (ID):", "material_type"), 
            ("Количество услуг:", "quantity"),
            ("Параметр услуги:", "service_param"),
            ("Коэффициент расхода:", "service_coef"),
            ("Процент перерасхода:", "waste_percent")
        ]
        
        for i, (label, key) in enumerate(fields):
            ttk.Label(input_frame, text=label, style="TLabel").grid(row=i, column=0, sticky=tk.W, pady=5, padx=5)
            entry = ttk.Entry(input_frame, width=20, style="TEntry")
            entry.grid(row=i, column=1, pady=5, padx=5)
            self.calc_entries[key] = entry
        
        # Значения по умолчанию
        self.calc_entries["service_type"].insert(0, "1")
        self.calc_entries["material_type"].insert(0, "1")
        self.calc_entries["quantity"].insert(0, "10")
        self.calc_entries["service_param"].insert(0, "5")
        self.calc_entries["service_coef"].insert(0, "1.0")
        self.calc_entries["waste_percent"].insert(0, "10.0")
        
        # Кнопка расчета
        ttk.Button(input_frame, text="Рассчитать потребность", 
                  command=self.calculate_materials,
                  style="Accent.TButton").grid(row=len(fields), column=0, columnspan=2, pady=10)
        
        # Поле результата
        result_frame = ttk.LabelFrame(parent, text="Результат расчета", padding="10", style="TFrame")
        result_frame.pack(fill=tk.X, pady=10)
        
        self.result_var = tk.StringVar()
        self.result_var.set("Введите параметры и нажмите 'Рассчитать'")
        result_label = ttk.Label(result_frame, textvariable=self.result_var, 
                               font=("Arial", 10, "bold"), 
                               foreground=self.colors['accent'],
                               background=self.colors['secondary_bg'])
        result_label.pack(pady=5)
    
    def load_partners(self):
        """Загрузка списка партнеров"""
        # Очистка таблицы
        for item in self.partners_tree.get_children():
            self.partners_tree.delete(item)
        
        # Тестовые данные
        test_data = [
            (1, "Поставщик", "ООО Химреактивы", "+7-999-111-22-33", "chem@reagents.ru", 8, "Активен"),
            (2, "Пункт приема", "Чистый Город", "+7-999-222-33-44", "clean@city.ru", 9, "Активен"),
            (3, "Агрегатор", "ЭкоСервис", "+7-999-333-44-55", "eco@service.ru", 7, "Неактивен"),
            (4, "Поставщик", "ТекстильПром", "+7-999-444-55-66", "textile@prom.ru", 6, "Активен")
        ]
        
        for data in test_data:
            self.partners_tree.insert("", tk.END, values=data)
        
        self.status_label.config(text="Партнеры загружены")
    
    def load_suppliers(self):
        """Загрузка списка поставщиков"""
        # Очистка таблицы
        for item in self.suppliers_tree.get_children():
            self.suppliers_tree.delete(item)
        
        # Тестовые данные
        test_data = [
            (1, "Химия", "ООО Химреактивы", "7701234567", "Смирнов А.В.", "+7-495-111-22-33", 8),
            (2, "Ткани", "Фабрика ТекстильПроф", "7701234568", "Орлова Е.П.", "+7-4932-444-55-66", 9),
            (3, "Оборудование", "Завод ЧистыеТехнологии", "7701234569", "Колесников С.М.", "+7-812-777-88-99", 7),
            (4, "Упаковка", "ПакетСервис", "7701234570", "Волков П.С.", "+7-495-999-00-11", 8)
        ]
        
        for data in test_data:
            self.suppliers_tree.insert("", tk.END, values=data)
        
        self.status_label.config(text="Поставщики загружены")
    
    def load_deliveries(self):
        """Загрузка списка поставок"""
        # Очистка таблицы
        for item in self.deliveries_tree.get_children():
            self.deliveries_tree.delete(item)
        
        # Тестовые данные
        test_data = [
            (1, "ООО Химреактивы", "Анна Иванова", "Химчистка", "50 кг", "2024-01-15", "доставлено"),
            (2, "Фабрика ТекстильПроф", "Дмитрий Петров", "Стирка белья", "100 литров", "2024-01-20", "в пути"),
            (3, "Завод ЧистыеТехнологии", "Ольга Сидорова", "Ремонт оборудования", "200 метров", "2024-01-25", "ожидает"),
            (4, "ПакетСервис", "Анна Иванова", "Упаковка", "500 шт", "2024-01-30", "доставлено")
        ]
        
        for data in test_data:
            self.deliveries_tree.insert("", tk.END, values=data)
        
        self.status_label.config(text="Поставки загружены")
    
    def add_partner(self):
        """Добавление нового партнера"""
        self.show_partner_dialog()
    
    def add_supplier(self):
        """Добавление нового поставщика"""
        self.show_supplier_dialog()
    
    def add_delivery(self):
        """Добавление новой поставки"""
        self.show_delivery_dialog()
    
    def edit_partner(self, event=None):
        """Редактирование выбранного партнера"""
        selection = self.partners_tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите партнера для редактирования")
            return
        
        partner_data = self.partners_tree.item(selection[0])['values']
        messagebox.showinfo("Редактирование", f"Редактирование партнера: {partner_data[2]}\n\nID: {partner_data[0]}")
    
    def edit_supplier(self, event=None):
        """Редактирование выбранного поставщика"""
        selection = self.suppliers_tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите поставщика для редактирования")
            return
        
        supplier_data = self.suppliers_tree.item(selection[0])['values']
        messagebox.showinfo("Редактирование", f"Редактирование поставщика: {supplier_data[2]}\n\nID: {supplier_data[0]}")
    
    def edit_delivery(self, event=None):
        """Редактирование выбранной поставки"""
        selection = self.deliveries_tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите поставку для редактирования")
            return
        
        delivery_data = self.deliveries_tree.item(selection[0])['values']
        messagebox.showinfo("Редактирование", f"Редактирование поставки: {delivery_data[0]}\n\nПоставщик: {delivery_data[1]}")
    
    def show_history(self, event=None):
        """Показать историю услуг для выбранного партнера"""
        selection = self.partners_tree.selection()
        if not selection:
            messagebox.showwarning("Внимание", "Выберите партнера из таблицы")
            return
        
        partner_data = self.partners_tree.item(selection[0])['values']
        messagebox.showinfo("История услуг", f"История услуг для: {partner_data[2]}\n\nЗдесь будет отображаться история заказов и услуг")
    
    def view_supplier_contacts(self):
        """Просмотр контактов поставщиков"""
        messagebox.showinfo("Контакты поставщиков", "Здесь будет отображаться подробная контактная информация поставщиков")
    
    def analyze_suppliers(self):
        """Анализ поставщиков"""
        messagebox.showinfo("Анализ поставщиков", "Здесь будет аналитика по поставщикам: рейтинги, надежность, сроки поставок")
    
    def delivery_report(self):
        """Отчет по поставкам"""
        messagebox.showinfo("Отчет по поставкам", "Здесь будет формироваться отчет по поставкам за выбранный период")
    
    def delivery_status(self):
        """Статус поставок"""
        messagebox.showinfo("Статус поставок", "Здесь будет отображаться текущий статус всех активных поставок")
    
    def calculate_materials(self):
        """Расчет потребности в материалах"""
        try:
            # Получение данных из полей ввода
            service_id = int(self.calc_entries["service_type"].get())
            material_id = int(self.calc_entries["material_type"].get())
            quantity = int(self.calc_entries["quantity"].get())
            param = float(self.calc_entries["service_param"].get())
            coef = float(self.calc_entries["service_coef"].get())
            waste = float(self.calc_entries["waste_percent"].get())
            
            # Расчет
            calculator = MaterialCalculator()
            result = calculator.calculate_material_required(
                service_id, material_id, quantity, param, coef, waste
            )
            
            if result == -1:
                self.result_var.set("Ошибка: Проверьте корректность введенных данных")
            else:
                self.result_var.set(f"Результат: необходимо {result} единиц материала")
                
        except ValueError as e:
            messagebox.showerror("Ошибка ввода", "Проверьте правильность числовых значений")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка при расчете:\n{str(e)}")
    
    def manage_users(self):
        """Управление пользователями (только для администратора)"""
        if not self.auth_system.has_permission('admin'):
            messagebox.showwarning("Доступ запрещен", "Эта функция доступна только администраторам")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("Управление пользователями")
        dialog.geometry("600x400")
        dialog.configure(bg=self.colors['primary_bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding="15", style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, 
                 text="Управление пользователями системы",
                 style="Title.TLabel").pack(pady=10)
        
        # Таблица пользователей
        columns = ("Логин", "ФИО", "Роль", "Статус")
        users_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            users_tree.heading(col, text=col)
            users_tree.column(col, width=120)
        
        users_tree.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Загрузка пользователей
        for username, user_data in self.auth_system.users.items():
            status = "Активен"
            users_tree.insert("", tk.END, values=(
                username, 
                user_data['full_name'], 
                user_data['role'], 
                status
            ))
        
        # Кнопки управления
        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Закрыть", 
                  command=dialog.destroy,
                  style="TButton").pack(side=tk.LEFT, padx=5)
    
    def show_partner_dialog(self):
        """Диалог добавления партнера"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление нового партнера")
        dialog.geometry("500x500")
        dialog.configure(bg=self.colors['primary_bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding="15", style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, 
                 text="Добавление нового партнера",
                 style="Title.TLabel").pack(pady=10)
        
        # Поля формы
        fields = [
            ("Тип партнера:*", "partner_type"),
            ("Название:*", "name"),
            ("Телефон:*", "phone"),
            ("Email:", "email"),
            ("Рейтинг (0-10):*", "rating")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(main_frame, text=label, style="TLabel").pack(anchor=tk.W, pady=5)
            
            if key == "partner_type":
                entry = ttk.Combobox(main_frame, values=["Пункт приема", "Поставщик", "Агрегатор"], width=50)
                entry.set("Поставщик")
            else:
                entry = ttk.Entry(main_frame, width=50)
                
            entry.pack(pady=5, fill=tk.X)
            entries[key] = entry
        
        # Значения по умолчанию
        entries["rating"].insert(0, "5")
        
        def save_partner():
            """Сохранение партнера"""
            # Простая валидация
            if not entries["name"].get().strip():
                messagebox.showerror("Ошибка", "Введите название партнера")
                return
            
            messagebox.showinfo("Успех", "Партнер успешно добавлен!")
            dialog.destroy()
            self.load_partners()  # Обновляем список
        
        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Добавить партнера", 
                  command=save_partner,
                  style="Accent.TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Отмена", 
                  command=dialog.destroy,
                  style="TButton").pack(side=tk.LEFT, padx=10)
    
    def show_supplier_dialog(self):
        """Диалог добавления поставщика"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление нового поставщика")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['primary_bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding="15", style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, 
                 text="Добавление нового поставщика",
                 style="Title.TLabel").pack(pady=10)
        
        # Поля формы
        fields = [
            ("Тип поставщика:*", "supplier_type"),
            ("Название:*", "name"),
            ("Контактное лицо:", "contact_person"),
            ("Телефон:*", "phone"),
            ("Рейтинг (0-10):", "rating")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(main_frame, text=label, style="TLabel").pack(anchor=tk.W, pady=5)
            entry = ttk.Entry(main_frame, width=50)
            entry.pack(pady=5, fill=tk.X)
            entries[key] = entry
        
        # Значения по умолчанию
        entries["rating"].insert(0, "5")
        
        def save_supplier():
            """Сохранение поставщика"""
            if not entries["name"].get().strip():
                messagebox.showerror("Ошибка", "Введите название поставщика")
                return
            
            messagebox.showinfo("Успех", "Поставщик успешно добавлен!")
            dialog.destroy()
            self.load_suppliers()
        
        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Добавить поставщика", 
                  command=save_supplier,
                  style="Accent.TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Отмена", 
                  command=dialog.destroy,
                  style="TButton").pack(side=tk.LEFT, padx=10)
    
    def show_delivery_dialog(self):
        """Диалог добавления поставки"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Добавление новой поставки")
        dialog.geometry("500x400")
        dialog.configure(bg=self.colors['primary_bg'])
        dialog.transient(self.root)
        dialog.grab_set()
        
        main_frame = ttk.Frame(dialog, padding="15", style="TFrame")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, 
                 text="Добавление новой поставки",
                 style="Title.TLabel").pack(pady=10)
        
        # Поля формы
        fields = [
            ("Поставщик:*", "supplier"),
            ("Материал:*", "material"),
            ("Количество:*", "quantity"),
            ("Дата поставки:", "delivery_date"),
            ("Статус:", "status")
        ]
        
        entries = {}
        for i, (label, key) in enumerate(fields):
            ttk.Label(main_frame, text=label, style="TLabel").pack(anchor=tk.W, pady=5)
            
            if key == "status":
                entry = ttk.Combobox(main_frame, values=["ожидает", "в пути", "доставлено", "отменено"], width=50)
                entry.set("ожидает")
            else:
                entry = ttk.Entry(main_frame, width=50)
                
            entry.pack(pady=5, fill=tk.X)
            entries[key] = entry
        
        # Значения по умолчанию
        entries["delivery_date"].insert(0, "2024-01-01")
        
        def save_delivery():
            """Сохранение поставки"""
            if not entries["supplier"].get().strip():
                messagebox.showerror("Ошибка", "Введите поставщика")
                return
            
            messagebox.showinfo("Успех", "Поставка успешно добавлена!")
            dialog.destroy()
            self.load_deliveries()
        
        button_frame = ttk.Frame(main_frame, style="TFrame")
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Добавить поставку", 
                  command=save_delivery,
                  style="Accent.TButton").pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="Отмена", 
                  command=dialog.destroy,
                  style="TButton").pack(side=tk.LEFT, padx=10)
    
    def logout(self):
        """Выход из системы и возврат к окну авторизации"""
        # Закрываем все дочерние окна
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Выход из системы
        self.auth_system.logout()
        
        # Показываем окно авторизации
        self.show_login()

# Запуск приложения
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = CleanPlanetApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Критическая ошибка при запуске: {e}")
        import traceback
        traceback.print_exc()
        input("Нажмите Enter для выхода...")