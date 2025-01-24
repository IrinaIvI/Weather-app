from fastapi import FastAPI
from routers import router
from dao import scheduler
import logging
from contextlib import asynccontextmanager
from dao import delete_old_weather_report
from apscheduler.triggers.cron import CronTrigger

logging.basicConfig(level=logging.INFO)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        scheduler.add_job(delete_old_weather_report, CronTrigger(hour=0, minute=0))
        scheduler.start()
        yield
    except Exception as e:
        logging.info(f"Ошибка инициализации планировщика: {e}")
    finally:
        scheduler.shutdown(wait=True)

app = FastAPI(title="Weather App", lifespan=lifespan)

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
