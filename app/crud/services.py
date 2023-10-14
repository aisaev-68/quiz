import datetime
from typing import Dict, List, Union
import aiohttp
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.config import settings
from app.models.database import get_db
from app.models.models import Answer
from app.utils.logger import get_logger
from app.schema.schemas import QuestionAnswer, Failure, AllQuestionAnswer

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

    async def insert_data(self, data: List) -> Union[QuestionAnswer, Failure]:

        try:
            prev = None
            prev_question = None
            async with self.session.begin():
                for answer in data:
                    stmt = select(Answer).where(Answer.question_id == int(answer['question_id']))
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
                        prev = add_data

                await self.session.commit()

                if prev_question:
                    return QuestionAnswer(**prev_question.to_json())

                else:
                    return QuestionAnswer()
        except Exception as er:
            await self.session.rollback()
            raise HTTPException(status_code=400, detail=f'{type(er).__name__}: {str(er)}')

    async def get_all_data(
            self,
    ) -> AllQuestionAnswer | List:
        """
        Метод для записи полученных данных.

        :param data: словарь данных ответов и вопросов.
        :return: None или словарь.
        """
        async with self.session.begin():
            stmt = select(Answer)
            question = await self.session.execute(stmt)
            item_question = question.all()
            data = []
            for question in item_question:
                data.append(QuestionAnswer(**question[0].to_json()))

        return AllQuestionAnswer(questions=data)
