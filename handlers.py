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
from bot_data import bot_data
from datetime import datetime
# from database.database import DataBase
from database import DataBase



db = DataBase()


class NewHomeW(StatesGroup):
    task = State()
    subject = State()
    day = State()
    date = State()

    days_of_week = {
        'mon', "tue", 'wed', 
        "thu", "fri", 'sat',
               "sun"    
    }

class SelectDay(StatesGroup):
    messages = State()



router = Router()


#* commands
# start new hm
@router.message(Command(commands=['new']))
async def new_home_work(message: Message, state: FSMContext):
    now = datetime.now()
    await message.answer("select day", reply_markup=kbs.gen_days_kb()[0])
    await message.answer("next week", reply_markup=kbs.gen_days_kb()[1])

    await state.set_state(NewHomeW)
    
    await db.add_user_if_not_ex(
        message.from_user.id, message.from_user.full_name
    )
    

@router.message(Command(commands=['dz']))
async def get_home_work(message: Message):

    kb = kbs.get_home_work_kb()

    await message.answer("Choose day", reply_markup=kb[0])
    await message.answer("Next week", reply_markup=kb[1])
        
@router.message(Command(commands=["c"]))
async def cansel_new_nm(message: Message, state: FSMContext):
    await message.delete()
    await state.clear()







#* states
# get task
@router.message(NewHomeW.task)
async def get_task(message: Message, state: FSMContext):
    task = message.text

    await state.update_data(task=task)

    data = await state.get_data()
    date = data.get("date")
    day = data.get("day")
    subject = data.get("subject")
    task = data.get("task")

    await db.add_day_if_not_ex(date, day)
    hm_rewritten = await db.add_home_work(date, subject, task)

    if hm_rewritten:
        await message.answer("Homework REwritten!")
    else:
        await message.answer("Homework written!")



    await state.clear()


#* sclear text

@router.message()
async def clear_text(message: Message):
    await message.delete()