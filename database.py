from engine import session_maker
from sqlalchemy import delete, select, update, insert
from models import User, Day
from models import BotData as BotDataModel
from bot_data import BotData
import json
from sqlalchemy.exc import NoResultFound

bot_data = BotData()


class DataBase:
    def __init__(self) -> None:
        pass

    async def add_user_if_not_ex(self, user_id, name):
        
        async with session_maker() as db_session:
            query = select(User)
            data = await db_session.execute(query)
            all_ids = [u.id for u in data.scalars().all()]

            if user_id not in all_ids:
                status = "user"
                if user_id in bot_data.admins:
                    status = "admin"

                db_session.add(User(
                    id=user_id, name=name,
                    status=status
                ))
                await db_session.commit()

    async def add_day_if_not_ex(self, date, day_name):
        async with session_maker() as db_session:
            query = select(Day)
            data = await db_session.execute(query)
            all_dates = [u.date for u in data.scalars().all()]

            if date not in all_dates:
                db_session.add(Day(
                    date=date, 
                    name=day_name
                ))
                await db_session.commit()
    
    async def add_home_work(self, date, subject, task) -> bool:
        async with session_maker() as db_session:
            # get homework
            query = select(Day).where(Day.date==date)
            home_work = await db_session.execute(query)
            home_work: list = json.loads(str(home_work.scalars().one().home_work))
            home_work_rewritten = False

            # update homework
            for i, hm in enumerate(home_work):
                if hm['subject'] == subject:
                    home_work[i]["task"] = task
                    home_work_rewritten = True
                    break
            else:
                home_work.append(
                    {
                        "subject": subject,
                        "task": task
                    }
                )
                
            query = update(Day).where(Day.date==date).values(home_work=json.dumps(home_work, ensure_ascii=False))
            await db_session.execute(query)
            await db_session.commit()

            return home_work_rewritten

    async def get_home_work(self, date):
        async with session_maker() as db_session:
            try:
                query = select(Day).where(Day.date==date)
                data = await db_session.execute(query)
                home_work = json.loads(data.scalars().one().home_work)
                return home_work
            except NoResultFound:
                return False
            
    async def get_all_days(self):
        async with session_maker() as db_session:
            query = select(Day)
            data = await db_session.execute(query)
            home_work = data.scalars().all()
            return home_work
            
    async def get_all_users(self):
        async with session_maker() as db_session:
            query = select(User)
            data = await db_session.execute(query)
            return data.scalars().all()
    
    async def get_admins(self):
        async with session_maker() as db_session:
            query = select(User).where(User.status == "admin")
            data = await db_session.execute(query)
            data = [u.id for u in data.scalars().all()]
            return data
        
    async def get_user_data(self, user_id):
        async with session_maker() as db_session:
            query = select(User).where(User.id == user_id)
            data = await db_session.execute(query)
            data = data.scalars().one()
            return data
        
    async def update_user_data(self, user_id, update_data, new_data):
        async with session_maker() as db_session:
            query = update(User).where(User.id == user_id).values({update_data: new_data})
            await db_session.execute(query)
            await db_session.commit()
            

    async def delete_day(self, day_id):
        async with session_maker() as db_session:
            query = delete(Day).where(Day.id == day_id)
            await db_session.execute(query)
            await db_session.commit()

    async def clear_home_work(self, day_id):
        async with session_maker() as db_session:
            query = update(Day).where(Day.id == day_id).values({"home_work": "[]"})
            await db_session.execute(query)
            await db_session.commit()

    async def get_banned_users(self):
        async with session_maker() as db_session:
            query = select(User).where(User.status == "banned")
            data = await db_session.execute(query)
            data = [u.id for u in data.scalars().all()]
            return data
        
    async def get_send_hw_dayly_for_all_users(self):
        async with session_maker() as db_session:
            query = select(BotDataModel)
            data = await db_session.execute(query)
            data = data.scalars().one()
            return data.send_home_work_daily_for_all_users
        
    async def update_bot_data(self, update_data, new_data):
        async with session_maker() as db_session:
            query = update(BotDataModel).where(BotDataModel.id == 1).values({update_data: new_data})
            await db_session.execute(query)
            await db_session.commit()