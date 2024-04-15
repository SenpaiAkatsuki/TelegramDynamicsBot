import asyncio
import datetime
import logging
import random

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from pyrogram import Client
from pyrogram.enums import ParseMode
from sqlalchemy.orm import sessionmaker

from infrastructure.database.functions.repo import Repo


async def poll_db_and_mailing(client: Client, session: sessionmaker):
    async for dialog in client.get_dialogs():
        await asyncio.sleep(random.randint(1, 50) / 100)

    async with session() as session:
        messages = await Repo.get_all_scheduled_messages(session)
        for message in messages:
            status = None
            if message.Template.text:
                logging.info(f'Message: {message.Template.text}')
                try:
                    m = await client.send_message(
                        chat_id=message.ScheduledMessage.group_id,
                        text=message.Template.text,
                        disable_web_page_preview=True,
                        parse_mode=ParseMode.HTML
                    )

                    status = 'success'

                except Exception as e:
                    logging.exception(e)
                    status = 'failed'
                    m = None

            elif message.Template.photo:
                try:
                    m = await client.send_photo(
                        chat_id=message.ScheduledMessage.group_id,
                        photo=message.Template.photo,
                        caption=message.Template.caption,
                        parse_mode=ParseMode.HTML
                    )
                    status = 'success'
                except Exception as e:
                    m = None
                    logging.exception(e)
                    status = 'failed'
            if status:
                await Repo.update_status_in_scheduled_message_messages(
                    session, status,
                    message.ScheduledMessage.scheduled_message_id,
                    m.link if m else None
                )
                # next time calculation
                numerator, denominator = map(int, message.ScheduledMessage.frequency.split('/'))
                result = (denominator / numerator)

                delta = datetime.timedelta(minutes=int(result * 60))
                next_time_obj = datetime.datetime.now() + delta

                await Repo.create_scheduled_message(
                    session,
                    message.ScheduledMessage.send_time,
                    next_time_obj,
                    message.ScheduledMessage.frequency,
                    message.ScheduledMessage.group_id,
                    'scheduled',
                    message.Template.template_id,
                    do_update=False,
                )
                await session.commit()
            await asyncio.sleep(random.randint(1, 5))


def setup_jobs(schedule: AsyncIOScheduler):
    schedule.add_job(
        poll_db_and_mailing,
        trigger=CronTrigger(minute='*/1'),
        next_run_time=datetime.datetime.now(),
        id='start_polling_db',
        replace_existing=True
    )
