import pytest
from .conftest import client


@pytest.mark.asyncio
async def test_add_question(client):
    response = await client.post(
        "/api/answer",
        json={
            "questions_num": 5,
        },
    )
    result = response.json()

    assert response.status_code == 201
    assert 'question' in result
    assert 'answer' in result


@pytest.mark.asyncio
async def test_get_question(client):
    response = await client.get("/api/answer/all")
    assert response.status_code == 200
