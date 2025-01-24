from fastapi import FastAPI
from src.app.routers import router
from src.app.scheduler import stop_scheduler, start_scheduler
import logging
from contextlib import asynccontextmanager


logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        await start_scheduler()
        yield
    except Exception as e:
        logging.info(f"Ошибка инициализации планировщика: {e}")
    finally:
        await stop_scheduler()

app = FastAPI(title="Weather App", lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
