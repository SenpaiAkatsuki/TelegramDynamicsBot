from aiogram_dialog import Window
from aiogram_dialog.api.entities import MediaAttachment
from aiogram_dialog.widgets.input import TextInput, MessageInput
from aiogram_dialog.widgets.kbd import Button, Back, Row, SwitchTo, Cancel, Group, NumberedPager, PrevPage, NextPage, \
    CurrentPage
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Const, Format, Multi

from tgbot.dialog.bot_menu import getters, keyboards, selected
from tgbot.dialog.bot_menu.selected import on_confirm_add_notification
from tgbot.dialog.bot_menu.states import MainMenu, GroupManagementAddGroup, \
    GroupManagement, GroupManagementGroupSettings, NotificationManagement, ControlPanel, AllInWork
from tgbot.misc.widgets import ScrollingText


def main_menu_window():
    return Window(
        Const('Головне меню'),
        keyboards.main_menu(),
        state=MainMenu.select_category,
    )


def manage_groups_select_option():
    return Window(
        Const('👥 Керування групами'),
        keyboards.group_management(),
        Cancel(Const('<< Назад'),
               id='cancel_to_main_menu', ),
        state=GroupManagement.group_management
    )


def scrolling_statuses():
    return Window(
        Const('📩 Статуси розсилок'),
        ScrollingText(
            Format('{notification_statuses}'),
            id='scrolling_statuses',
            when='notification_statuses',
            page_size=40,
        ),
        Row(
            PrevPage(scroll="scrolling_statuses"),
            CurrentPage(scroll="scrolling_statuses"),
            NextPage(scroll="scrolling_statuses"),
        ),
        Cancel(Const('<< Назад')),
        state=selected.NotificationStatus.show_notification,
        getter=getters.get_notifications,
        disable_web_page_preview=True,
    )


def choose_group():
    return Window(
        Const('🔧 Оберіть группу'),
        keyboards.choose_group(),
        Cancel(Const('<< Назад'),
               id='ccl_to_gr_mae_frm_segs_TST',
               ),
        state=GroupManagementGroupSettings.group_settings,
        getter=getters.get_groups
    )


def select_scheduled_time():
    return Window(
        Multi(
            Const('⏰ Задайте час постингу у форматі: 00:00'),
            Format('{group_settings}', when='group_settings'),
        ),
        TextInput(id='enter_schedule_time',
                  on_success=selected.on_enter_schedule_time),
        SwitchTo(
            Const('🗑 Вилучити групу'),
            id='delete_group',
            state=GroupManagementGroupSettings.delete_group,
        ),
        Back(Const('<< Назад')),
        state=GroupManagementGroupSettings.group_scheduled_time,
        getter=getters.get_group_settings
    )


def confirm_delete_group():
    return Window(
        Const('Ви впевнені що хочете вилучити групу?'),
        Button(Const('Так'),
               id='confirm_delete_group',
               on_click=selected.on_confirm_delete_group),

        SwitchTo(Const('<< Назад'),
                 id='back_to_group_settings',
                 state=GroupManagementGroupSettings.group_scheduled_time),
        state=GroupManagementGroupSettings.delete_group,
    )


def select_scheduled_period():
    return Window(
        Format('⏰ Час постингу <b>{schedule_time}</b> для групи <b>{group_name}</b>\n'
               '🔁 виберіть періодичність постингу'),
        keyboards.choose_scheduled_period(),
        Back(Const('<< Назад до списку груп')),
        state=GroupManagementGroupSettings.group_scheduled_period,
        getter=getters.get_schedule_time
    )


def select_scheduled_custom_period():
    return Window(
        Const('🔁 Введіть періодичність постингу у форматі: 00/00'),
        TextInput(id='enter_schedule_custom_period',
                  on_success=selected.on_enter_schedule_custom_period),
        SwitchTo(Const('<< Назад до списку груп'),
                 id='cancel_from_custom_period',
                 state=GroupManagementGroupSettings.group_settings),
        state=GroupManagementGroupSettings.group_custom_scheduled_period
    )


def select_scheduled_custom_period_exception():
    return Window(
        Const('Схоже що ви ввели невірний формат періодичності постингу, спробуйте ще раз'),
        TextInput(id='enter_schedule_custom_period_error',
                  on_success=selected.on_enter_schedule_custom_period),
        SwitchTo(Const('<< Назад до списку груп'),
                 id='cancel_to_group_manage_from_settings',
                 state=GroupManagementGroupSettings.group_settings),
        state=GroupManagementGroupSettings.group_custom_scheduled_period_exception
    )


def group_scheduled_complete():
    return Window(
        Const('Готово!'),
        Cancel(Const('<< Назад'),
               id='ccl_to_gr_mae_frm_segs_TST',
               ),
        state=GroupManagementGroupSettings.group_scheduled_complete
    )


def get_new_group():
    return Window(
        Const("Відправте боту <b>ID</b> групи"),
        TextInput(id='enter_group_name',
                  on_success=selected.on_enter_group_id),
        Cancel(Const('<< Назад'),
               id='cancel_to_group_manage_from_add_group',
               ),
        state=GroupManagementAddGroup.add_group,
    )


def enter_group_name():
    return Window(
        Const("Відправте <b>Назву</b> групи"),
        TextInput(id='enter_group_name',
                  on_success=selected.on_enter_group_name),
        SwitchTo(Const('<< Назад'),
                 id='cancel_to_group_manage_from_add_group',
                 state=GroupManagementAddGroup.add_group,
                 ),
        state=GroupManagementAddGroup.enter_group_name,
    )


def confirm_new_group():
    return Window(
        Format('''
Група {group_name} додана до списку групп
        '''),
        Cancel(Const('<< Назад до меню'),
               id='cancel_to_menu_groups',
               ),
        state=GroupManagementAddGroup.confirm_group,
        getter=getters.get_group_name,
    )


# =============================================== #


def get_notification():
    return Window(
        Const('Повідомлення'),
        Group(
            Button(Const('📂 Шаблони'), id='preset_settings',
                   on_click=selected.on_choose_template_from_notification_management),
            Button(Const('Створити повідомлення'), id='add_notification', on_click=selected.on_add_notification),
        ),
        Cancel(Const('<< Назад до головного меню'),
               id='cancel_to_group_manage_from_notification',
               ),
        state=NotificationManagement.notification_management
    )


def add_notification():
    return Window(
        Const('Відправте боту те що бажаєте опублікувати (готовий месседж з фото або без)'),
        MessageInput(on_confirm_add_notification),
        Back(Const('<< Назад')),
        state=NotificationManagement.add_notification,
    )


def enter_name_for_template():
    return Window(
        Const('📋✍️ Введіть назву шаблону, або оберіть зі списку, щоб перезаписати'),
        keyboards.choose_template(),
        TextInput(id='enter_name_for_template',
                  on_success=selected.on_enter_name_template),
        Back(Const('<< Назад')),
        state=NotificationManagement.enter_name_for_template,
        getter=getters.get_templates
    )


def choose_template():
    return Window(
        Const('Оберіть шаблон'),
        keyboards.choose_template(),
        SwitchTo(Const('« Назад'),
                 id='cancel_to_notification_from_choose_template',
                 state=NotificationManagement.notification_management),
        state=NotificationManagement.choose_template,
        getter=getters.get_templates
    )


def choose_group_for_notification():
    return Window(
        Multi(
            Format('{template_text}'),
            Const('📢Оберіть канал для постінгу'),
            sep='\n\n'
        ),
        DynamicMedia(
            selector='photo',
            when='photo'
        ),
        keyboards.choose_group_for_notification(),
        SwitchTo(
            Const('🗑 Вилучити шаблон'),
            id='delete_template',
            state=NotificationManagement.delete_template
        ),
        SwitchTo(
            Const('« Назад до шаблонів'),
            id='back_to_templates',
            state=NotificationManagement.choose_template
        ),
        SwitchTo(Const('<< Назад до меню'),
                 id='ccl_to_ntf_from_chse_gp',
                 state=NotificationManagement.notification_management),

        state=NotificationManagement.choose_group_for_notification,
        disable_web_page_preview=True,
        getter=(
            getters.get_groups,
            getters.get_template_info
        )
    )


def confirm_delete_template():
    return Window(
        Const('Видалити шаблон?'),
        Button(Const('Так'),
               id='confirm_delete_template',
               on_click=selected.on_confirm_delete_template),
        SwitchTo(Const('Ні'),
                 id='cancel_delete_template',
                 state=NotificationManagement.choose_group_for_notification),
        state=NotificationManagement.delete_template
    )


def choose_notification_options():
    return Window(
        Const('Оберіть опції для розсилки'),
        Button(Const('🚀 Старт зараз!'),
               id='start_now',
               on_click=selected.on_start_posting_message),
        Button(Const('🕰️ Запланувати розсилку'),
               id='start',
               on_click=selected.on_start_posting_message),
        Button(Const('⏸️ Пауза'),
               id='pause',
               on_click=selected.on_start_posting_message),
        Button(Const('⛔️ Стоп'),
               id='stop',
               on_click=selected.on_start_posting_message),
        Back(Const('<< Назад')),
        state=NotificationManagement.choose_notification_options,
    )


def choose_group_for_notification_exception():
    return Window(
        Const('Схоже у вас немає налаштувань для цієї групи\n\n'
              'Оберіть канал для постінгу'),
        keyboards.choose_group_for_notification(),
        Cancel(Const('<< Налаштування груп'),
               id='cl_to_non_fm_cse_gup'),
        SwitchTo(Const('<< Назад до меню'),
                 id='cel_to_noion_fm_cse_grp',
                 state=NotificationManagement.notification_management),
        state=NotificationManagement.choose_group_for_notification_exceptiom,
        getter=getters.get_groups
    )


def notification_complete():
    return Window(
        Const('Готово!'),
        SwitchTo(Const('<< Назад до меню'),
                 id='cancel_to_notification_from_choose_group',
                 state=NotificationManagement.notification_management),
        state=NotificationManagement.notification_complete,
    )


# =================== #

def control_panel():
    return Window(
        Const('Панель керування'),
        SwitchTo(Const('💼 Всі в роботі'),
                 id='all_in_work',
                 state=ControlPanel.control_option_all_in_bot),
        Row(
            Button(Const('⛔️ Всі стоп'),
                   id='all_stop',
                   on_click=selected.on_select_control_option),
            Button(Const('🚀 Всі старт'),
                   id='all_start',
                   on_click=selected.on_select_control_option),
        ),
        Cancel(Const('<< Назад до меню'),
               id='cel_to_mu_fm_crl_pal', ),
        state=ControlPanel.control_panel,
    )


def control_option_set():
    return Window(
        Const('Готово!'),
        SwitchTo(Const('<< Назад до меню'),
                 id='cl_to_mu_fom_cl_oon_st',
                 state=ControlPanel.control_panel),
        state=ControlPanel.control_option_set,
    )


def control_option_all_in_bot():
    return Window(
        Const('Групи повідомлень'),
        keyboards.templates_from_scheduled_messages(),

        SwitchTo(Const('<< Назад до меню'),
                 id='cl_to_mu_from_ctl_opn_all',
                 state=ControlPanel.control_panel),
        state=ControlPanel.control_option_all_in_bot,
        getter=getters.get_templates_from_scheduled_messages
    )


def all_in_bot_template_info():
    return Window(
        DynamicMedia(
            selector='template_photo',
            when='template_photo'
        ),
        Multi(
            Format('Інформація про шаблон: "{template_name}"'),
            Format('Текст: "{template_text}"'),
            ScrollingText(
                Format('{statuses}'),
                id='all_in_work_scroll',
                page_size=15,
            ),
            sep='\n\n'
        ),
        Row(
            PrevPage(scroll="all_in_work_scroll"),
            CurrentPage(scroll="all_in_work_scroll"),
            NextPage(scroll="all_in_work_scroll"),
        ),
        Cancel(Const('<< Назад до повідомлень'),
               id='cel_to_mu_fr_all_in_bt_tte_io',
               ),
        state=AllInWork.show_statuses,
        getter=getters.get_info_from_template,
        disable_web_page_preview=True
    )
