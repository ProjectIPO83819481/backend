#!/usr/bin/env python
"""
Script для заполнения базы данных тестовыми данными
Запуск: python seed_database.py
"""

import os
import sys
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import DATABASE_URL

engine = create_engine(DATABASE_URL.replace("+asyncpg", ""), pool_size=1000, max_overflow=-1, connect_args={"timeout": 60})
session_maker = sessionmaker(engine, expire_on_commit=False)

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.models.models import (
    User, Order, Role, Status,
    AdditionalWorkRequestStatuses,
    AdditionalWork
)
from app.models.service import ( Service, Photo, ServiceCategory )


def create_test_data(session):

    users_data = [
        # Клиенты
        {
            "email": "ivan@example.com",
            "password_hash": "hash_ivan123",
            "role": Role.CLIENT,
            "full_name": "Иван Петров",
            "phone": "+79161234567",
            "photo_url": "/photos/ivan.jpg",
            "is_suspended": False,
            "suspended_until": None,
        },
        {
            "email": "maria@example.com",
            "password_hash": "hash_maria123",
            "role": Role.CLIENT,
            "full_name": "Мария Сидорова",
            "phone": "+79162345678",
            "photo_url": "/photos/maria.jpg",
            "is_suspended": False,
            "suspended_until": None,
        },
        {
            "email": "alexey@example.com",
            "password_hash": "hash_alexey123",
            "role": Role.CLIENT,
            "full_name": "Алексей Смирнов",
            "phone": "+79163456789",
            "photo_url": "/photos/alexey.jpg",
            "is_suspended": False,
            "suspended_until": None,
        },
        {
            "email": "elena@example.com",
            "password_hash": "hash_elena123",
            "role": Role.CLIENT,
            "full_name": "Елена Кузнецова",
            "phone": "+79164567890",
            "photo_url": "/photos/elena.jpg",
            "is_suspended": False,
            "suspended_until": None,
        },
        {
            "email": "blocked@example.com",
            "password_hash": "hash_blocked123",
            "role": Role.CLIENT,
            "full_name": "Заблокированный Пользователь",
            "phone": "+79169012345",
            "photo_url": None,
            "is_suspended": True,
            "suspended_until": datetime.now() + timedelta(days=30),
        },
        # Исполнители
        {
            "email": "master1@example.com",
            "password_hash": "hash_master123",
            "role": Role.EXECUTOR,
            "full_name": "Дмитрий Волков",
            "phone": "+79165678901",
            "photo_url": "/photos/master1.jpg",
            "is_suspended": False,
            "suspended_until": None,
        },
        {
            "email": "master2@example.com",
            "password_hash": "hash_master456",
            "role": Role.EXECUTOR,
            "full_name": "Андрей Морозов",
            "phone": "+79166789012",
            "photo_url": "/photos/master2.jpg",
            "is_suspended": False,
            "suspended_until": None,
        },
        {
            "email": "master3@example.com",
            "password_hash": "hash_master789",
            "role": Role.EXECUTOR,
            "full_name": "Сергей Новиков",
            "phone": "+79167890123",
            "photo_url": "/photos/master3.jpg",
            "is_suspended": False,
            "suspended_until": None,
        },
        # Администратор
        {
            "email": "admin@example.com",
            "password_hash": "hash_admin123",
            "role": Role.ADMIN,
            "full_name": "Администратор Системы",
            "phone": "+79168901234",
            "photo_url": "/photos/admin.jpg",
            "is_suspended": False,
            "suspended_until": None,
        },
    ]

    users = {}
    for user_data in users_data:
        user = User(**user_data)
        session.add(user)
        session.flush()
        users[user_data["email"]] = user

    session.commit()


    executor1 = users["master1@example.com"]
    executor2 = users["master2@example.com"]
    executor3 = users["master3@example.com"]

    services_data = [
        {
            "user_id": executor1.user_id,
            "name": "Ремонт iPhone 13",
            "category_name": ServiceCategory.REPAIRS,
            "subcategory": "Mobile Phones",
            "description": "Замена экрана, аккумулятора, разъема зарядки. Работаем с оригинальными запчастями.",
            "base_price": 5000.00,
            "price_range_max": 8000.00,
            "avg_duration_minutes": 120,
            "required_materials": "Запасные части, специальный инструмент",
            "rating": 4.8,
            "total_reviews": 45,
            "popularity_score": 92.5,
            "is_active": True,
        },
        {
            "user_id": executor1.user_id,
            "name": "Ремонт ноутбуков",
            "category_name": ServiceCategory.REPAIRS,
            "subcategory": "Computers",
            "description": "Диагностика, чистка от пыли, замена термопасты, ремонт материнской платы.",
            "base_price": 3000.00,
            "price_range_max": 15000.00,
            "avg_duration_minutes": 90,
            "required_materials": "Термопаста, инструменты",
            "rating": 4.9,
            "total_reviews": 78,
            "popularity_score": 88.3,
            "is_active": True,
        },
        {
            "user_id": executor2.user_id,
            "name": "Сантехнические работы",
            "category_name": ServiceCategory.PLUMBING,
            "subcategory": "Installation",
            "description": "Установка и замена сантехники, устранение протечек, монтаж труб.",
            "base_price": 4000.00,
            "price_range_max": 10000.00,
            "avg_duration_minutes": 180,
            "required_materials": "Сантехника, прокладки, герметик",
            "rating": 4.7,
            "total_reviews": 112,
            "popularity_score": 85.7,
            "is_active": True,
        },
        {
            "user_id": executor2.user_id,
            "name": "Электромонтаж",
            "category_name": ServiceCategory.ELECTRICAL,
            "subcategory": "Wiring",
            "description": "Установка розеток и выключателей, прокладка проводки, замена электрощитов.",
            "base_price": 3500.00,
            "price_range_max": 12000.00,
            "avg_duration_minutes": 120,
            "required_materials": "Кабель, розетки, автоматы",
            "rating": 4.6,
            "total_reviews": 67,
            "popularity_score": 79.2,
            "is_active": True,
        },
        {
            "user_id": executor3.user_id,
            "name": "Уборка квартир",
            "category_name": ServiceCategory.CLEANING,
            "subcategory": "General Cleaning",
            "description": "Генеральная уборка 3-комнатной квартиры. Включает мытье окон, чистку ковров, санузлов.",
            "base_price": 6000.00,
            "price_range_max": 15000.00,
            "avg_duration_minutes": 240,
            "required_materials": "Моющие средства, инвентарь",
            "rating": 4.9,
            "total_reviews": 203,
            "popularity_score": 96.8,
            "is_active": True,
        },
        {
            "user_id": executor3.user_id,
            "name": "Химчистка мягкой мебели",
            "category_name": ServiceCategory.CLEANING,
            "subcategory": "Upholstery",
            "description": "Глубокая чистка диванов и кресел с выведением пятен.",
            "base_price": 3500.00,
            "price_range_max": 7000.00,
            "avg_duration_minutes": 120,
            "required_materials": "Специальные средства, экстрактор",
            "rating": 4.8,
            "total_reviews": 89,
            "popularity_score": 87.4,
            "is_active": True,
        },
    ]

    services = []
    for service_data in services_data:
        service = Service(**service_data)
        session.add(service)
        session.flush()
        services.append(service)

        photos_data = [
            {
                "service_id": service.service_id,
                "image_url": f"/photos/services/service_{service.service_id}_1.jpg",
                "description": f"Пример работы: {service.name} - фото 1"
            },
            {
                "service_id": service.service_id,
                "image_url": f"/photos/services/service_{service.service_id}_2.jpg",
                "description": f"Пример работы: {service.name} - фото 2"
            },
        ]

        for photo_data in photos_data:
            photo = Photo(**photo_data)
            session.add(photo)

    session.commit()


    client1 = users["ivan@example.com"]
    client2 = users["maria@example.com"]
    client3 = users["alexey@example.com"]
    client4 = users["elena@example.com"]

    orders_data = [
        {
            "client_id": client1.user_id,
            "executor_id": None,
            "service_id": services[0].service_id,
            "status": Status.NEW,
            "address": "г. Москва, ул. Тверская, д. 15, кв. 47",
            "scheduled_at": datetime.now() + timedelta(days=2),
            "description": "Телефон перестал заряжаться, нужна замена разъема",
            "base_cost": 5000.00,
            "final_cost": 5000.00,
            "created_at": datetime.now() - timedelta(hours=3),
        },
        # Принятый заказ
        {
            "client_id": client2.user_id,
            "executor_id": executor1.user_id,
            "service_id": services[1].service_id,
            "status": Status.ACCEPTED,
            "address": "г. Москва, Ленинский пр-т, д. 25",
            "scheduled_at": datetime.now() + timedelta(days=1),
            "description": "Ноутбук сильно греется и выключается",
            "base_cost": 3000.00,
            "final_cost": 3500.00,
            "created_at": datetime.now() - timedelta(days=1),
            "updated_at": datetime.now() - timedelta(hours=12),
        },
        # В работе
        {
            "client_id": client3.user_id,
            "executor_id": executor2.user_id,
            "service_id": services[2].service_id,
            "status": Status.IN_PROGRESS,
            "address": "г. Москва, ул. Арбат, д. 10",
            "scheduled_at": datetime.now() - timedelta(hours=2),
            "description": "Протекает кран на кухне и в ванной",
            "base_cost": 4000.00,
            "final_cost": 4500.00,
            "created_at": datetime.now() - timedelta(days=2),
            "updated_at": datetime.now() - timedelta(hours=3),
            "started_at": datetime.now() - timedelta(hours=1),
        },
        # Завершенный с отзывом
        {
            "client_id": client4.user_id,
            "executor_id": executor3.user_id,
            "service_id": services[4].service_id,
            "status": Status.COMPLETED,
            "address": "г. Москва, ул. Пушкина, д. 8, кв. 123",
            "scheduled_at": datetime.now() - timedelta(days=5),
            "description": "Генеральная уборка 3-комнатной квартиры",
            "base_cost": 6000.00,
            "final_cost": 6000.00,
            "created_at": datetime.now() - timedelta(days=6),
            "updated_at": datetime.now() - timedelta(days=4),
            "started_at": datetime.now() - timedelta(days=5),
            "completed_at": datetime.now() - timedelta(days=5),
            "review_comment": "Отличная работа! Всё чисто и аккуратно. Рекомендую!",
            "review_created_at": datetime.now() - timedelta(days=4),
            "review_executor_response": "Спасибо за отзыв! Рады стараться!",
        },
        # Отмененный заказ
        {
            "client_id": client1.user_id,
            "executor_id": executor2.user_id,
            "service_id": services[3].service_id,
            "cancelled_by_user_id": client1.user_id,
            "status": Status.CANCELLED,
            "address": "г. Москва, ул. Ленина, д. 5",
            "scheduled_at": datetime.now() + timedelta(days=3),
            "description": "Установка новой проводки",
            "base_cost": 3500.00,
            "final_cost": 3500.00,
            "created_at": datetime.now() - timedelta(days=2),
            "updated_at": datetime.now() - timedelta(days=1),
            "cancelled_at": datetime.now() - timedelta(days=1),
            "cancellation_reason": "Передумал, нашел более дешевый вариант",
        },
        # Еще один завершенный заказ с отзывом
        {
            "client_id": client2.user_id,
            "executor_id": executor1.user_id,
            "service_id": services[0].service_id,
            "status": Status.COMPLETED,
            "address": "г. Москва, ул. Новослободская, д. 12",
            "scheduled_at": datetime.now() - timedelta(days=10),
            "description": "Замена экрана iPhone 13 после падения",
            "base_cost": 5000.00,
            "final_cost": 6500.00,  # С дополнительными работами
            "created_at": datetime.now() - timedelta(days=12),
            "updated_at": datetime.now() - timedelta(days=8),
            "started_at": datetime.now() - timedelta(days=10),
            "completed_at": datetime.now() - timedelta(days=8),
            "review_comment": "Сделали быстро и качественно. Цена немного выше ожидаемой, но результат того стоит.",
            "review_created_at": datetime.now() - timedelta(days=7),
            "review_executor_response": "Спасибо за доверие! Оригинальное стекло действительно дороже, но служит дольше.",
        },
        # В работе с запросом на доп работы
        {
            "client_id": client3.user_id,
            "executor_id": executor3.user_id,
            "service_id": services[5].service_id,
            "status": Status.IN_PROGRESS,
            "address": "г. Москва, Рублевское шоссе, д. 3",
            "scheduled_at": datetime.now() - timedelta(hours=5),
            "description": "Химчистка большого углового дивана",
            "base_cost": 3500.00,
            "final_cost": 3500.00,
            "created_at": datetime.now() - timedelta(days=1),
            "updated_at": datetime.now() - timedelta(hours=4),
            "started_at": datetime.now() - timedelta(hours=4),
        },
    ]

    orders = []
    for order_data in orders_data:
        order = Order(**order_data)
        session.add(order)
        session.flush()
        orders.append(order)

    session.commit()
    print(f"  Создано {len(orders)} заказов")

    # ============================================
    # 4. СОЗДАНИЕ ЗАПРОСОВ НА ДОПОЛНИТЕЛЬНЫЕ РАБОТЫ
    # ============================================
    print("Создание запросов на дополнительные работы...")

    additional_works_data = [
        # Для заказа в работе (ожидает ответа)
        {
            "order_id": orders[2].order_id,  # Заказ на сантехнику
            "responded_by_user_id": executor2.user_id,
            "description": "Обнаружил, что требуется замена стояка, так как старый в плохом состоянии",
            "additional_cost": 5000.00,
            "additional_time_minutes": 120,
            "status": AdditionalWorkRequestStatuses.PENDING,
            "created_at": datetime.now() - timedelta(hours=2),
            "responded_at": None,
        },
        # Одобренный запрос на доп работы (для завершенного заказа)
        {
            "order_id": orders[4].order_id,  # Заказ на ремонт iPhone
            "responded_by_user_id": executor1.user_id,
            "description": "Помимо экрана, требуется замена аккумулятора (он вздулся)",
            "additional_cost": 1500.00,
            "additional_time_minutes": 30,
            "status": AdditionalWorkRequestStatuses.APPROVED,
            "created_at": datetime.now() - timedelta(days=11),
            "responded_at": datetime.now() - timedelta(days=10),
        },
        # Отклоненный запрос
        {
            "order_id": orders[5].order_id,  # Заказ на уборку
            "responded_by_user_id": executor3.user_id,
            "description": "Клиент просит также помыть окна снаружи (это требует спецоборудования)",
            "additional_cost": 2000.00,
            "additional_time_minutes": 60,
            "status": AdditionalWorkRequestStatuses.REJECTED,
            "created_at": datetime.now() - timedelta(days=3),
            "responded_at": datetime.now() - timedelta(days=2),
        },
        # Новый запрос (для заказа в работе)
        {
            "order_id": orders[6].order_id,  # Заказ на химчистку
            "responded_by_user_id": executor3.user_id,
            "description": "На диване есть сложные пятна от вина, требуется усиленная обработка специальным средством",
            "additional_cost": 1000.00,
            "additional_time_minutes": 45,
            "status": AdditionalWorkRequestStatuses.PENDING,
            "created_at": datetime.now() - timedelta(hours=1),
            "responded_at": None,
        },
    ]

    for aw_data in additional_works_data:
        additional_work = AdditionalWork(**aw_data)
        session.add(additional_work)

    session.commit()
    print(f"  Создано {len(additional_works_data)} запросов на дополнительные работы")

    # ============================================
    # 5. ОБНОВЛЕНИЕ РЕЙТИНГОВ УСЛУГ
    # ============================================
    print("Обновление рейтингов услуг на основе отзывов...")

    # В реальном приложении здесь можно пересчитать рейтинги на основе отзывов
    # Сейчас просто выводим информацию

    print("  Рейтинги услуг обновлены")

    print("\n" + "="*50)
    print("База данных успешно заполнена тестовыми данными!")
    print("="*50)

    # Вывод статистики
    print("\nСтатистика:")
    print(f"  - Пользователей: {session.query(User).count()}")
    print(f"  - Услуг: {session.query(Service).count()}")
    print(f"  - Фото: {session.query(Photo).count()}")
    print(f"  - Заказов: {session.query(Order).count()}")
    print(f"  - Запросов на доп. работы: {session.query(AdditionalWork).count()}")


def main():
    with session_maker() as session:
        create_test_data(session)


if __name__ == "__main__":
    main()