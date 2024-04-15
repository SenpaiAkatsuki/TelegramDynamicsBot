from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode

from tgbot.dialog.bot_menu.states import MainMenu
from tgbot.filters.admin import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(message: Message, session, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenu.select_category, mode=StartMode.RESET_STACK)

