from apscheduler.schedulers.asyncio import AsyncIOScheduler
from database import DataBase
from aiogram import Bot
from config import *
import date_generator
from bot_data import bot_data

scheduler = AsyncIOScheduler()
db = DataBase()

async def send_home_work(bot: Bot):
    next_day = date_generator.get_next_day()
    home_work = await db.get_home_work(next_day[0])
    all_users = await db.get_all_users()

    if bot_data.send_home_work_daily_for_all_users:
        for user in all_users:
            try:
                if bool(user.send_home_work_daily) and home_work:
                    await bot.send_message(user.id, f"Home work on {next_day[1]} {next_day[0]}")
                    for hm in home_work:
                        await bot.send_message(user.id, f"{hm.get('subject')}: {hm.get('task')}")
            except Exception:
                pass

def start_all_jobs(bot: Bot):
    scheduler.add_job(
        send_home_work, 'cron', 
        day_of_week=", ".join(HW_SEND_DAYS), 
        hour=HW_SEND_HOURS, 
        minute=HW_SEND_MINUTES, 
        second=HW_SEND_SECONDS, 
        args=(bot,), id='main_job'
    )

def reload_main_job():
    ...
