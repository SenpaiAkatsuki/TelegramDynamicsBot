from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_commands(bot: Bot):
    commands = [
        ("start", "Начать работу с ботом"),
    ]
    await bot.set_my_commands([
        BotCommand(command=command, description=description)
        for command, description in commands
    ])
