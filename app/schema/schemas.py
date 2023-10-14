import datetime
from typing import List
from pydantic import BaseModel, Field, ConfigDict


class Question(BaseModel):
    questions_num: int = Field(
        default=1, description="Количество вопросов", gt=0
    )


class QuestionAnswer(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int | None = Field(
        default=None, json_schema_extra={'examples': [13]}
    )
    question_id: int | None = Field(
        default=None, json_schema_extra={'examples': [13333]}
    )
    question: str | None = Field(
        default=None, json_schema_extra={'examples': ["David Duchovny & Gillian Anderson are FBI special agents Mulder & Scully on this series"]}
    )
    answer: str | None = Field(
        default=None, json_schema_extra={'examples': ["The X-Files"]}
    )
    created_at: datetime.datetime | None = Field(
        default=None, json_schema_extra={'examples': ["The X-Files"]}
    )


class AllQuestionAnswer(BaseModel):
    questions: List[QuestionAnswer]


class Failure(BaseModel):
    result: bool = False
    error_type: str
    error_message: str
