from typing import Union, Annotated
from fastapi import (
    APIRouter,
    status,
    Depends,
    HTTPException,
    Body,
)

from app.schema.schemas import (
    Failure,
    QuestionAnswer,
    Question,
    EmptyQuestion,
    AllQuestionAnswer,
)
from app.crud.services import AnswerService
from app.utils.logger import get_logger

logger = get_logger("api.answer")

router = APIRouter()


@router.post(
    "",
    response_model=Union[QuestionAnswer, EmptyQuestion, Failure],
    summary="Возвращает предыдущей сохранённый вопрос для викторины.",
    description="Маршрут - возвращает предыдущей сохранённый вопрос.",
    response_description="Успешный ответ",
    status_code=status.HTTP_201_CREATED,
)
async def get_questions(
        service: Annotated[AnswerService, Depends()],
        questions_num: Question = Body(..., example={"questions_num": 5})
) -> Union[QuestionAnswer, EmptyQuestion, Failure]:
    try:
        questions_num = questions_num.questions_num

        if questions_num is None:
            raise HTTPException(status_code=400, detail="Отсутствует количество впросов.")

        questions = await service.get_data(questions_num)
        response_data = await service.insert_data(questions)
        if response_data is None:
            logger.info("Возвращаю пустое значение")
            return EmptyQuestion()

    except Exception as er:
        error_message = str(er)
        error_type = type(er).__name__
        logger.error(error_message)
        return Failure(result=False, error_type=error_type, body_message=error_message)

    logger.info("Возвращаю предыдущей сохранённый вопрос")
    return response_data


@router.get(
    "/all",
    response_model=Union[AllQuestionAnswer, EmptyQuestion, Failure],
    summary="Возвращает все сохранённые в базе вопросы для викторины.",
    description="Маршрут - возвращает все сохранённые вопросы.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
)
async def get_all_questions(
        service: Annotated[AnswerService, Depends()],
) -> Union[AllQuestionAnswer, EmptyQuestion, Failure]:
    try:
        questions = await service.get_all_data()
        if len(questions) == 0:
            logger.info("Возвращаю пустое значение")
            return EmptyQuestion()

    except Exception as er:
        error_message = str(er)
        error_type = type(er).__name__
        logger.error(error_message)
        return Failure(result=False, error_type=error_type, body_message=error_message)

    logger.info("Возвращаю все данные из базы")
    return AllQuestionAnswer(questions=questions)
