from fastapi import FastAPI
from app.logger import setup_logging
from app.routes import router

# Настраиваем логирование
setup_logging()

# Создаем приложение FastAPI
app = FastAPI(
    title="StaffServerKaspersky",
    description="REST API для управления сотрудниками",
    version="1.0.0"
)

# Подключаем роуты
app.include_router(router)


@app.get("/")
async def root():
    """Корневой эндпоинт с информацией о приложении."""
    return {
        "message": "StaffServerKaspersky API",
        "version": "1.0.0",
        "description": "REST API для управления сотрудниками"
    }


@app.get("/health")
async def health_check():
    """Эндпоинт для проверки здоровья приложения."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)