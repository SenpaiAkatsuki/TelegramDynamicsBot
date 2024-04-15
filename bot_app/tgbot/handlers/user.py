from typing import Optional

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram_dialog import StartMode, DialogManager

from infrastructure.database.functions.repo import Repo

user_router = Router()

router_test = Router()


# class TestCallback(CallbackData, prefix='test'):
#     action: str
#
#
# def get_keyboard():
#     builder = InlineKeyboardBuilder()
#     builder.button(
#         text="test", callback_data=TestCallback(action='test')
#     )
#     builder.adjust(1)
#     return builder.as_markup()
#
#
# @router_test.message(CommandStart())
# async def user_start(message: Message, dialog_manager: DialogManager):
#     await message.answer('test',
#                          reply_markup=get_keyboard())
#
#
# @router_test.callback_query(TestCallback.filter(F.action == 'test'))
# async def user_start(call: CallbackQuery, dialog_manager: DialogManager):
#     await call.answer()
#     await call.message.answer('test2')
#     await dialog_manager.start(BotMenu.select_categories, mode=StartMode.RESET_STACK)

# @user_router.message(CommandStart())
# async def user_start(message: Message, session):
#     groups = await Repo.get_all_groups(session)
#     # await Repo.create_group(session, message.chat.id, 'test')
#     await message.reply(f"Вітаю, звичайний користувач! {groups}")
