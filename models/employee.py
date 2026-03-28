from dataclasses import dataclass, asdict
from typing import Optional
from enum import Enum


class EmployeeGroup(str, Enum):
    """Допустимые группы сотрудников."""
    CDM_MANAGERS = 'CDM/Managers'
    CDN_MANAGERS = 'CDN/Managers'
    CDM_FINANCIALS = 'CDM/Financials'
    CDN_HUMAN_RESOURCES = 'CDN/Human resources'
    CDN_KVANTS = 'CDN/Kvants'
    CDN_OUTSOURCED = 'CDN/Outsourced'
    CDN_SALES = 'CDN/Sales'
    CDN_TOP_KEVINS = 'CDN/Top Kevins'
    CONVEO = 'CONVEO'

    @classmethod
    def values(cls) -> list:
        """Возвращает список допустимых значений."""
        return [e.value for e in cls]


@dataclass
class Employee:
    """Модель сотрудника с полным набором данных."""
    id: int
    name: str
    username: str
    group: Optional[str] = None
    phone: str = ""
    email: str = ""
    age: Optional[int] = None
    sex: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Преобразует объект в словарь."""
        return asdict(self)


@dataclass
class EmployeeCreate:
    """Модель для создания сотрудника (без id)."""
    name: str
    username: str
    phone: str
    email: str
    age: Optional[int] = None
    sex: Optional[str] = None
    group: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Преобразует объект в словарь."""
        return asdict(self)


@dataclass
class EmployeeUpdate:
    """Модель для обновления сотрудника (все поля опциональны)."""
    name: Optional[str] = None
    username: Optional[str] = None
    group: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    sex: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Преобразует объект в словарь, исключая None значения."""
        return {k: v for k, v in asdict(self).items() if v is not None}