import sqlite3
import os
from typing import Generator
import logging

logger = logging.getLogger(__name__)


def get_connection(database_url: str = None) -> sqlite3.Connection:
    """Создает и возвращает соединение с SQLite базой данных.
    
    Args:
        database_url: Путь к файлу базы данных. Если None, используется employees.db
        
    Returns:
        sqlite3.Connection: Соединение с базой данных
    """
    if database_url is None:
        database_url = os.getenv("DATABASE_URL", "employees.db")
    
    conn = sqlite3.connect(database_url, check_same_thread=False)
    conn.row_factory = sqlite3.Row  # Для доступа к полям по имени
    
    logger.info(f"Подключение к базе данных создано: {database_url}")
    return conn


def init_db(conn: sqlite3.Connection) -> None:
    """Инициализирует базу данных, создавая таблицу employees если она не существует.
    
    Args:
        conn: Соединение с базой данных
    """
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
    
    try:
        conn.execute(create_table_sql)
        conn.commit()
        logger.info("Таблица employees создана или уже существует")
    except sqlite3.Error as e:
        logger.error(f"Ошибка при создании таблицы: {e}")
        raise


def get_db() -> Generator[sqlite3.Connection, None, None]:
    """Генератор для dependency injection в FastAPI.
    
    Yields:
        sqlite3.Connection: Соединение с базой данных
    """
    conn = get_connection()
    try:
        init_db(conn)
        yield conn
    finally:
        conn.close()
        logger.info("Соединение с базой данных закрыто")