import re

from aiogram import Router, F
from aiogram.filters import Command

from infrastructure.database.functions.repo import Repo

commands_router = Router()


@commands_router.message(F.text.regexp(r'/stop_(\d+)').as_('match_message_id'))
async def stop_scheduled_message_command(message, match_message_id: re.Match, session):
    await Repo.update_scheduled_message_status(session, int(match_message_id.group(1)), status='stopped')
    await session.commit()
    await message.answer('Повідомлення зупинено!')

@commands_router.message(F.text.regexp(r'/start_(\d+)').as_('match_message_id'))
async def start_scheduled_message_command(message, match_message_id: re.Match, session):
    await Repo.update_scheduled_message_status(session, int(match_message_id.group(1)), status='scheduled')
    await session.commit()
    await message.answer('Повідомлення запущено!')
