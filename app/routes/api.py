from fastapi import APIRouter

from routes import controller

api_router = APIRouter()
api_router.include_router(controller.router, tags=["pruebas"], prefix="/base")