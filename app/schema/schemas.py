import datetime
from typing import List
from pydantic import BaseModel, Field, ConfigDict


class Question(BaseModel):
    questions_num: int = Field(
        default=1, description="Количество вопросов", gt=0
    )


class QuestionAnswer(BaseModel):
    id: int | None = None
    question_id: int | None = None
    question: str | None = None
    answer: str
    created_at: datetime.datetime | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": 13,
                    "question_id": 1223,
                    "question": "David Duchovny & Gillian Anderson are FBI special agents Mulder & Scully on this series",
                    "answer": "The X-Files",
                    "created_at": datetime.datetime(2023, 12, 30, 12, 34, 56)
                },
            ]
        }
    }


class AllQuestionAnswer(BaseModel):
    questions: List[QuestionAnswer]


class Failure(BaseModel):
    result: bool = False
    error_type: str
    error_message: str
