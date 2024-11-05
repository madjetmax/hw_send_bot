import logging
from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import asyncio
import sqlite3
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import keyboards as kbs
from handlers import NewHomeW, SelectDay

from bot_data import bot_data
from database import DataBase





db = DataBase()




router = Router()


@router.callback_query()
async def callback(call: CallbackQuery, state: FSMContext):
    # select_day 
    if call.data.startswith("set_d_"):
        week_is_current = True
        if call.data.endswith("_n"):
            week_is_current = False
        day = call.data.replace("set_d_", "").split('_')[0]
        date = call.data.replace("set_d_", "").replace(f'{day}_date_', "").replace("_n", "")
        await state.update_data(day=day, date=date)
        await call.message.edit_text("Chose Subject", reply_markup=kbs.get_subjects_kb(day, week_is_current))
    
    # return to days list
    if call.data == "back_to_next_days":
        chat_id = call.message.chat.id
        msg_id = call.message.message_id
        await call.message.edit_text("next week", reply_markup=kbs.gen_days_kb()[1])

    if call.data == "back_to_cur_days":
        chat_id = call.message.chat.id
        msg_id = call.message.message_id
        await call.message.edit_text("select day", reply_markup=kbs.gen_days_kb()[0])
    # select subject
    if call.data.startswith("select_sub_"):
        week_is_current = True
        if call.data.endswith("_n_d"):
            week_is_current = False
        subj = call.data.replace("select_sub_", "").replace("_n_d", "")
        await call.message.edit_text(f"Enter task for subject: {subj}", reply_markup=kbs.get_back_to_subject_kb(week_is_current))
        await state.update_data(subject=subj)
        await state.set_state(NewHomeW.task)


    # ret to subjs list
    if call.data == "back_to_subjects_n_d":
        data = await state.get_data()
        day = data.get("day")

        if day:
            chat_id = call.message.chat.id
            msg_id = call.message.message_id
            week_is_current = False

            # await call.bot.edit_message_text("Chose Subject", chat_id=chat_id, message_id=msg_id, reply_markup=kbs.get_subjects_kb(day, week_is_current))
            await call.message.edit_text("Chose Subject", reply_markup=kbs.get_subjects_kb(day, week_is_current))
        await call.answer("")

    if call.data == "back_to_subjects_c_d":
        data = await state.get_data()
        day = data.get("day")

        if day:
            chat_id = call.message.chat.id
            msg_id = call.message.message_id
            week_is_current = True

            # await call.bot.edit_message_text("Chose Subject", chat_id=chat_id, message_id=msg_id-1, reply_markup=kbs.get_subjects_kb(day, week_is_current))
            await call.message.edit_text("Chose Subject", reply_markup=kbs.get_subjects_kb(day, week_is_current))   
        await call.answer("")
    
    if call.data.startswith("get_hm_"):
        date = call.data.split("_")[4]
        day = call.data.split("_")[2]


        home_work = await db.get_home_work(date)
        
        if home_work:
            await call.message.answer(f"Home work on {day} {date}")
            for hm in home_work:
                await call.message.answer(f"{hm.get("subject")}: {hm.get("task")}")
        else:
            await call.message.answer(f"No home work on {day} {date}")
    
    # user menu
    if call.data == "get_user_settings":
        await call.message.edit_text("Settings:", reply_markup=kbs.user_settings_kb)
    
    if call.data == "back_to_user_menu":
        await call.message.edit_text("User menu:", reply_markup=kbs.user_menu_kb)

    if call.data == "send_hw_d_setting_user":
        user_data = await db.get_user_data(call.from_user.id)
        if bool(user_data.send_home_work_daily):
            await call.message.edit_text("Manage Sending home work dayly", reply_markup=kbs.user_send_hw_d_off_kb)
        else:
            await call.message.edit_text("Manage Sending home work dayly", reply_markup=kbs.user_send_hw_d_on_kb)
    
    if call.data == "back_to_user_settings":
        await call.message.edit_text("Settings:", reply_markup=kbs.user_settings_kb)

    if call.data == "off_user_send_hw_d":
        await db.update_user_data(call.from_user.id, "send_home_work_daily", False)
        await call.answer("Updated!")
        await call.message.edit_text("Settings:", reply_markup=kbs.user_settings_kb)

    if call.data == "on_user_send_hw_d":
        await db.update_user_data(call.from_user.id, "send_home_work_daily", True)
        await call.answer("Updated!")
        await call.message.edit_text("Settings:", reply_markup=kbs.user_settings_kb)

    # admin menu
    user_id = call.from_user.id
    if call.data == "get_admin_settings":
        admins = bot_data.admins
        if user_id in admins:
            await call.message.edit_text("Settings:", reply_markup=kbs.admin_settings_kb)
    
    if call.data == "back_to_admin_menu":
        admins = bot_data.admins
        if user_id in admins:
            await call.message.edit_text("Admin menu:", reply_markup=await kbs.get_admin_menu_kb())

    if call.data == "get_users":
        admins = bot_data.admins
        if user_id in admins:
            msgs = await kbs.get_admin_users_kb()
            for msg in msgs:
                await call.message.answer(msg[0], reply_markup=msg[1])


    if call.data == "send_hw_d_setting_admin":
        admins = bot_data.admins
        if user_id in admins:
            user_data = await db.get_user_data(call.from_user.id)
            if bool(user_data.send_home_work_daily):
                await call.message.edit_text("Manage Sending home work dayly", reply_markup=kbs.admin_send_hw_d_off_kb)
            else:
                await call.message.edit_text("Manage Sending home work dayly", reply_markup=kbs.admin_send_hw_d_on_kb)
    
    if call.data == "back_to_admin_settings":
        admins = bot_data.admins
        if user_id in admins:
            await call.message.edit_text("Settings:", reply_markup=kbs.admin_settings_kb)

    if call.data == "off_admin_send_hw_d":
        admins = bot_data.admins
        if user_id in admins:
            await db.update_user_data(call.from_user.id, "send_home_work_daily", False)
            await call.answer("Updated!")
            await call.message.edit_text("Settings:", reply_markup=kbs.admin_settings_kb)

    if call.data == "on_admin_send_hw_d":
        admins = bot_data.admins
        if user_id in admins:
            await db.update_user_data(call.from_user.id, "send_home_work_daily", True)
            await call.answer("Updated!")
            await call.message.edit_text("Settings:", reply_markup=kbs.admin_settings_kb)

    if call.data == "get_written_home_work":
        admins = bot_data.admins
        if user_id in admins:
            msgs = await kbs.get_admin_written_home_work_kb()
            for msg in msgs:
                await call.message.answer(msg[0], reply_markup=msg[1])

    if call.data.startswith("delete_day_d_id_"):
        admins = bot_data.admins
        if user_id in admins:
            day_id = int(call.data.replace("delete_day_d_id_", ""))
            await db.delete_day(day_id)
            await call.message.delete()
    
    if call.data.startswith("clear_hw_d_id_"):
        admins = bot_data.admins
        if user_id in admins:
            day_id = int(call.data.replace("clear_hw_d_id_", ""))
            await db.clear_home_work(day_id)
    
    if call.data.startswith("ban_user_u_id_"):
        ban_user_id = int(call.data.replace("ban_user_u_id_", ""))
        admins = bot_data.admins
        if user_id in admins:
            if ban_user_id not in admins:
                await db.update_user_data(ban_user_id, "status", "banned")
                bot_data.banned_users = await db.get_banned_users()
                print(12)
            else:
                await call.answer("Cannot bun this user")

    if call.data.startswith("unban_user_u_id_"):
        unban_user_id = int(call.data.replace("unban_user_u_id_", ""))
        admins = bot_data.admins
        if user_id in admins:
            await db.update_user_data(unban_user_id, "status", "user")
            bot_data.banned_users = await db.get_banned_users()

    if call.data == "turn_off_send_hw_for_all_users":
        admins = bot_data.admins
        if user_id in admins:
            await db.update_bot_data(
                "send_home_work_daily_for_all_users",
                False
            )
            await call.message.edit_text("Admin menu:", reply_markup=await kbs.get_admin_menu_kb())
            bot_data.send_home_work_daily_for_all_users = False

        await call.answer("")

    if call.data == "turn_on_send_hw_for_all_users":
        admins = bot_data.admins
        if user_id in admins:
            await db.update_bot_data(
                "send_home_work_daily_for_all_users",
                True
            )
            await call.message.edit_text("Admin menu:", reply_markup=await kbs.get_admin_menu_kb())

            bot_data.send_home_work_daily_for_all_users = True
        await call.answer("")