from typing import AsyncGenerator

import pytest
import asyncio
from httpx import ASGITransport, AsyncClient
from time import monotonic

from main import app


@pytest.fixture
async def ac() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as client:
        yield client


async def test_single_request(ac):
    start = monotonic()
    response = await ac.get("/test")
    end = monotonic()

    assert response.status_code == 200

    json_response = response.json()
    assert "elapsed" in json_response
    assert isinstance(json_response["elapsed"], float)

    assert 2.9 <= json_response["elapsed"] <= 3.1

    assert 2.9 <= (end - start) <= 3.5


async def test_parallel_requests(ac):
    num_requests = 3

    responses = await asyncio.gather(*[ac.get("/test") for _ in range(num_requests)])

    elapsed_times = []
    for response in responses:
        assert response.status_code == 200
        json_response = response.json()
        elapsed_times.append(json_response["elapsed"])

    elapsed_diffs = [elapsed_times[i] - elapsed_times[i - 1] for i in range(1, len(elapsed_times))]
    for diff in elapsed_diffs:
        assert diff >= 2.9
