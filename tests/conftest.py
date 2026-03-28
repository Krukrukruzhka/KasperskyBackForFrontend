import pytest
import sqlite3
from fastapi.testclient import TestClient
from app.main import app
from db.database import get_db


@pytest.fixture
def client():
    """Фикстура для создания тестового клиента с переопределенной базой данных."""
    
    # Создаем одно соединение для всех запросов в рамках теста
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    
    # Создаем таблицу
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        username TEXT NOT NULL,
        "group" TEXT,
        phone TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        sex TEXT NOT NULL
    )
    """
    conn.execute(create_table_sql)
    conn.commit()
    
    def override_get_db():
        try:
            yield conn
        finally:
            # Не закрываем соединение здесь, оно будет закрыто после теста
            pass
    
    # Переопределяем зависимость get_db
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Закрываем соединение после теста
    conn.close()
    
    # Очищаем переопределения после теста
    app.dependency_overrides.clear()


@pytest.fixture
def sample_employee():
    """Фикстура с тестовыми данными сотрудника."""
    return {
        "name": "John Smith",
        "username": "johnsmith",
        "group": "CDM/Managers",
        "phone": "+7-999-123-45-67",
        "email": "john.smith@example.com",
        "age": 30,
        "sex": "M"
    }