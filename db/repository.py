import sqlite3
import logging
from typing import List, Optional
from models.employee import Employee, EmployeeCreate, EmployeeUpdate

logger = logging.getLogger(__name__)


class EmployeeRepository:
    """Репозиторий для работы с сотрудниками в базе данных."""

    @staticmethod
    def get_all(conn: sqlite3.Connection) -> List[Employee]:
        """Получает всех сотрудников из базы данных.
        
        Args:
            conn: Соединение с базой данных
            
        Returns:
            List[Employee]: Список всех сотрудников
        """
        try:
            cursor = conn.execute("SELECT * FROM employees ORDER BY id")
            employees = []
            for row in cursor:
                employee = Employee(
                    id=row['id'],
                    name=row['name'],
                    username=row['username'],
                    group=row['group'],
                    phone=row['phone'],
                    email=row['email'],
                    age=row['age'],
                    sex=row['sex']
                )
                employees.append(employee)
            
            logger.info(f"Получено {len(employees)} сотрудников")
            return employees
        except sqlite3.Error as e:
            logger.error(f"Ошибка при получении сотрудников: {e}")
            raise

    @staticmethod
    def get_by_id(conn: sqlite3.Connection, employee_id: int) -> Optional[Employee]:
        """Получает сотрудника по ID.
        
        Args:
            conn: Соединение с базой данных
            employee_id: ID сотрудника
            
        Returns:
            Optional[Employee]: Сотрудник или None если не найден
        """
        try:
            cursor = conn.execute("SELECT * FROM employees WHERE id = ?", (employee_id,))
            row = cursor.fetchone()
            
            if row:
                employee = Employee(
                    id=row['id'],
                    name=row['name'],
                    username=row['username'],
                    group=row['group'],
                    phone=row['phone'],
                    email=row['email'],
                    age=row['age'],
                    sex=row['sex']
                )
                logger.info(f"Сотрудник с ID {employee_id} найден")
                return employee
            else:
                logger.info(f"Сотрудник с ID {employee_id} не найден")
                return None
        except sqlite3.Error as e:
            logger.error(f"Ошибка при получении сотрудника {employee_id}: {e}")
            raise

    @staticmethod
    def create(conn: sqlite3.Connection, data: EmployeeCreate) -> Employee:
        """Создает нового сотрудника.
        
        Args:
            conn: Соединение с базой данных
            data: Данные для создания сотрудника
            
        Returns:
            Employee: Созданный сотрудник
        """
        try:
            sql = """
            INSERT INTO employees (name, username, "group", phone, email, age, sex)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """
            
            cursor = conn.execute(sql, (
                data.name,
                data.username,
                data.group,
                data.phone,
                data.email,
                data.age,
                data.sex
            ))
            conn.commit()
            
            # Получаем созданного сотрудника
            employee_id = cursor.lastrowid
            employee = EmployeeRepository.get_by_id(conn, employee_id)
            
            if employee is None:
                raise ValueError(f"Не удалось получить созданного сотрудника с ID {employee_id}")
            
            logger.info(f"Создан сотрудник с ID {employee_id}")
            return employee
        except sqlite3.Error as e:
            logger.error(f"Ошибка при создании сотрудника: {e}")
            raise

    @staticmethod
    def update(conn: sqlite3.Connection, employee_id: int, data: EmployeeUpdate) -> Optional[Employee]:
        """Обновляет данные сотрудника.
        
        Args:
            conn: Соединение с базой данных
            employee_id: ID сотрудника
            data: Данные для обновления
            
        Returns:
            Optional[Employee]: Обновленный сотрудник или None если не найден
        """
        try:
            # Строим динамический SQL запрос
            update_fields = []
            params = []
            
            update_data = data.to_dict()
            for field, value in update_data.items():
                if value is not None:
                    # Используем кавычки для зарезервированного слова group
                    field_name = f'"{field}"' if field == 'group' else field
                    update_fields.append(f"{field_name} = ?")
                    params.append(value)
            
            if not update_fields:
                # Нет полей для обновления
                return EmployeeRepository.get_by_id(conn, employee_id)
            
            params.append(employee_id)
            sql = f"UPDATE employees SET {', '.join(update_fields)} WHERE id = ?"
            
            cursor = conn.execute(sql, params)
            conn.commit()
            
            if cursor.rowcount == 0:
                logger.info(f"Сотрудник с ID {employee_id} не найден для обновления")
                return None
            
            # Получаем обновленного сотрудника
            employee = EmployeeRepository.get_by_id(conn, employee_id)
            logger.info(f"Сотрудник с ID {employee_id} обновлен")
            return employee
        except sqlite3.Error as e:
            logger.error(f"Ошибка при обновлении сотрудника {employee_id}: {e}")
            raise

    @staticmethod
    def delete(conn: sqlite3.Connection, employee_id: int) -> bool:
        """Удаляет сотрудника по ID.
        
        Args:
            conn: Соединение с базой данных
            employee_id: ID сотрудника
            
        Returns:
            bool: True если сотрудник удален, False если не найден
        """
        try:
            cursor = conn.execute("DELETE FROM employees WHERE id = ?", (employee_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                logger.info(f"Сотрудник с ID {employee_id} удален")
                return True
            else:
                logger.info(f"Сотрудник с ID {employee_id} не найден для удаления")
                return False
        except sqlite3.Error as e:
            logger.error(f"Ошибка при удалении сотрудника {employee_id}: {e}")
            raise