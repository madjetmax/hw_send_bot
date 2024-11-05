from aiogram import Bot, Dispatcher, types, F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
import asyncio
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from datetime import datetime
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import keyboards as kbs
from bot_data import BotData
from datetime import datetime

from database import DataBase


router = Router()



@router.message(Command(commands=['me']))
async def get_user_preferences(message: Message):
    await message.answer("User menu:", reply_markup=kbs.user_menu_kb)