#!/usr/bin/env python3
"""Скрипт для генерации базы данных с 500 сотрудниками."""

import sqlite3
from faker import Faker
import random
import logging
import sys
import os

# Добавляем путь к проекту для импорта модулей
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db.database import get_connection, init_db
from models.employee import EmployeeGroup

# Настраиваем логирование
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем экземпляр Faker для генерации данных на английском
fake = Faker()


def generate_employees(count: int = 500) -> list:
    """Генерирует список сотрудников с рандомными данными.
    
    Args:
        count: Количество сотрудников для генерации
        
    Returns:
        list: Список кортежей с данными сотрудников
    """
    employees = []
    
    # Список возможных групп (включая None для сотрудников без группы)
    groups = EmployeeGroup.values() + [None]
    
    # Список возможных полов
    sexes = ["M", "F"]
    
    for i in range(count):
        sex = random.choice(sexes)
        
        if sex == "M":
            name = fake.first_name_male() + " " + fake.last_name_male()
        else:
            name = fake.first_name_female() + " " + fake.last_name_female()
        
        # Генерируем username на основе имени
        username = fake.user_name()
        
        employee = (
            name,
            username,
            random.choice(groups),
            fake.phone_number(),
            fake.email(),
            random.randint(20, 65),
            sex
        )
        employees.append(employee)
    
    return employees


def seed_database():
    """Заполняет базу данных тестовыми данными."""
    try:
        # Создаем соединение с базой данных
        conn = get_connection()
        init_db(conn)
        
        # Генерируем данные сотрудников
        logger.info("Generating data for 500 employees...")
        employees = generate_employees(500)
        
        # Вставляем данные в базу
        sql = """
        INSERT INTO employees (name, username, "group", phone, email, age, sex)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        
        conn.executemany(sql, employees)
        conn.commit()
        
        # Проверяем количество добавленных записей
        cursor = conn.execute("SELECT COUNT(*) FROM employees")
        count = cursor.fetchone()[0]
        
        logger.info(f"Database successfully populated. Added {count} employees")
        
        # Закрываем соединение
        conn.close()
        
    except Exception as e:
        logger.error(f"Error populating database: {e}")
        raise


if __name__ == "__main__":
    seed_database()