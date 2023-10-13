import pytest
from sqlalchemy.sql import select

from .conftest import async_db
from app.models.models import Answer


@pytest.mark.asyncio
async def test_get_data(async_db):
    response = await async_db.session.execute(select(Answer))
    print(response)

    # result = response.json()
    #
    # assert response.status_code == 201
    # assert 'question' in result
    # assert 'answer' in result