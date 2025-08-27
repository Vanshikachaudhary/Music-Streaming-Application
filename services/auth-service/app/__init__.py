# auth-service/app/__init__.py

from fastapi import FastAPI

app = FastAPI(
    title="Auth Service",
    description="Handles user signup, login, and JWT authentication",
    version="1.0.0"
)
