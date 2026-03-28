from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Employee:
    """Модель сотрудника с полным набором данных."""
    id: int
    name: str
    username: str
    group: Optional[str] = None
    phone: str = ""
    email: str = ""
    age: int = 0
    sex: str = ""
    
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
    age: int
    sex: str
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