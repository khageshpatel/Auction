import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio

async def test_root(async_client: AsyncClient):
    response = await async_client.get("/")
    assert response.status_code == 404

async def test_user_info(async_client: AsyncClient):
    response = await async_client.post("/user/user_create", json={'full_name': "john doe"})
    assert response.status_code == 200
    response = await async_client.get("/user/user_info?uuid=" + str(response.json()['user_id']))
    assert response.status_code == 200