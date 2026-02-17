"""
Модуль аутентификации и авторизации для АСУ ПСП «Чистая Планета»
"""

import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
import hashlib
import binascii
import os

class AuthSystem:
    def __init__(self, db_connection):
        self.conn = db_connection
        self.cursor = self.conn.cursor()
        self.current_user = None
        self.current_role = None
    
    def hash_password(self, password):
        """Хеширование пароля"""
        salt = hashlib.sha256(os.urandom(60)).hexdigest().encode('ascii')
        pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
        pwdhash = binascii.hexlify(pwdhash)
        return (salt + pwdhash).decode('ascii')
    
    def verify_password(self, stored_password, provided_password):
        """Проверка пароля"""
        salt = stored_password[:64]
        stored_password = stored_password[64:]
        pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), salt.encode('ascii'), 100000)
        pwdhash = binascii.hexlify(pwdhash).decode('ascii')
        return pwdhash == stored_password
    
    def login(self, username, password):
        """Аутентификация пользователя"""
        try:
            self.cursor.execute("""
                SELECT user_id, username, password_hash, full_name, role 
                FROM users 
                WHERE username = %s AND is_active = true
            """, (username,))
            
            user = self.cursor.fetchone()
            
            if user and self.verify_password(user[2], password):
                self.current_user = {
                    'user_id': user[0],
                    'username': user[1],
                    'full_name': user[3],
                    'role': user[4]
                }
                self.current_role = user[4]
                
                # Обновляем время последнего входа
                self.cursor.execute("""
                    UPDATE users SET last_login = CURRENT_TIMESTAMP 
                    WHERE user_id = %s
                """, (user[0],))
                self.conn.commit()
                
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Ошибка при аутентификации: {e}")
            return False
    
    def check_permission(self, module, action):
        """Проверка прав доступа"""
        if not self.current_role:
            return False
            
        try:
            self.cursor.execute("""
                SELECT can_view, can_create, can_edit, can_delete 
                FROM role_permissions 
                WHERE role = %s AND module = %s
            """, (self.current_role, module))
            
            permission = self.cursor.fetchone()
            
            if not permission:
                return False
            
            # Сопоставление действий с полями разрешений
            action_mapping = {
                'view': permission[0],
                'create': permission[1],
                'edit': permission[2],
                'delete': permission[3]
            }
            
            return action_mapping.get(action, False)
            
        except Exception as e:
            print(f"Ошибка при проверке прав: {e}")
            return False
    
    def get_user_display_name(self):
        """Получение отображаемого имени пользователя"""
        if self.current_user:
            role_display = "Администратор" if self.current_role == 'admin' else "Менеджер"
            return f"{self.current_user['full_name']} ({role_display})"
        return "Неавторизованный пользователь"
    
    def logout(self):
        """Выход из системы"""
        self.current_user = None
        self.current_role = None

class LoginWindow:
    def __init__(self, parent, auth_system, on_success_callback):
        self.parent = parent
        self.auth_system = auth_system
        self.on_success_callback = on_success_callback
        
        self.create_login_window()
    
    def create_login_window(self):
        """Создание окна входа"""
        self.login_window = tk.Toplevel(self.parent)
        self.login_window.title("АСУ ПСП «Чистая Планета» - Вход в систему")
        self.login_window.geometry("400x300")
        self.login_window.resizable(False, False)
        self.login_window.configure(bg='white')
        self.login_window.transient(self.parent)
        self.login_window.grab_set()
        
        # Центрирование окна
        self.login_window.update_idletasks()
        x = (self.login_window.winfo_screenwidth() - self.login_window.winfo_width()) // 2
        y = (self.login_window.winfo_screenheight() - self.login_window.winfo_height()) // 2
        self.login_window.geometry(f"+{x}+{y}")
        
        # Стили
        style = ttk.Style()
        style.configure("Login.TFrame", background='white')
        style.configure("Login.TLabel", background='white', font=('Arial', 10))
        style.configure("Login.TButton", font=('Arial', 10, 'bold'), padding=(10, 5))
        
        # Главный фрейм
        main_frame = ttk.Frame(self.login_window, style="Login.TFrame", padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, 
                               text="Вход в систему",
                               font=('Arial', 16, 'bold'),
                               background='white',
                               foreground='#00CED1')
        title_label.pack(pady=20)
        
        # Фрейм формы
        form_frame = ttk.Frame(main_frame, style="Login.TFrame")
        form_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Поле логина
        ttk.Label(form_frame, text="Логин:", style="Login.TLabel").grid(row=0, column=0, sticky=tk.W, pady=10, padx=5)
        self.username_entry = ttk.Entry(form_frame, width=25, font=('Arial', 10))
        self.username_entry.grid(row=0, column=1, pady=10, padx=5, sticky=tk.EW)
        
        # Поле пароля
        ttk.Label(form_frame, text="Пароль:", style="Login.TLabel").grid(row=1, column=0, sticky=tk.W, pady=10, padx=5)
        self.password_entry = ttk.Entry(form_frame, width=25, show="*", font=('Arial', 10))
        self.password_entry.grid(row=1, column=1, pady=10, padx=5, sticky=tk.EW)
        
        # Кнопка входа
        button_frame = ttk.Frame(form_frame, style="Login.TFrame")
        button_frame.grid(row=2, column=0, columnspan=2, pady=20)
        
        ttk.Button(button_frame, text="Войти", 
                  command=self.attempt_login,
                  style="Login.TButton").pack(side=tk.LEFT, padx=10)
        
        ttk.Button(button_frame, text="Отмена", 
                  command=self.login_window.destroy).pack(side=tk.LEFT, padx=10)
        
        # Тестовые данные
        test_data_frame = ttk.Frame(main_frame, style="Login.TFrame")
        test_data_frame.pack(fill=tk.X, pady=10)
        
        test_info = "Тестовые данные:\nАдминистратор - admin/admin123\nМенеджер - manager/manager123"
        test_label = ttk.Label(test_data_frame, 
                              text=test_info,
                              style="Login.TLabel",
                              justify=tk.LEFT,
                              foreground='#666666')
        test_label.pack()
        
        # Настройка фокуса и привязка Enter
        self.username_entry.focus_set()
        self.login_window.bind('<Return>', lambda e: self.attempt_login())
        
        # Центрирование колонок
        form_frame.columnconfigure(1, weight=1)
    
    def attempt_login(self):
        """Попытка входа в систему"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Ошибка", "Введите логин и пароль")
            return
        
        if self.auth_system.login(username, password):
            messagebox.showinfo("Успех", f"Добро пожаловать, {self.auth_system.get_user_display_name()}!")
            self.login_window.destroy()
            self.on_success_callback()
        else:
            messagebox.showerror("Ошибка", "Неверный логин или пароль")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus_set()