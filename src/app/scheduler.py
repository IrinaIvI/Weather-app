from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import logging
import sys
from os.path import dirname, abspath, join

BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
sys.path.insert(0, BASE_DIR)
DB_PATH = join(BASE_DIR, "jobs.sqlite")

STORE_URL = f"sqlite:///{DB_PATH}"

logging.basicConfig(level=logging.INFO)
job_stores = {
    'default': SQLAlchemyJobStore(url=STORE_URL)
}
async_scheduler = AsyncIOScheduler(job_stores=job_stores)


async def start_scheduler():
    if not async_scheduler.running:
        async_scheduler.start()
        logging.info("Шедулер запущен")


async def stop_scheduler():
    if async_scheduler.running:
        async_scheduler.shutdown(wait=True)
        logging.info("Шедулер остановлен")