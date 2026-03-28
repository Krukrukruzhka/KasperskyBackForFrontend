from fastapi import APIRouter, Depends, HTTPException, Request, status
import sqlite3
import logging
from typing import List

from models.employee import Employee, EmployeeCreate, EmployeeUpdate
from db.repository import EmployeeRepository
from db.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/employees", tags=["employees"])


@router.get("/", response_model=List[Employee])
async def get_employees(conn: sqlite3.Connection = Depends(get_db)):
    """Получить список всех сотрудников."""
    logger.info("Запрос на получение списка сотрудников")
    employees = EmployeeRepository.get_all(conn)
    return employees


@router.get("/{employee_id}", response_model=Employee)
async def get_employee(employee_id: int, conn: sqlite3.Connection = Depends(get_db)):
    """Получить сотрудника по ID."""
    logger.info(f"Запрос на получение сотрудника с ID {employee_id}")
    employee = EmployeeRepository.get_by_id(conn, employee_id)
    
    if employee is None:
        logger.warning(f"Сотрудник с ID {employee_id} не найден")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Сотрудник с ID {employee_id} не найден"
        )
    
    return employee


@router.post("/", response_model=Employee, status_code=status.HTTP_201_CREATED)
async def create_employee(request: Request, conn: sqlite3.Connection = Depends(get_db)):
    """Создать нового сотрудника."""
    logger.info("Запрос на создание сотрудника")
    
    try:
        # Парсим JSON вручную без Pydantic
        data = await request.json()
        
        # Валидация обязательных полей
        required_fields = ['name', 'username', 'phone', 'email', 'age', 'sex']
        for field in required_fields:
            if field not in data:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=f"Обязательное поле '{field}' отсутствует"
                )
        
        # Создаем объект EmployeeCreate
        employee_data = EmployeeCreate(
            name=data['name'],
            username=data['username'],
            phone=data['phone'],
            email=data['email'],
            age=data['age'],
            sex=data['sex'],
            group=data.get('group')
        )
        
        employee = EmployeeRepository.create(conn, employee_data)
        logger.info(f"Создан сотрудник с ID {employee.id}")
        return employee
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при создании сотрудника: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Некорректные данные для создания сотрудника"
        )


@router.put("/{employee_id}", response_model=Employee)
async def update_employee(employee_id: int, request: Request, conn: sqlite3.Connection = Depends(get_db)):
    """Обновить данные сотрудника."""
    logger.info(f"Запрос на обновление сотрудника с ID {employee_id}")
    
    try:
        # Парсим JSON вручную
        data = await request.json()
        
        # Создаем объект EmployeeUpdate
        update_data = EmployeeUpdate(
            name=data.get('name'),
            username=data.get('username'),
            group=data.get('group'),
            phone=data.get('phone'),
            email=data.get('email'),
            age=data.get('age'),
            sex=data.get('sex')
        )
        
        employee = EmployeeRepository.update(conn, employee_id, update_data)
        
        if employee is None:
            logger.warning(f"Сотрудник с ID {employee_id} не найден для обновления")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Сотрудник с ID {employee_id} не найден"
            )
        
        logger.info(f"Сотрудник с ID {employee_id} обновлен")
        return employee
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при обновлении сотрудника {employee_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Некорректные данные для обновления сотрудника"
        )


@router.delete("/{employee_id}")
async def delete_employee(employee_id: int, conn: sqlite3.Connection = Depends(get_db)):
    """Удалить сотрудника по ID."""
    logger.info(f"Запрос на удаление сотрудника с ID {employee_id}")
    
    deleted = EmployeeRepository.delete(conn, employee_id)
    
    if not deleted:
        logger.warning(f"Сотрудник с ID {employee_id} не найден для удаления")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Сотрудник с ID {employee_id} не найден"
        )
    
    logger.info(f"Сотрудник с ID {employee_id} удален")
    return {"message": f"Сотрудник с ID {employee_id} успешно удален"}