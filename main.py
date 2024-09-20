from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from time import monotonic
import asyncio

app = FastAPI()
router = APIRouter()

work_lock = asyncio.Lock()

class TestResponse(BaseModel):
    elapsed: float


async def work() -> None:
    await asyncio.sleep(3)

@router.get("/test", response_model=TestResponse)
async def handler() -> TestResponse:
    ts1 = monotonic()

    async with work_lock:
        await work()

    ts2 = monotonic()
    return TestResponse(elapsed=ts2 - ts1)

app.include_router(router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
