"""
Модуль 4: Метод расчета количества материалов для АСУ ПСП «Чистая Планета»
Автоматизированная система управления производственно-сервисным предприятием
"""

class MaterialCalculator:
    """
    Класс для расчета потребности в материалах для производственных услуг
    с учетом технологических особенностей и перерасхода
    """
    
    @staticmethod
    def calculate_material_required(service_type_id, material_type_id, 
                                  quantity, service_param, service_coef, waste_percent):
        """
        Расчет количества материала с учетом перерасхода
        
        Args:
            service_type_id (int): ID типа услуги
            material_type_id (int): ID типа материала
            quantity (int): Количество услуг
            service_param (float): Параметр услуги (вес, объем и т.д.)
            service_coef (float): Коэффициент расхода материала на единицу параметра
            waste_percent (float): Процент технологического перерасхода
            
        Returns:
            int: Общее количество материала с учетом перерасхода, округленное до целого
                 Возвращает -1 в случае ошибки валидации данных
        """
        try:
            # Валидация входных данных
            if (quantity <= 0 or service_param <= 0 or 
                service_coef <= 0 or waste_percent < 0):
                return -1
            
            # Расчет материала на одну услугу
            material_per_service = service_param * service_coef
            
            # Общее количество материала
            total_material = material_per_service * quantity
            
            # Учет технологического перерасхода
            waste_factor = 1 + (waste_percent / 100)
            total_with_waste = total_material * waste_factor
            
            # Округление до целого числа в большую сторону
            return int(total_with_waste + 0.5)
            
        except (TypeError, ValueError):
            # Обработка ошибок неверного типа данных
            return -1

# Тестирование метода
if __name__ == "__main__":
    calculator = MaterialCalculator()
    
    print("Тестирование модуля расчета материалов АСУ ПСП 'Чистая Планета'")
    print("=" * 60)
    
    # Примеры расчетов для разных услуг
    test_cases = [
        {
            "name": "Стирка постельного белья",
            "params": (1, 1, 10, 5.0, 0.15, 5.0)  # 10 комплектов по 5кг, 0.15кг порошка на кг, 5% перерасход
        },
        {
            "name": "Химчистка курток", 
            "params": (2, 2, 5, 3.0, 0.2, 10.0)  # 5 курток по 3кг, 0.2л химии на кг, 10% перерасход
        },
        {
            "name": "Ремонт одежды",
            "params": (3, 3, 8, 1.0, 0.5, 15.0)  # 8 единиц, 0.5м ткани на единицу, 15% перерасход
        }
    ]
    
    for test in test_cases:
        result = calculator.calculate_material_required(*test["params"])
        print(f"Услуга: {test['name']}")
        print(f"Параметры: {test['params']}")
        print(f"Результат расчета: {result} единиц материала")
        print("-" * 40)