from aiogram_dialog import Dialog

from tgbot.dialog.bot_menu import windows


def bot_menu_dialogs():
    return [
        Dialog(  # main menu branch
            windows.main_menu_window(),
        ),
        Dialog(
            windows.manage_groups_select_option()
        ),
        Dialog(  # new group branch
            windows.get_new_group(),
            windows.enter_group_name(),
            windows.confirm_new_group(),
            # windows.get_new_group_exception(),
        ),
        Dialog(  # group settings branch
            windows.choose_group(),
            windows.select_scheduled_time(),
            windows.select_scheduled_period(),
            windows.group_scheduled_complete(),
            windows.select_scheduled_custom_period(),
            windows.select_scheduled_custom_period_exception(),
            windows.confirm_delete_group(),
        ),
        Dialog(
            windows.scrolling_statuses(),
        ),
        Dialog(
            windows.get_notification(),
            windows.add_notification(),
            windows.enter_name_for_template(),
            # windows.add_notification_confirm(),
            windows.choose_template(),
            windows.choose_group_for_notification(),
            windows.choose_notification_options(),
            windows.choose_group_for_notification_exception(),
            windows.notification_complete(),
            windows.confirm_delete_template(),
        ),
        Dialog(
            windows.control_panel(),
            windows.control_option_set(),
            windows.control_option_all_in_bot(),
        ),
        Dialog(
            windows.all_in_bot_template_info(),
        )
    ]
