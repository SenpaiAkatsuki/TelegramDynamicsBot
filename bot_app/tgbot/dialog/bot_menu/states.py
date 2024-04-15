from aiogram.fsm.state import StatesGroup, State


class MainMenu(StatesGroup):
    select_category = State()


# =================== #
class GroupManagement(StatesGroup):
    group_management = State()


class GroupManagementAddGroup(StatesGroup):
    add_group = State()
    confirm_group = State()
    enter_group_name = State()
    confirm_group_exception = State()


class GroupManagementGroupSettings(StatesGroup):
    group_settings = State()
    group_scheduled_time = State()
    group_scheduled_time_exception = State()
    group_scheduled_period = State()
    group_custom_scheduled_period = State()
    group_custom_scheduled_period_exception = State()
    group_scheduled_complete = State()
    delete_group = State()


# =================== #

class NotificationManagement(StatesGroup):
    notification_management = State()
    add_notification = State()
    # add_notification_confirm = State()
    save_template = State()
    enter_name_for_template = State()
    choose_template = State()
    choose_group_for_notification = State()
    choose_group_for_notification_exceptiom = State()
    choose_notification_options = State()
    notification_complete = State()
    delete_template = State()


# =================== #

class NotificationStatus(StatesGroup):
    notification_status = State()
    show_notification = State()


# =================== #

class ControlPanel(StatesGroup):
    control_panel = State()
    control_option_set = State()
    control_option_all_in_bot = State()
    all_in_work_scroll = State()


class AllInWork(StatesGroup):
    show_statuses = State()
