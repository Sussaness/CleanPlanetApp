"""
Модуль системы справки и документации для АСУ ПСП «Чистая Планета»
"""

import tkinter as tk
from tkinter import ttk, scrolledtext
import webbrowser

class HelpSystem:
    def __init__(self, parent):
        self.parent = parent
    
    def show_about(self):
        """Окно 'О программе'"""
        about_window = tk.Toplevel(self.parent)
        about_window.title("О программе")
        about_window.geometry("600x500")
        about_window.resizable(False, False)
        about_window.transient(self.parent)
        about_window.grab_set()
        
        # Главный фрейм
        main_frame = ttk.Frame(about_window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Заголовок
        title_label = ttk.Label(main_frame, 
                               text="АСУ ПСП «Чистая Планета»",
                               font=("Arial", 16, "bold"),
                               foreground="darkblue")
        title_label.pack(pady=10)
        
        # Версия
        version_label = ttk.Label(main_frame,
                                 text="Версия 1.0",
                                 font=("Arial", 10, "italic"))
        version_label.pack(pady=5)
        
        # Информация о программе
        info_text = """
Автоматизированная система управления 
производственно-сервисным предприятием

Функциональные модули:
• Управление партнерами (пункты приема, поставщики, агрегаторы)
• Обработка заказов и история услуг  
• Калькулятор потребности в материалах
• Управление производственными процессами

Технические характеристики:
• Python 3.9+ с фреймворком Tkinter
• PostgreSQL 12+ для хранения данных
• Кроссплатформенная архитектура
• Валидация данных и обработка ошибок

Разработано в соответствии с ТЗ учебной практики
ФГАОУ ВО «СПбПУ» Института среднего профессионального образования

© 2024 Все права защищены
"""
        
        info_area = scrolledtext.ScrolledText(main_frame, 
                                            width=60, 
                                            height=20,
                                            font=("Arial", 9),
                                            wrap=tk.WORD)
        info_area.pack(pady=10, fill=tk.BOTH, expand=True)
        info_area.insert(tk.END, info_text)
        info_area.config(state=tk.DISABLED)
        
        # Кнопка закрытия
        ttk.Button(main_frame, 
                  text="Закрыть", 
                  command=about_window.destroy).pack(pady=10)
    
    def show_user_manual(self):
        """Руководство пользователя"""
        manual_window = tk.Toplevel(self.parent)
        manual_window.title("Руководство пользователя")
        manual_window.geometry("700x600")
        manual_window.transient(self.parent)
        
        # Панель вкладок
        notebook = ttk.Notebook(manual_window)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Вкладка общего руководства
        general_frame = ttk.Frame(notebook, padding="10")
        notebook.add(general_frame, text="Общее руководство")
        
        general_text = """
РАБОТА С СИСТЕМОЙ «ЧИСТАЯ ПЛАНЕТА»

1. ГЛАВНОЕ ОКНО ПРОГРАММЫ
   • Программа запускается с главного окна, содержащего две основные вкладки
   • Вкладка "Управление партнерами" - для работы с контрагентами
   • Вкладка "Калькулятор материалов" - для производственных расчетов

2. УПРАВЛЕНИЕ ПАРТНЕРАМИ
   • Просмотр списка всех партнеров в таблице
   • Добавление новых партнеров через кнопку "Добавить партнера"
   • Просмотр истории услуг по двойному клику на партнере
   • Обновление данных кнопкой "Обновить список"

3. РАБОТА С КАЛЬКУЛЯТОРОМ
   • Расчет потребности в материалах для услуг
   • Ввод параметров услуги и материалов
   • Автоматический учет технологического перерасхода
   • Получение точного количества необходимых материалов

4. НАВИГАЦИЯ
   • Используйте мышь для выбора элементов
   • Tab - переход между полями ввода
   • Enter - подтверждение ввода в формах
"""
        
        general_area = scrolledtext.ScrolledText(general_frame, 
                                               width=80, 
                                               height=25,
                                               font=("Arial", 9),
                                               wrap=tk.WORD)
        general_area.pack(fill=tk.BOTH, expand=True)
        general_area.insert(tk.END, general_text)
        general_area.config(state=tk.DISABLED)
        
        # Вкладка модуля 4
        module4_frame = ttk.Frame(notebook, padding="10")
        notebook.add(module4_frame, text="Модуль 4: Калькулятор")
        
        module4_text = """
МОДУЛЬ 4: КАЛЬКУЛЯТОР МАТЕРИАЛОВ

НАЗНАЧЕНИЕ:
   Расчет потребности в материалах для производственных услуг 
   с учетом технологических особенностей и перерасхода.

ПАРАМЕТРЫ РАСЧЕТА:

1. Тип услуги (ID) - идентификатор вида услуги:
   • 1 - Стирка
   • 2 - Химчистка  
   • 3 - Ремонт
   • 4 - Глажка
   • 5 - Дополнительные услуги

2. Тип материала (ID) - идентификатор материала:
   • 1 - Стиральный порошок
   • 2 - Кондиционер
   • 3 - Отбеливатель
   • 4 - Растворитель химчистки
   • 5 - Клей для ткани
   • 6 - Нитки
   • 7 - Пуговицы
   • 8 - Молнии
   • 9 - Упаковочные материалы

3. Количество услуг - число идентичных услуг для расчета

4. Параметр услуги - основной измеримый параметр:
   • Для стирки - вес белья в кг
   • Для химчистки - площадь обработки
   • Для ремонта - количество операций

5. Коэффициент расхода - норма расхода материала на единицу параметра

6. Перерасход % - технологические потери (обычно 5-15%)

ПРИМЕР РАСЧЕТА:
   Услуга: Стирка постельного белья (ID: 1)
   Материал: Порошок (ID: 1)
   Количество: 10 услуг
   Параметр: 5.0 кг на услугу
   Коэффициент: 0.15 кг порошка на кг белья
   Перерасход: 10%

   Расчет: 10 × 5.0 × 0.15 × 1.10 = 8.25 → 8 единиц

ФОРМУЛА:
   Результат = ceil(Количество × Параметр × Коэффициент × (1 + Перерасход/100))

ВОЗВРАЩАЕМЫЕ ЗНАЧЕНИЯ:
   • Положительное число - количество материала
   • -1 - ошибка валидации входных данных
"""
        
        module4_area = scrolledtext.ScrolledText(module4_frame, 
                                               width=80, 
                                               height=25,
                                               font=("Arial", 9),
                                               wrap=tk.WORD)
        module4_area.pack(fill=tk.BOTH, expand=True)
        module4_area.insert(tk.END, module4_text)
        module4_area.config(state=tk.DISABLED)
        
        # Вкладка технической документации
        tech_frame = ttk.Frame(notebook, padding="10")
        notebook.add(tech_frame, text="Техническая документация")
        
        tech_text = """
ТЕХНИЧЕСКАЯ ДОКУМЕНТАЦИЯ

АРХИТЕКТУРА СИСТЕМЫ:

1. КЛИЕНТСКАЯ ЧАСТЬ:
   • Графический интерфейс: Tkinter
   • Язык программирования: Python 3.9+
   • Платформа: Windows/Linux/macOS

2. СЕРВЕРНАЯ ЧАСТЬ:
   • Система управления базами данных: PostgreSQL 12+
   • Хостинг: локальный сервер

3. СТРУКТУРА БАЗЫ ДАННЫХ:

   ТАБЛИЦА partners:
   • partner_id (SERIAL PRIMARY KEY)
   • partner_type (VARCHAR) - тип партнера
   • name (VARCHAR) - название
   • phone (VARCHAR) - телефон
   • email (VARCHAR) - электронная почта
   • rating (DECIMAL) - рейтинг
   • is_active (BOOLEAN) - статус активности

   ТАБЛИЦА services:
   • service_id (SERIAL PRIMARY KEY) 
   • name (VARCHAR) - название услуги
   • description (TEXT) - описание
   • base_price (DECIMAL) - базовая цена
   • category (VARCHAR) - категория

   ТАБЛИЦА orders:
   • order_id (SERIAL PRIMARY KEY)
   • partner_id (INTEGER) - ссылка на партнера
   • order_date (TIMESTAMP) - дата заказа
   • status (VARCHAR) - статус заказа
   • total_amount (DECIMAL) - общая сумма
   • prepayment (DECIMAL) - предоплата

   ТАБЛИЦА order_services:
   • order_service_id (SERIAL PRIMARY KEY)
   • order_id (INTEGER) - ссылка на заказ
   • service_id (INTEGER) - ссылка на услугу
   • quantity (INTEGER) - количество
   • agreed_price (DECIMAL) - согласованная цена

ТРЕБОВАНИЯ К СИСТЕМЕ:

Минимальные требования:
   • Процессор: Intel Core i3 или аналогичный
   • Память: 4 ГБ ОЗУ
   • Дисковое пространство: 500 МБ
   • PostgreSQL 12+

Рекомендуемые требования:
   • Процессор: Intel Core i5 или лучше
   • Память: 8 ГБ ОЗУ  
   • Дисковое пространство: 1 ГБ
   • PostgreSQL 13+

ЛОГИРОВАНИЕ И ОТЛАДКА:
   • Все операции логируются в консоль
   • Ошибки отображаются в диалоговых окнах
   • Валидация данных на стороне клиента и сервера
"""
        
        tech_area = scrolledtext.ScrolledText(tech_frame, 
                                            width=80, 
                                            height=25,
                                            font=("Arial", 9),
                                            wrap=tk.WORD)
        tech_area.pack(fill=tk.BOTH, expand=True)
        tech_area.insert(tk.END, tech_text)
        tech_area.config(state=tk.DISABLED)
    
    def show_quick_start(self):
        """Быстрый старт"""
        quick_window = tk.Toplevel(self.parent)
        quick_window.title("Быстрый старт")
        quick_window.geometry("500x400")
        quick_window.resizable(False, False)
        
        main_frame = ttk.Frame(quick_window, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, 
                 text="Быстрый старт - начало работы",
                 font=("Arial", 12, "bold")).pack(pady=10)
        
        steps_text = """
ШАГ 1: ДОБАВЛЕНИЕ ПАРТНЕРА
   1. Перейдите на вкладку "Управление партнерами"
   2. Нажмите кнопку "Добавить партнера"
   3. Заполните обязательные поля:
      - Тип партнера (выберите из списка)
      - Название организации
      - Телефон (в формате +7-XXX-XXX-XX-XX)
      - Рейтинг (число от 0 до 10)
   4. Нажмите "Добавить партнера"

ШАГ 2: РАБОТА С КАЛЬКУЛЯТОРОМ
   1. Перейдите на вкладку "Калькулятор материалов"
   2. Введите параметры для расчета:
      - ID услуги и материала
      - Количество услуг
      - Параметр услуги (вес, объем и т.д.)
      - Коэффициент расхода
      - Процент перерасхода
   3. Нажмите "Рассчитать потребность"

ШАГ 3: ПРОСМОТР ИСТОРИИ
   1. Выберите партнера в таблице
   2. Нажмите "История услуг"
   3. Просмотрите историю заказов

СОВЕТЫ:
   • Email не является обязательным полем
   • Рейтинг влияет на приоритет в отчетах
   • Для тестирования используйте ID от 1 до 10
   • Стандартный перерасход - 10-15%
"""
        
        text_area = scrolledtext.ScrolledText(main_frame, 
                                            width=60, 
                                            height=20,
                                            font=("Arial", 9),
                                            wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True)
        text_area.insert(tk.END, steps_text)
        text_area.config(state=tk.DISABLED)
        
        ttk.Button(main_frame, 
                  text="Закрыть", 
                  command=quick_window.destroy).pack(pady=10)