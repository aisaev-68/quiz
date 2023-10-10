from fastapi import APIRouter

from app.api.v1.endpoints import answer

api_router = APIRouter()
api_router.include_router(answer.router, prefix="/api/answer", tags=["Получение вопросов и ответов"])
