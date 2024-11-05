from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from bot_data import BotData
from datetime import datetime
from date_generator import gen_week_days
from database import DataBase

bot_data = BotData()
db = DataBase()

def gen_days_kb():
    days = gen_week_days()

    cur_week_kb = [[InlineKeyboardButton(text=d[0], callback_data=f"set_d_{d[0]}_date_{d[1].date()}")] for d in days[0] if d[1]]
    next_week_kb = [[InlineKeyboardButton(text=d[0], callback_data=f"set_d_{d[0]}_date_{d[1].date()}_n")] for d in days[1] if d[1]]

    cur_week_days_kb = InlineKeyboardMarkup(inline_keyboard=
        cur_week_kb
    )

    next_week_days_kb = InlineKeyboardMarkup(inline_keyboard=
        next_week_kb
    )
    return (cur_week_days_kb, next_week_days_kb)


def get_back_to_subject_kb(week_is_current):
    if week_is_current:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Back", callback_data="back_to_subjects_c_d")]
        ])
    else:
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Back", callback_data="back_to_subjects_n_d")]
        ])

    return kb

def get_subjects_kb(day, week_is_current) -> InlineKeyboardMarkup:
    subjects = bot_data.days_subjects[day]
    
    if week_is_current:
        kb = [[InlineKeyboardButton(text=sb, callback_data=f"select_sub_{sb}")] for sb in subjects]
        kb.append([InlineKeyboardButton(text="Back", callback_data="back_to_cur_days")])
    else:
        kb = [[InlineKeyboardButton(text=sb, callback_data=f"select_sub_{sb}_n_d")] for sb in subjects]
        kb.append([InlineKeyboardButton(text="Back", callback_data="back_to_next_days")])
    return InlineKeyboardMarkup(inline_keyboard=kb)




def get_home_work_kb():
    days = gen_week_days()

    cur_week_kb = [[InlineKeyboardButton(text=d[0], callback_data=f"get_hm_{d[0]}_date_{d[1].date()}")] for d in days[0] if d[1]]
    next_week_kb = [[InlineKeyboardButton(text=d[0], callback_data=f"get_hm_{d[0]}_date_{d[1].date()}")] for d in days[1] if d[1]]
    cur_week_days_kb = InlineKeyboardMarkup(inline_keyboard=
        cur_week_kb
    )

    next_week_days_kb = InlineKeyboardMarkup(inline_keyboard=
        next_week_kb
    )
    return (cur_week_days_kb, next_week_days_kb)


# user menu
user_menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Settings",callback_data="get_user_settings")],
    
])

user_settings_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Send home work dayly",callback_data="send_hw_d_setting_user")],
    [InlineKeyboardButton(text="Back", callback_data="back_to_user_menu")]
])

user_send_hw_d_off_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Turn off",callback_data="off_user_send_hw_d")],
    [InlineKeyboardButton(text="Back", callback_data="back_to_user_settings")]
])


user_send_hw_d_on_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Turn on",callback_data="on_user_send_hw_d")],
    [InlineKeyboardButton(text="Back", callback_data="back_to_user_settings")]
])


# admin menu
async def get_admin_menu_kb():
    send_hw_for_all_users = await db.get_send_hw_dayly_for_all_users()

    kb = [
        [InlineKeyboardButton(text="Settings",callback_data="get_admin_settings")],
        [InlineKeyboardButton(text="Users",callback_data="get_users")],
        [InlineKeyboardButton(text="Home Work",callback_data="get_written_home_work")],
    ]

    if send_hw_for_all_users:
        kb.append(
            [InlineKeyboardButton(text="Turn off sending hw for all users",callback_data="turn_off_send_hw_for_all_users")]
        )
    else:
        kb.append(
            [InlineKeyboardButton(text="Turn on sending hw for all users",callback_data="turn_on_send_hw_for_all_users")]
        )

    return InlineKeyboardMarkup(inline_keyboard=kb)
admin_settings_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Send home work dayly",callback_data="send_hw_d_setting_admin")],
    [InlineKeyboardButton(text="Back", callback_data="back_to_admin_menu")]
])


async def get_admin_written_home_work_kb():
    days = await db.get_all_days()
    msgs = []
    for i, day in enumerate(days):
        kb = [
            [InlineKeyboardButton(text="DELETE", callback_data=f"delete_day_d_id_{day.id}")],
            [InlineKeyboardButton(text="Clear Home Work", callback_data=f"clear_hw_d_id_{day.id}")],
        ]
        if i+1 == len(days):
            kb.append(
                [InlineKeyboardButton(text="Back", callback_data="back_to_admin_menu")]
            )
        msg = [
            f"id: {day.id}, date: {day.date}, day: {day.name}, hw: {day.home_work}, created: {day.created}, updated: {day.updated}",
            InlineKeyboardMarkup(inline_keyboard=kb)
        ]

        msgs.append(msg)
    return msgs


async def get_admin_users_kb():
    users = await db.get_all_users()
    msgs = []
    for i, user in enumerate(users):
        kb = [
            # [InlineKeyboardButton(text="BAN", callback_data=f"delete_day_d_id_{day.id}")],
            # [InlineKeyboardButton(text="Clear Home Work", callback_data=f"clear_hw_d_id_{day.id}")],
        ]
        if user.status == "banned":
            kb.append([InlineKeyboardButton(text="UNBAN", callback_data=f"unban_user_u_id_{user.id}")],)
        else:
            kb.append([InlineKeyboardButton(text="BAN", callback_data=f"ban_user_u_id_{user.id}")],)
            
        if i+1 == len(users):
            kb.append(
                [InlineKeyboardButton(text="Back", callback_data="back_to_admin_menu")]
            )
        msg = [
            f"id: {user.id}, name: {user.name}, status: {user.status} registered: {user.created}, updated: {user.updated}",
            InlineKeyboardMarkup(inline_keyboard=kb)
        ]

        msgs.append(msg)
    return msgs



admin_send_hw_d_off_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Turn off",callback_data="off_admin_send_hw_d")],
    [InlineKeyboardButton(text="Back", callback_data="back_to_admin_settings")]
])


admin_send_hw_d_on_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Turn on",callback_data="on_admin_send_hw_d")],
    [InlineKeyboardButton(text="Back", callback_data="back_to_admin_settings")]
])
