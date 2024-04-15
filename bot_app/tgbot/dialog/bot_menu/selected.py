import asyncio
import logging
import re
from collections import defaultdict
from datetime import timedelta, datetime

from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Select, Button

from infrastructure.database.functions.repo import Repo
from tgbot.dialog.bot_menu.states import GroupManagementAddGroup, \
    GroupManagement, GroupManagementGroupSettings, NotificationManagement, NotificationStatus, ControlPanel, AllInWork
from tgbot.services.telegraph.uploader import TelegraphService


async def on_group_management(c: CallbackQuery, widget: Select, manager: DialogManager):
    await manager.start(GroupManagement.group_management)


async def on_group_settings(c: CallbackQuery, widget: Select, manager: DialogManager):
    await manager.start(GroupManagementGroupSettings.group_settings)


async def on_control_panel(c: CallbackQuery, widget: Select, manager: DialogManager):
    await manager.start(ControlPanel.control_panel)


# ===================== #

async def on_add_group(c: CallbackQuery, widget: Select, manager: DialogManager):
    await manager.start(GroupManagementAddGroup.add_group)


async def on_enter_group_id(m: Message, widget: TextInput, manager: DialogManager, group_id: str):
    ctx = manager.current_context()

    session = manager.middleware_data.get('session')
    bot = manager.middleware_data.get('bot')
    ctx.dialog_data.update(group_id=group_id)
    await manager.switch_to(GroupManagementAddGroup.enter_group_name)


async def on_enter_group_name(m: Message, widget: TextInput, manager: DialogManager, group_name: str):
    ctx = manager.current_context()
    session = manager.middleware_data.get('session')
    bot = manager.middleware_data.get('bot')
    group_id = ctx.dialog_data.get('group_id')
    ctx.dialog_data.update(group_name=group_name)
    await Repo.create_group(session, group_id=int(group_id), group_name=group_name)
    await session.commit()
    await manager.switch_to(GroupManagementAddGroup.confirm_group)


async def on_enter_schedule_time(m: Message, widget: TextInput, manager: DialogManager, schedule_time: str):
    ctx = manager.current_context()
    pattern = r'^(0\d|1\d|2[0-3]):([0-5]\d)$'

    if re.match(pattern, schedule_time):
        ctx.dialog_data.update(schedule_time=schedule_time)
        await manager.switch_to(GroupManagementGroupSettings.group_scheduled_period)
    else:
        await m.answer('Час має бути в форматі HH:MM')


async def on_time_settings(c: CallbackQuery, widget: Button, manager: DialogManager, group_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(group_id=group_id)
    session = manager.middleware_data.get('session')
    group = await Repo.get_group_by_id(session, group_id=int(group_id))
    if group:
        ctx.dialog_data.update(
            group_name=group.scalars().first().name,
        )
    await manager.switch_to(GroupManagementGroupSettings.group_scheduled_time)


async def confirm_schedule_settings(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    session = manager.middleware_data.get('session')
    # group_id = await Repo.get_group_id_by_name(session, group_name=ctx.dialog_data.get('group_name'))

    group_id = ctx.dialog_data.get('group_id')
    frequency, hours = widget.widget_id.split('_to_')
    await Repo.create_group_settings(session,
                                     group_id=int(group_id),  # group_id
                                     frequency=f'{frequency}/{hours}',
                                     start_time=ctx.dialog_data.get('schedule_time'),
                                     end_time='None',
                                     status='inactive'
                                     )
    await Repo.update_frequency_scheduled_messages(
        session,
        frequency=f'{frequency}/{hours}',
        group_id=int(group_id),
    )
    await session.commit()

    await manager.switch_to(GroupManagementGroupSettings.group_scheduled_complete)


def on_get_custom_schedule_period(c: CallbackQuery, widget: Button, manager: DialogManager):
    return manager.switch_to(GroupManagementGroupSettings.group_custom_scheduled_period)


async def on_enter_schedule_custom_period(m: Message, widget: TextInput, manager: DialogManager,
                                          schedule_frequency: str):
    ctx = manager.current_context()
    session = manager.middleware_data.get('session')
    group_id = ctx.dialog_data.get('group_id')
    pattern = r'^(\d+\/\d+)$'

    if re.match(pattern, schedule_frequency):

        schedule_time = ctx.dialog_data.get('schedule_time')
        await Repo.create_group_settings(session,
                                         group_id=int(group_id),
                                         frequency=schedule_frequency,
                                         start_time=schedule_time,
                                         end_time='None',
                                         status='inactive'
                                         )

        await Repo.update_time_scheduled_messages(
            session,
            next_send_time=datetime.today().replace(
                hour=int(schedule_time.split(':')[0]),
                minute=int(schedule_time.split(':')[1]),
            ),
            group_id=int(group_id),
        )

        await session.commit()
        await manager.switch_to(GroupManagementGroupSettings.group_scheduled_complete)
    else:
        await manager.switch_to(GroupManagementGroupSettings.group_custom_scheduled_period_exception)


# =================== #


async def on_notification_management(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.start(NotificationManagement.notification_management)


async def on_add_notification(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(NotificationManagement.add_notification)


async def on_choose_template_from_notification_management(c: CallbackQuery, widget: Button, manager: DialogManager):
    await manager.switch_to(NotificationManagement.choose_template)


async def on_confirm_add_notification(m: Message, widget: MessageInput, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.clear()
    if m.text:
        ctx.dialog_data.update(text=m.html_text)
        await manager.switch_to(NotificationManagement.enter_name_for_template)
    elif m.photo:
        photo = m.photo[-1]
        telegraph_uploader: TelegraphService = manager.middleware_data.get('telegraph_uploader')
        bot = manager.middleware_data.get('bot')
        uploaded_photo = await telegraph_uploader.upload_photo(bot, photo)
        ctx.dialog_data.update(photo=uploaded_photo.link)
        ctx.dialog_data.update(caption=m.html_text)
        await manager.switch_to(NotificationManagement.enter_name_for_template)
    elif m.document:
        await m.reply(
            'Документы не поддерживаются, попробуйте отправить фото или текстовое сообщение'
        )


async def on_confirm_add_notification_cancel(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    ctx.dialog_data.clear()
    await manager.switch_to(NotificationManagement.add_notification)


async def on_enter_name_template(m: Message, widget: TextInput, manager: DialogManager, template_name: str):
    ctx = manager.current_context()
    session = manager.middleware_data.get('session')

    ctx.dialog_data.update(template_name=template_name)

    template = await Repo.create_template(session,
                                          name=template_name,
                                          text=ctx.dialog_data.get('text'),
                                          caption=ctx.dialog_data.get('caption'),
                                          document=ctx.dialog_data.get('document'),
                                          photo=ctx.dialog_data.get('photo')
                                          )

    await session.commit()
    manager.dialog_data.update(template_id=template.template_id)
    await manager.switch_to(NotificationManagement.choose_group_for_notification)


async def on_add_template(c: CallbackQuery, widget: Select, manager: DialogManager):
    await manager.switch_to(NotificationManagement.enter_name_for_template)


async def on_choose_group_notification(c: CallbackQuery, widget: Select, manager: DialogManager):
    await manager.switch_to(NotificationManagement.choose_group_for_notification)


async def on_choose_group_from_templates(c: CallbackQuery, widget: Select, manager: DialogManager, template_id: str):
    ctx = manager.current_context()
    session = manager.middleware_data.get('session')
    ctx.dialog_data.update(template_id=int(template_id))
    new_template_data = {
        key: value for key, value in ctx.dialog_data.items() if key in ['text', 'photo',
                                                                        'caption', 'document']
    }
    if new_template_data:
        await Repo.update_template(
            session,
            template_id=int(template_id),
            **new_template_data
        )
        logging.info(f'template updated: {new_template_data}')
        await session.commit()
    await manager.switch_to(NotificationManagement.choose_group_for_notification)


async def on_options_for_notification(c: CallbackQuery, widget: Select, manager: DialogManager, group_id: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(group_id=group_id)
    await manager.switch_to(NotificationManagement.choose_notification_options)


async def on_confirm_delete_template(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    session = manager.middleware_data.get('session')
    template_id = ctx.dialog_data.get('template_id')
    await Repo.delete_template(session, template_id=int(template_id))
    await session.commit()
    await c.answer('Шаблон вилучено!', show_alert=True)
    await manager.switch_to(NotificationManagement.choose_template)


async def on_start_posting_message(c: CallbackQuery, widget: Button, manager: DialogManager):
    session = manager.middleware_data.get('session')
    ctx = manager.current_context()

    group_id = int(ctx.dialog_data.get('group_id'))

    group_settings = await Repo.get_group_settings_by_group_id(session, group_id=group_id)

    group_settings = group_settings.first()
    if not group_settings:
        # if not group_settings then create group_settings at 1/24 and 09:00
        group_settings = await Repo.create_group_settings(session, group_id=group_id, frequency='1/24',
                                                          start_time='09:00',
                                                          status=widget.widget_id, end_time='23:00')
    # next time calculation
    numerator, denominator = map(int, group_settings.frequency.split('/'))
    result = (denominator / numerator)

    time_obj = datetime.strptime(group_settings.start_time, '%H:%M')
    datetime_obj = datetime.combine(datetime.today(), time_obj.time())
    delta = timedelta(minutes=int(result * 60))
    next_time_obj = datetime_obj + delta

    template_id = ctx.dialog_data.get('template_id')
    template_id = int(template_id)
    if widget.widget_id == 'pause':
        await Repo.update_status_in_scheduled_message_template(session,
                                                               scheduled_group_id=group_id,
                                                               scheduled_template_id=template_id,
                                                               status="paused")
    elif widget.widget_id == 'stop':
        await Repo.update_status_in_scheduled_message_template(session,
                                                               scheduled_group_id=group_id,
                                                               scheduled_template_id=template_id,
                                                               status="stopped")
    elif widget.widget_id == 'start':
        await Repo.create_scheduled_message(session,
                                            send_time=group_settings.start_time,
                                            next_send_time=next_time_obj,
                                            frequency=group_settings.frequency,
                                            template_id=template_id,
                                            group_id=group_id,
                                            status="scheduled",
                                            # do_update=False)
                                            )
    elif widget.widget_id == 'start_now':
        next_send_time: datetime = datetime.now() + timedelta(minutes=2)

        await Repo.create_scheduled_message(session,
                                            send_time=next_send_time.time().strftime('%H:%M'),
                                            next_send_time=next_send_time,
                                            frequency=group_settings.frequency,
                                            template_id=template_id,
                                            group_id=group_id,
                                            status="scheduled")
    await session.commit()
    await c.answer('Готово!', show_alert=True)
    # await manager.switch_to(NotificationManagement.notification_complete)


async def on_confirm_delete_group(c: CallbackQuery, widget: Button, manager: DialogManager):
    session = manager.middleware_data.get('session')
    ctx = manager.current_context()
    group_id = ctx.dialog_data.get('group_id')
    await Repo.delete_group(session, group_id=int(group_id))
    await session.commit()
    await c.answer('Группа удалена')
    await manager.done()


# ======================== #

async def on_select_control_option(c: CallbackQuery, widget: Button, manager: DialogManager):
    ctx = manager.current_context()
    session = manager.middleware_data.get('session')

    if widget.widget_id == 'all_stop':
        await Repo.update_status_to_all_scheduled_messages(session, status="stopped")
    else:
        await Repo.update_status_to_all_scheduled_messages(session, status="scheduled")

    await session.commit()
    await manager.switch_to(ControlPanel.control_option_set)


async def choose_template_for_all(c: CallbackQuery, widget: Button, manager: DialogManager, template_name: str):
    ctx = manager.current_context()
    ctx.dialog_data.update(template_name_for_info=template_name)
    await manager.start(AllInWork.show_statuses,
                        data=ctx.dialog_data)
