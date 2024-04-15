from aiogram import Dispatcher, Router
from aiogram_dialog import DialogRegistry
from . import bot_menu


def setup_dialogs(dp: Dispatcher):
    registry = DialogRegistry()
    dg_router = Router()
    for dialog in [
        *bot_menu.bot_menu_dialogs(),
    ]:
        registry.register(dialog, router=dg_router)
    dp.include_router(dg_router)
    registry.setup_dp(dp)


