from typing import Union, Annotated
import aiohttp
from fastapi import (
    APIRouter,
    status,
    Depends,
    Body,
    HTTPException,
)

from app.schema.schemas import (
    Failure,
    QuestionAnswer,
    Question,
    AllQuestionAnswer,
)
from app.crud.services import AnswerService
from app.utils.logger import get_logger

logger = get_logger("api.answer")

router = APIRouter()


@router.post(
    "",
    response_model=Union[QuestionAnswer, Failure],
    response_model_exclude_unset=True,  # пустые поля в ответе исключаются
    summary="Возвращает предыдущей сохранённый вопрос для викторины.",
    description="Маршрут - возвращает предыдущей сохранённый вопрос.",
    response_description="Успешный ответ",
    status_code=status.HTTP_201_CREATED,
)
async def get_questions(
        service: Annotated[AnswerService, Depends()],
        questions_num: Question = Body(embed=False)
) -> QuestionAnswer | Failure:
    """
    Возвращает предыдущей сохранённый вопрос для викторины.
    :param service: сервис работы с данными.
    :param questions_num: словарь в виде запроса.
    :return: модели QuestionAnswer или Failure.
    """

    try:
        questions_num = questions_num.questions_num
        questions = await service.get_data(questions_num)
    except aiohttp.ClientConnectorError as er:
        raise HTTPException(status_code=400, detail=f'{type(er).__name__}: {str(er)}')

    response_data = await service.insert_data(questions)

    logger.info("Возвращаю предыдущей сохранённый вопрос")
    return response_data


@router.get(
    "/all",
    response_model=Union[AllQuestionAnswer, Failure],
    summary="Возвращает все сохранённые в базе вопросы для викторины.",
    description="Маршрут - возвращает все сохранённые вопросы.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
)
async def get_all_questions(
        service: Annotated[AnswerService, Depends()],
) -> AllQuestionAnswer | Failure:
    """
    Возвращает все сохранённые в базе вопросы для викторины.
    :param service: сервис работы с данными.
    :return: модели AllQuestionAnswer или Failure.
    """

    questions = await service.get_all_data()

    logger.info("Возвращаю все данные из базы")
    return questions
