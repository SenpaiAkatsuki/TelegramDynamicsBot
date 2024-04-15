import itertools
import logging
from collections import defaultdict

from aiogram.utils.markdown import hlink
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment

from infrastructure.database.functions.repo import Repo


async def get_groups(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data['session']
    query = await Repo.get_all_groups(session)
    groups = query.all()

    data = {
        'groups': [
            [f'{group.name}', group.group_id]
            for (group,) in groups
        ]
    }
    logging.info(data)
    return data


async def get_group_name(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data['session']
    ctx = dialog_manager.current_context()
    group_name = ctx.dialog_data.get('group_name')

    await session.commit()

    data = {
        'group_name': group_name
    }
    return data


async def get_schedule_time(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()
    schedule_time = ctx.dialog_data.get('schedule_time')
    group_name = ctx.dialog_data.get('group_name')

    data = {
        'schedule_time': schedule_time,
        'group_name': group_name
    }
    return data


# =================== #

async def get_notification_message(dialog_manager: DialogManager, **middleware_data):
    ctx = dialog_manager.current_context()

    text = ctx.dialog_data.get('text')
    photo = ctx.dialog_data.get('photo')
    caption = ctx.dialog_data.get('caption')
    document = ctx.dialog_data.get('document')
    return {
        'text': text,
        'photo': photo,
        'caption': caption,
        'document': document
    }


async def get_templates(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data['session']
    templates = await Repo.get_all_templates(session)

    data = {
        'templates': [
            [f'#{template.template_id}. {template.name}', template.template_id]
            for template in templates
        ]
    }
    return data


# =================== #


async def get_group_settings(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data['session']
    ctx = dialog_manager.current_context()
    group_id = ctx.dialog_data.get('group_id')

    group = await Repo.get_group_settings_by_group_id(session, int(group_id))
    data = {}
    if group and (group := group.first()):
        logging.info(f'{group=}')

        data = {
            'group_settings': f'''
<b>Налаштування групи:</b>
🔹 <b>Назва:</b> {group.name}
🔹 <b>Ідентифікатор:</b> {group.group_id}
🔹 <b>Старт розсилки:</b> {group.start_time}
🔹 <b>Інтервал:</b> {group.frequency} 
    '''
        }
    return data


async def get_template_info(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data['session']
    ctx = dialog_manager.current_context()
    template_id = ctx.dialog_data.get('template_id')

    template = await Repo.get_template_by_id(session, int(template_id))
    template = template.first()
    if not template:
        await dialog_manager.done()
        return {}
    logging.info(f'{template=}')
    data = {
        'template_text': f'<b>Назва шаблону:</b> {template.name}\n\n'
                         f'<b>Текст:</b>\n' + (template.text or template.caption or '')
    }
    if template.photo:
        data['photo'] = MediaAttachment(
            'photo',
            url=template.photo,
        )
    return data


async def get_notifications(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('session')
    notifications = await Repo.get_all_scheduled_statuses(session)
    # Firstly we group messages by date:
    dates = defaultdict(list)
    for status, template_id, template_name, group_name, schedule_time, message_link in notifications:
        dates[schedule_time.strftime("%Y-%m-%d")].append((
            status, template_id, template_name, group_name, schedule_time, message_link
        ))

    # Secondly, we group messages by group name within each date:
    grouped_dates = defaultdict(list)
    for date, date_notifications in dates.items():
        groups = defaultdict(list)
        for status, template_id, template_name, group_name, schedule_time, message_link in date_notifications:
            groups[group_name].append(
                f'🔹 #{template_id} {template_name} - ' +
                ('🟢' +
                 hlink(schedule_time.strftime(" в %H:%M"), message_link or '')
                 if status == 'success' else
                 (f'🟠 Заплановано' if status == 'scheduled' else
                  f'🔴 Помилка' if status == 'failed' else
                  f'⚪️ На павзі' if status == 'paused' else
                  f'⚫️ Зупинено'
                  ) + schedule_time.strftime(' %H:%M')
                 )
            )
        grouped_dates[date].extend(
            list(f'🔻 {group_name}:\n' + '\n'.join(
                f'  {notification}' for notification in notifications
            ) for group_name, notifications in groups.items()
                 )
        )

    statuses = [
        f'<b>{date}</b>:\n' + '\n'.join(
            f'{grouped_date}' for grouped_date in grouped_dates
        ) for date, grouped_dates in grouped_dates.items()
    ]
    return {
        'notification_statuses': '\n\n'.join(statuses)
    }


async def get_all_in_work(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data.get('session')


async def get_delivered_message_status(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data['session']
    ctx = dialog_manager.current_context()
    template_name = ctx.dialog_data.get('template_name')

    template = await Repo.get_template_by_name(session, template_name)

    if template.photo:
        data = {
            'text': template.text,
            'photo': template.photo,
        }
    else:
        data = {
            'text': template.text,
        }
    return data


# =================== #

async def get_templates_from_scheduled_messages(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data['session']
    query = await Repo.get_all_scheduled_messages_template_ids(session)
    scheduled_messages = query.all()
    logging.info(scheduled_messages)

    data = {
        'scheduled': []
    }

    for scheduled_message in scheduled_messages:
        query_template = await Repo.get_template_by_id(session, scheduled_message.template_id)
        logging.info(query_template)
        template = query_template.first()
        logging.info(template)

        data['scheduled'].append([
            f'{template.name}', f'{template.template_id}']
        )

    return data


async def get_info_from_template(dialog_manager: DialogManager, **middleware_data):
    session = middleware_data['session']
    ctx = dialog_manager.current_context()
    template_name_for_info = ctx.start_data.get('template_name_for_info')

    template = await Repo.get_template_by_name(session, template_name_for_info)
    logging.info(template)

    scheduled_message_query = await Repo.get_scheduled_messages_from_template(session, template.template_id)
    scheduled_message_query = scheduled_message_query.all()
    scheduled_message_query.sort(key=lambda x: x[0].date(), reverse=True)
    groups = []
    for date, messages in itertools.groupby(scheduled_message_query, lambda x: x[0].date()):
        group_text = '\n'.join([f'  🔻 "{group_name}". ' + (
            (
                    '🟢' +
                    hlink(time.strftime(" в %H:%M"), message_link or '')
            )
            if status == 'success' else
            (f'🟠 Заплановано /stop_{message_id}' if status == 'scheduled' else
             f'🔴 Помилка' if status == 'failed' else
             f'⚪️ На павзі ' if status == 'paused' else
             f'⚫️ Зупинено  /start_{message_id}') + f' До відправки в {time.strftime(" %H:%M")}'
        )
                                for (time, status, group_name, message_link, message_id) in messages])
        groups.append((date, group_text))

    text = '\n\n'.join([
        f'🔹 <b>Дата: {date.strftime("%d.%m.%Y")}</b>\n'
        f'{group_text}'
        for date, group_text in groups])

    return {
        'template_name': template_name_for_info,
        'template_photo': MediaAttachment(
            'photo',
            url=template.photo,
        ) if template.photo else None,
        'template_text': template.text or template.caption or '',
        'statuses': text or 'Нет запланированных сообщений'
    }
