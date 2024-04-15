import asyncio
import logging
from pathlib import Path

from apscheduler.jobstores.redis import RedisJobStore
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.base import BaseScheduler
from apscheduler_di import ContextSchedulerDecorator
from pyrogram import Client
from sqlalchemy.orm import sessionmaker
from tzlocal import get_localzone

from config import Config, load_config
from infrastructure.database.functions.repo import create_session_pool
from jobs import setup_jobs


def setup_scheduler(client: Client, config: Config, session_pool):
    job_stores = {
        "default": RedisJobStore(
            db=2,
            host='redis_cache',
            password=config.redis.redis_pass,
            port=config.redis.redis_port,
            jobs_key="dispatched_trips_jobs", run_times_key="dispatched_trips_running"
        )
    }

    scheduler = ContextSchedulerDecorator(
        AsyncIOScheduler(jobstores=job_stores, timezone=str(get_localzone()))
    )

    scheduler.ctx.add_instance(scheduler, declared_class=BaseScheduler)
    scheduler.ctx.add_instance(session_pool, declared_class=sessionmaker)
    scheduler.ctx.add_instance(client, declared_class=Client)

    return scheduler


async def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    config = load_config('.env')
    session_pool = create_session_pool(
        config.db
    )

    client = Client(
        config.user.phone_number,
        phone_number=config.user.phone_number,
        api_id=config.user.api_id,
        api_hash=config.user.api_hash,
    )

    await client.start()

    scheduler = setup_scheduler(
        client=client,
        config=config,
        session_pool=session_pool
    )
    logging.info('Starting')
    setup_jobs(scheduler)
    scheduler.start()
    while True:
        await asyncio.sleep(1000)


if __name__ == '__main__':
    asyncio.run(main())
    logging.info('Exited ')
