from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram_dialog import StartMode, DialogManager

router_test = Router()


@router_test.message(CommandStart())
async def user_start(message: Message, dialog_manager: DialogManager):
    await message.answer('TEST')

# # # Optional handler for default users
