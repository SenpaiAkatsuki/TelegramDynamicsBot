import logging
import operator

from aiogram_dialog.widgets.kbd import ScrollingGroup, Select, Button, Group, Radio, Row, SwitchTo, Start
from aiogram_dialog.widgets.text import Format, Const

from tgbot.dialog.bot_menu import selected

SCROLLING_HEIGHT = 6


def main_menu():
    return Group(
        Button(Const('💬 Повідомлення'), id='notification_manage',
               on_click=selected.on_notification_management),
        Row(
            Button(Const('👥 Керування групами'), id='group_manage', on_click=selected.on_group_management),
            Start(Const('🔍 Статуси повідомлень'), id='notification_status', state=selected.NotificationStatus.show_notification)
        ),
        Button(Const('📩 Керування розсилками'), id='group_status', on_click=selected.on_control_panel),
        id='main_menu'
    )


def group_management():
    return Group(
        Button(Const('⚙️ Налаштування'), id='group_settings', on_click=selected.on_group_settings),
        Button(Const('👥 Додати групу'), id='add_group', on_click=selected.on_add_group),
    )


def choose_group():
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),  # Group name
            id='s_scroll_groups',
            item_id_getter=operator.itemgetter(1),
            items='groups',
            on_click=selected.on_time_settings,
        ),
        id='groups_ids',
        width=1, height=SCROLLING_HEIGHT,
    )


def choose_scheduled_period():
    return Group(
        Row(
            Button(Const('1/24'), id='1_to_24', on_click=selected.confirm_schedule_settings),
            Button(Const('2/24'), id='2_to_24', on_click=selected.confirm_schedule_settings),
            Button(Const('3/24'), id='3_to_24', on_click=selected.confirm_schedule_settings),
            Button(Const('4/24'), id='4_to_24', on_click=selected.confirm_schedule_settings),
        ),
        Button(Const('⚙️ Задати свій період'), id='custom_period', on_click=selected.on_get_custom_schedule_period),
        id='choose_scheduled_period'
    )


# =================== #


def choose_template():
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),  # Template name
            id='s_scroll_templates',
            item_id_getter=operator.itemgetter(1),
            items='templates',
            on_click=selected.on_choose_group_from_templates,
        ),
        id='templates_ids',
        width=1, height=SCROLLING_HEIGHT,
    )


def choose_group_for_notification():
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),  # Group name
            id='s_scroll_groups',
            item_id_getter=operator.itemgetter(1),
            items='groups',
            on_click=selected.on_options_for_notification,
        ),
        id='groups_ids',
        width=1, height=SCROLLING_HEIGHT,
    )


# =================== #

def templates_from_scheduled_messages():
    return ScrollingGroup(
        Select(
            Format('{item[0]}'),
            id='s_scroll_templates',
            item_id_getter=operator.itemgetter(0),
            items='scheduled',
            on_click=selected.choose_template_for_all,
        ),
        id='templates_ids',
        width=1, height=SCROLLING_HEIGHT,
    )
