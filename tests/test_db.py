import datetime
import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from .conftest import get_db
from app.models.models import Answer


@pytest.mark.asyncio
async def test_add_get_data(get_db: AsyncSession):
    add_data = Answer(
        question_id=14499,
        question='Test question55',
        answer='Test answer55',
        created_at=datetime.datetime(2023, 12, 30, 12, 34, 56)
    )
    get_db.add(add_data)
    await get_db.flush()
    await get_db.commit()

    stmt = select(Answer).where(Answer.question == "Test question55")
    result = await get_db.execute(stmt)
    quest = result.scalars().first()
    assert quest.id == add_data.id
