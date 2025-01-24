from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
import logging
logging.basicConfig(level=logging.INFO)
# job_stores = {
#     'default': SQLAlchemyJobStore(url="sqlite:///./jobs.sqlite")
# }
async_scheduler = AsyncIOScheduler()
async_scheduler.add_jobstore('sqlalchemy', url='sqlite:///./jobs.sqlite')


async def start_scheduler():
    if not async_scheduler.running:
        async_scheduler.start()


async def stop_scheduler():
    if async_scheduler.running:
        async_scheduler.shutdown(wait=True)