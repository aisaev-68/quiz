from datetime import datetime
from typing import Dict, Any, Union
from sqlalchemy import DateTime
from sqlalchemy import Column, Integer, String

from app.models.database import Base


class Answer(Base):
    """
    Модель вопросов и ответов.

    Атрибуты:
        id (int): ID ответа.
        id_question (int): ID вопроса.
        question (str): вопрос.
        answer (str): ответ.
        created_on (datetime): Дата создания вопроса.
    """
    __tablename__ = 'answer'
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, unique=True, nullable=False)
    question = Column(String(300), nullable=False)
    answer = Column(String(200), nullable=False)
    created_at = Column(DateTime())

    def __repr__(self) -> str:
        """
        Возвращает класс.
        :return: класс.
        """
        return self.__class__.__name__
        # return "{name} ({id}, {question_id}, {question}, {answer}, {created_at})".format(
        #     name=self.__class__.__name__,
        #     id=self.id,
        #     question_id=self.question_id,
        #     question=self.question,
        #     answer=self.answer,
        #     created_at=self.created_at
        # )

    def to_json(self) -> Dict[str, Union[str, int, datetime]]:
        """
        Возвращает данные в виде словаря.
        :return: словарь.
        """

        return {
            "id": self.id,
            "question_id": self.question_id,
            "question": self.question,
            "answer": self.answer,
            "created_at": self.created_at
        }
