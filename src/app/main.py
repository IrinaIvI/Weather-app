from fastapi import FastAPI
from routers import router
from scheduler import async_scheduler
import logging
from contextlib import asynccontextmanager

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        async_scheduler.start()
        yield
    except Exception as e:
        logging.info(f"Ошибка инициализации планировщика: {e}")
    finally:
        async_scheduler.shutdown(wait=True)

app = FastAPI(title="Weather App", lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
