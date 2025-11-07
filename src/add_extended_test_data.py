"""
Скрипт для добавления расширенных тестовых данных в базу данных АСУ ПСП «Чистая Планета»
"""

import psycopg2
from datetime import datetime, timedelta
import random

def add_extended_test_data():
    """Добавление расширенных тестовых данных"""
    try:
        conn = psycopg2.connect(
            dbname="lean_planet_enterprise",
            user="postgres",
            password="postgres",  # Замените на ваш пароль
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()
        
        print("Добавление расширенных тестовых данных...")
        
        # 1. Добавление дополнительных услуг
        additional_services = [
            ('Ремонт пуховика', 'Починка и восстановление пуховиков', 800.00, 'ремонт'),
            ('Чистка дубленки', 'Специальная чистка дубленок и овчин', 1500.00, 'химчистка'),
            ('Стирка штор', 'Стирка и глажка оконных штор', 600.00, 'стирка'),
            ('Отпаривание костюма', 'Профессиональное отпаривание костюмов', 400.00, 'глажка'),
            ('Чистка кожаной куртки', 'Специальная чистка кожаных изделий', 1200.00, 'химчистка'),
            ('Ремонт подкладки', 'Замена и починка подкладки', 450.00, 'ремонт'),
            ('Стирка пухового одеяла', 'Стирка объемных пуховых изделий', 900.00, 'стирка'),
            ('Чистка пальто', 'Химчистка шерстяных пальто', 1100.00, 'химчистка'),
            ('Услуга вызова курьера', 'Вызов курьера для забора/доставки', 200.00, 'дополнительно'),
            ('Упаковка одежды', 'Фирменная упаковка очищенной одежды', 100.00, 'дополнительно')
        ]
        
        for service in additional_services:
            cursor.execute("""
                INSERT INTO services (name, description, base_price, category)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, service)
        
        print(f"Добавлено {len(additional_services)} дополнительных услуг")
        
        # 2. Добавление дополнительных партнеров
        additional_partners = [
            ('Пункт приема', 'Филиал Южный', '+7-999-666-66-66', 'south@cleanplanet.ru', 8.8),
            ('Пункт приема', 'Филиал Западный', '+7-999-777-77-77', 'west@cleanplanet.ru', 8.2),
            ('Пункт приема', 'Филиал Восточный', '+7-999-888-88-88', 'east@cleanplanet.ru', 8.5),
            ('Агрегатор', 'Сервис "БыстраяЧистка"', '+7-999-999-99-99', 'fast@clean.ru', 7.8),
            ('Агрегатор', 'Платформа "ЧистоOnline"', '+7-999-000-00-00', 'online@clean.ru', 8.9),
            ('Поставщик', 'ООО "СпецХимСнаб"', '+7-999-121-21-21', 'spec@chemicals.ru', 8.3),
            ('Поставщик', 'Компания "ПрофОборудование"', '+7-999-131-31-31', 'pro@equipment.ru', 9.2),
            ('Поставщик', 'Фирма "КачественнаяУпаковка"', '+7-999-141-41-41', 'pack@quality.ru', 7.9)
        ]
        
        for partner in additional_partners:
            cursor.execute("""
                INSERT INTO partners (partner_type, name, phone, email, rating, is_active)
                VALUES (%s, %s, %s, %s, %s, true)
                ON CONFLICT DO NOTHING
            """, partner)
        
        print(f"Добавлено {len(additional_partners)} дополнительных партнеров")
        
        # 3. Добавление расширенных заказов
        # Получаем ID партнеров и услуг для создания заказов
        cursor.execute("SELECT partner_id FROM partners ORDER BY partner_id LIMIT 15")
        partner_ids = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT service_id FROM services ORDER BY service_id")
        service_ids = [row[0] for row in cursor.fetchall()]
        
        # Статусы заказов
        order_statuses = ['новый', 'в работе', 'выполнен', 'отменен', 'ожидает оплаты']
        
        # Создаем 50 дополнительных заказов
        additional_orders = []
        for i in range(50):
            partner_id = random.choice(partner_ids)
            status = random.choice(order_statuses)
            total_amount = random.randint(500, 5000)
            prepayment = random.randint(0, total_amount // 2)
            
            # Случайная дата за последние 90 дней
            order_date = datetime.now() - timedelta(days=random.randint(0, 90))
            
            additional_orders.append((
                partner_id, 
                order_date, 
                status, 
                total_amount, 
                prepayment
            ))
        
        for order in additional_orders:
            cursor.execute("""
                INSERT INTO orders (partner_id, order_date, status, total_amount, prepayment)
                VALUES (%s, %s, %s, %s, %s)
                RETURNING order_id
            """, order)
            
            order_id = cursor.fetchone()[0]
            
            # Добавляем услуги в заказ (1-4 услуги на заказ)
            num_services = random.randint(1, 4)
            for _ in range(num_services):
                service_id = random.choice(service_ids)
                quantity = random.randint(1, 3)
                agreed_price = random.randint(200, 2000)
                
                cursor.execute("""
                    INSERT INTO order_services (order_id, service_id, quantity, agreed_price)
                    VALUES (%s, %s, %s, %s)
                """, (order_id, service_id, quantity, agreed_price))
        
        print(f"Добавлено {len(additional_orders)} дополнительных заказов с услугами")
        
        # 4. Добавление тестовых материалов для калькулятора
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS materials (
                material_id SERIAL PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                unit VARCHAR(20) NOT NULL,
                current_stock INTEGER DEFAULT 0,
                min_stock INTEGER DEFAULT 10
            )
        """)
        
        test_materials = [
            ('Стиральный порошок', 'кг', 100, 20),
            ('Кондиционер для белья', 'л', 50, 10),
            ('Отбеливатель', 'л', 30, 5),
            ('Пятновыводитель', 'л', 25, 5),
            ('Химчистка растворитель', 'л', 80, 15),
            ('Клей для ткани', 'шт', 40, 8),
            ('Нитки (катушка)', 'шт', 100, 20),
            ('Пуговицы набор', 'шт', 50, 10),
            ('Молния 40см', 'шт', 30, 5),
            ('Упаковочная пленка', 'рулон', 20, 4)
        ]
        
        for material in test_materials:
            cursor.execute("""
                INSERT INTO materials (name, unit, current_stock, min_stock)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, material)
        
        print(f"Добавлено {len(test_materials)} видов материалов")
        
        conn.commit()
        print("Все тестовые данные успешно добавлены!")
        
        # Вывод статистики
        cursor.execute("SELECT COUNT(*) FROM partners")
        total_partners = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM services")
        total_services = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM orders")
        total_orders = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM order_services")
        total_order_services = cursor.fetchone()[0]
        
        print("\n=== ТЕКУЩАЯ СТАТИСТИКА БАЗЫ ДАННЫХ ===")
        print(f"Всего партнеров: {total_partners}")
        print(f"Всего услуг: {total_services}")
        print(f"Всего заказов: {total_orders}")
        print(f"Всего услуг в заказах: {total_order_services}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"Ошибка при добавлении тестовых данных: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    add_extended_test_data()
    input("\nНажмите Enter для выхода...")