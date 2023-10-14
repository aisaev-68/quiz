from datetime import datetime
from typing import Dict, Any
from sqlalchemy import DateTime
from sqlalchemy import Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

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
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    question_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False)
    question: Mapped[str] = mapped_column(String(300), nullable=False)
    answer: Mapped[str] = mapped_column(String(200), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime())

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

    def to_json(self) -> Dict[str, Any]:
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
