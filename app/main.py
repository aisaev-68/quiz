from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from app.api.v1.api import api_router as api_router_v1
from app.schema.schemas import Failure
from app.models.database import engine, Base
from app.utils.logger import get_logger

logger = get_logger("main")


app = FastAPI(
    title="Test task",
    description="Тестовое задание.",
    version="0.1.0",
    docs_url="/api/docs",
    redoc_url='/api/redoc',
    responses={
        422: {
            "description": "Ошибка проверки",
            "model": Failure,
        },
    },
)

templates = Jinja2Templates(directory="www/data/templates")

origins = [
    "http://localhost",
    "http://127.0.0.1/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router_v1)


@app.on_event("startup")
async def start_db():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all)
        logger.info("База создана")
        await conn.run_sync(Base.metadata.create_all)


async def index(request: Request):
    logger.info("Переход на главную страницу")
    return templates.TemplateResponse("index.html", {"request": request})

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)
