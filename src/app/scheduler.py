from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.triggers.cron import CronTrigger
import logging
from dao import delete_old_weather_report
logging.basicConfig(level=logging.INFO)
job_stores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
}
async_scheduler = AsyncIOScheduler(job_stores=job_stores)
async_scheduler.add_job(delete_old_weather_report, CronTrigger(hour=0, minute=0))