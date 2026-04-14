from typing import Optional
import datetime



class OrderCostCalculator:

    COMPLEXITY_RATES = {
        "Стандарт": 1000,
        "Повышенная": 1500,
        "Высокая": 2500
    }

 
    URGENCY_COEFFICIENTS = {
        "Обычный": 1.0,
        "Срочный": 1.5,
        "В течение часа": 2.0
    }

    def __init__(self):
        self.base_price = 0.0
        self.complexity = ""
        self.work_time_hours = 0.0
        self.materials_cost = 0.0
        self.urgency = ""

    async def get_user_input(self):
        print("=== РАСЧЕТ СТОИМОСТИ ЗАКАЗА ===")
        
        print("Введите базовую цену услуги:")
        self.base_price = float(input())

        print("Выберите сложность работ:")
        for key in self.COMPLEXITY_RATES.keys():
            print(f"- {key}")
        self.complexity = input()

        print("Введите предполагаемое время выполнения (в часах):")
        self.work_time_hours = float(input())

        print("Введите стоимость материалов (если есть, иначе 0):")
        self.materials_cost = float(input())

        print("Выберите срочность заказа:")
        for key in self.URGENCY_COEFFICIENTS.keys():
            print(f"- {key}")
        self.urgency = input()

    def calculate_total(self) -> float:
        """Расчет итоговой стоимости по формуле."""
        try:
            rate_per_hour = self.COMPLEXITY_RATES[self.complexity]
            urgency_coeff = self.URGENCY_COEFFICIENTS[self.urgency]
            
            labor_cost = self.work_time_hours * rate_per_hour
            subtotal = self.base_price + labor_cost + self.materials_cost
            total_cost = subtotal * urgency_coeff

            return total_cost
        
        except KeyError as e:
            print(f"Ошибка: Неизвестное значение {e}. Расчет невозможен.")
            return 0

# Пример использования
if __name__ == "__main__":
    calculator = OrderCostCalculator()
    
   
    import asyncio
    asyncio.run(calculator.get_user_input())
    
    total = calculator.calculate_total()
    if total:
        print(f"Итоговая стоимость заказа: {total:.2f} руб.")