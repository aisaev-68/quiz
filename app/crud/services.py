import datetime
from typing import Dict, List, Union
import aiohttp
from fastapi import Depends
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.models.database import get_db
from app.models.models import Answer
from app.utils.logger import get_logger
from app.schema.schemas import QuestionAnswer

logger = get_logger("crud.services")


class AnswerService:
    """Класс для обработки Endpoint связанных с вопросами и ответами."""

    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def get_data(self, count: int) -> List[Dict[str, Union[str, int, datetime.datetime]]]:
        """
        Метод для получения вопросов и ответов.
        :param count: количество вопросов.
        :return: список словарей.
        """
        url = f'{settings.URL}{count}'
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return []
                data = await response.json()
                answer_data = []
                for answer in data:
                    answer_data.append(
                        {
                            'question_id': answer['id'],
                            'question': answer['question'],
                            'answer': answer['answer'],
                            'created_at': datetime.datetime.strptime(answer['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ')
                        }
                    )
                return answer_data

    async def insert_data(self, data: List) -> Union[None, QuestionAnswer]:
        try:
            async with self.session.begin():
                prev = None
                prev_question = None

                for answer in data:
                    stmt = select(Answer).where(Answer.question_id == answer['question_id'])
                    question = await self.session.execute(stmt)
                    item_question = question.scalars().first()

                    if item_question is None:
                        add_data = Answer(
                            question_id=answer['question_id'],
                            question=answer['question'],
                            answer=answer['answer'],
                            created_at=answer['created_at']
                        )
                        self.session.add(add_data)

                        prev_question = prev
                        prev = QuestionAnswer(
                            id=add_data.id,
                            question_id=add_data.question_id,
                            question=add_data.question,
                            answer=add_data.answer,
                            created_at=add_data.created_at
                        )

                return prev_question
        except SQLAlchemyError:
            await self.session.rollback()
            raise

    async def get_all_data(
            self,
    ) -> List[Dict[str, Union[str, int, datetime.datetime]]]:
        """
        Метод для записи полученных данных.

        :param data: словарь данных ответов и вопросов.
        :return: None или словарь.
        """

        stmt = select(Answer)
        question = await self.session.execute(stmt)
        item_question = question.all()
        data = []
        for question in item_question:
            data.append(question[0].to_json())

        return data
