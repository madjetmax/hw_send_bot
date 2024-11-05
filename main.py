import logging
from aiogram import Bot, Dispatcher

import asyncio
from config import *
# from handlers import handlers, callbacks
import handlers, callbacks
from middlewares import MaiMiddleware
# from database.engine import create_db
from engine import create_db, drop_db
import database
# from database import database
import scheduler
import user, admin
from bot_data import bot_data


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


db = database.DataBase()


dp.message.middleware.register(MaiMiddleware())


dp.include_routers(
    admin.router,
    user.router,
    handlers.router,
    callbacks.router
)


async def main():
    scheduler.start_all_jobs(bot)
    # logging.basicConfig(level=logging.INFO)
    scheduler.scheduler.start()
    await create_db()
    
    bot_data.admins = await db.get_admins()
    bot_data.banned_users = await db.get_banned_users()
    bot_data.send_home_work_daily_for_all_users = await db.get_send_hw_dayly_for_all_users()

    print('bot launched')
    await dp.start_polling(bot, skip_updates=True)
    
if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("bot stoped!")