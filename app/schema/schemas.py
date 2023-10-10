import datetime
from typing import List
from pydantic import BaseModel


class Question(BaseModel):
    questions_num: int


class QuestionAnswer(BaseModel):
    id: int
    question_id: int
    question: str
    answer: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            'title': 'Answer',
            'description': 'Example answer list',
            'example':
                {
                    'id': 13,
                    'question_id': 1223,
                    'question': 'David Duchovny & Gillian Anderson are FBI special agents Mulder & Scully on this series',
                    'answer': 'The X-Files',
                    'created_at': datetime.datetime(2023, 12, 30, 12, 34, 56)
                },
        }


class AllQuestionAnswer(BaseModel):
    questions: List[QuestionAnswer]


class EmptyQuestion(BaseModel):
    question: str = None


class Failure(BaseModel):
    result: bool = False
    error_type: str
    error_message: str
