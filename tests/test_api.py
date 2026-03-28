import pytest
from fastapi import status


class TestEmployeeAPI:
    """Тесты для API сотрудников."""

    def test_create_employee(self, client, sample_employee):
        """Тест создания сотрудника."""
        response = client.post("/employees/", json=sample_employee)
        
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        
        assert "id" in data
        assert data["name"] == sample_employee["name"]
        assert data["username"] == sample_employee["username"]
        assert data["group"] == sample_employee["group"]
        assert data["phone"] == sample_employee["phone"]
        assert data["email"] == sample_employee["email"]
        assert data["age"] == sample_employee["age"]
        assert data["sex"] == sample_employee["sex"]

    def test_get_employees(self, client, sample_employee):
        """Тест получения списка сотрудников."""
        # Сначала создаем сотрудника
        client.post("/employees/", json=sample_employee)
        
        response = client.get("/employees/")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert isinstance(data, list)
        assert len(data) > 0
        assert "id" in data[0]
        assert "name" in data[0]
        assert "username" in data[0]

    def test_get_employee_by_id(self, client, sample_employee):
        """Тест получения сотрудника по ID."""
        # Создаем сотрудника
        create_response = client.post("/employees/", json=sample_employee)
        employee_id = create_response.json()["id"]
        
        response = client.get(f"/employees/{employee_id}")
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["id"] == employee_id
        assert data["name"] == sample_employee["name"]
        assert data["username"] == sample_employee["username"]

    def test_get_employee_not_found(self, client):
        """Тест получения несуществующего сотрудника."""
        response = client.get("/employees/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "не найден" in response.json()["detail"]

    def test_update_employee(self, client, sample_employee):
        """Тест обновления сотрудника."""
        # Создаем сотрудника
        create_response = client.post("/employees/", json=sample_employee)
        employee_id = create_response.json()["id"]
        
        # Обновляем данные
        update_data = {
            "name": "Peter Peterson",
            "username": "peterp",
            "group": "CDN/Sales",
            "age": 35
        }
        
        response = client.put(f"/employees/{employee_id}", json=update_data)
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        
        assert data["id"] == employee_id
        assert data["name"] == update_data["name"]
        assert data["username"] == update_data["username"]
        assert data["group"] == update_data["group"]
        assert data["age"] == update_data["age"]
        # Проверяем, что остальные поля не изменились
        assert data["phone"] == sample_employee["phone"]
        assert data["email"] == sample_employee["email"]
        assert data["sex"] == sample_employee["sex"]

    def test_update_employee_not_found(self, client):
        """Тест обновления несуществующего сотрудника."""
        update_data = {"name": "New Name"}
        response = client.put("/employees/999", json=update_data)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "не найден" in response.json()["detail"]

    def test_delete_employee(self, client, sample_employee):
        """Тест удаления сотрудника."""
        # Создаем сотрудника
        create_response = client.post("/employees/", json=sample_employee)
        employee_id = create_response.json()["id"]
        
        # Удаляем сотрудника
        response = client.delete(f"/employees/{employee_id}")
        
        assert response.status_code == status.HTTP_200_OK
        assert "успешно удален" in response.json()["message"]
        
        # Проверяем, что сотрудник действительно удален
        get_response = client.get(f"/employees/{employee_id}")
        assert get_response.status_code == status.HTTP_404_NOT_FOUND

    def test_delete_employee_not_found(self, client):
        """Тест удаления несуществующего сотрудника."""
        response = client.delete("/employees/999")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert "не найден" in response.json()["detail"]

    def test_create_employee_validation(self, client):
        """Тест валидации при создании сотрудника."""
        # Неполные данные (отсутствует обязательное поле)
        invalid_data = {
            "name": "John Smith",
            "username": "johnsmith",
            "phone": "+7 (999) 123-45-67",
            "email": "john@example.com"
            # Отсутствуют age и sex (теперь они опциональны)
        }
        
        response = client.post("/employees/", json=invalid_data)
        
        # Теперь age и sex опциональны, поэтому запрос должен пройти
        assert response.status_code == status.HTTP_201_CREATED

    def test_create_employee_invalid_group(self, client):
        """Тест создания сотрудника с недопустимой группой."""
        invalid_data = {
            "name": "John Smith",
            "username": "johnsmith",
            "group": "InvalidGroup",
            "phone": "+7 (999) 123-45-67",
            "email": "john@example.com",
            "age": 30,
            "sex": "M"
        }
        
        response = client.post("/employees/", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "Недопустимое значение группы" in response.json()["detail"]

    def test_update_employee_invalid_group(self, client, sample_employee):
        """Тест обновления сотрудника с недопустимой группой."""
        # Создаем сотрудника
        create_response = client.post("/employees/", json=sample_employee)
        employee_id = create_response.json()["id"]

        update_data = {"group": "NotAValidGroup"}
        response = client.put(f"/employees/{employee_id}", json=update_data)

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "Недопустимое значение группы" in response.json()["detail"]

    def test_create_employee_without_group(self, client):
        """Тест создания сотрудника без группы (group=None допустимо)."""
        data = {
            "name": "Jane Doe",
            "username": "janedoe",
            "phone": "+7 (999) 000-00-00",
            "email": "jane@example.com",
            "age": 25,
            "sex": "F"
        }

        response = client.post("/employees/", json=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["group"] is None

    def test_create_employee_invalid_phone_format(self, client):
        """Тест создания сотрудника с неверным форматом телефона."""
        invalid_data = {
            "name": "John Smith",
            "username": "johnsmith",
            "group": "CDM/Managers",
            "phone": "+7-999-123-45-67",  # Неправильный формат
            "email": "john@example.com",
            "age": 30,
            "sex": "M"
        }
        
        response = client.post("/employees/", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "Телефонный номер должен быть в формате" in response.json()["detail"]

    def test_create_employee_invalid_username(self, client):
        """Тест создания сотрудника с username, начинающимся с @."""
        invalid_data = {
            "name": "John Smith",
            "username": "@johnsmith",  # Начинается с @
            "group": "CDM/Managers",
            "phone": "+7 (999) 123-45-67",
            "email": "john@example.com",
            "age": 30,
            "sex": "M"
        }
        
        response = client.post("/employees/", json=invalid_data)
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        assert "Username не должен начинаться с символа @" in response.json()["detail"]

    def test_create_employee_without_age_sex(self, client):
        """Тест создания сотрудника без age и sex (теперь они опциональны)."""
        data = {
            "name": "Jane Doe",
            "username": "janedoe",
            "phone": "+7 (999) 000-00-00",
            "email": "jane@example.com"
            # age и sex отсутствуют
        }

        response = client.post("/employees/", json=data)

        assert response.status_code == status.HTTP_201_CREATED
        assert response.json()["age"] is None
        assert response.json()["sex"] is None