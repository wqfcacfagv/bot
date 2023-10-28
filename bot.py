# from asyncio import gather, create_task
from asyncio import run as aiorun
from aiogram import Bot, Dispatcher
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from my_storage import StorageFSM
from handlers_shedule import router_shedule
from handlers_after_start import router_after_start, router_aneki
from handlers_settings import router_settings, schedule
# from handlers_chat import router_chat, router_chat2, router_chat3
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime, timedelta
from my_functions import schedparse, schedule_db
from other_things import Keyboards, antispam, Port, States, token, owner_id

bot = Bot(token=token)

storage_fsm = StorageFSM(port=Port.port, password=Port.password, host=Port.host)  # подключаю свое хранилище фсм
dp = Dispatcher(storage=storage_fsm)

router_start = Router()


@router_start.message(Command(commands=['start']))
@antispam
async def cmd_start(msg: Message, state: FSMContext):
    if await state.get_state():
        await msg.reply(text='Бот уже запущен')
    else:
        await state.set_state(state=States.after_start)
        await msg.reply(text='Гениальный бот для расписания и анекдотов, остальное в разработке\n\n'
                             'Команды в группе ему лучше писать через /command@real_genius_bot\n\n'
                             'А сообщения в группе отправлять как ответ на его сообщение',
                        reply_markup=Keyboards.afterstartkb)
    return


@router_start.message(Command(commands=['restart']))
@antispam
async def cmd_start(msg, state):
    await state.set_state(state=States.after_start)
    await msg.reply(text='Мы в главном меню',
                    reply_markup=Keyboards.afterstartkb)
    return


@dp.message(Command(commands=['van']))
async def sensor(msg: Message):
    if msg.from_user.id == owner_id:
        m_text = msg.text[8::]
        from subprocess import check_output as sub_check
        from os import system as sos
        await msg.reply('Команда принята')
        try:
            s = sub_check(m_text).decode('utf8')
            sl = s.split('\n')
            s = ''
            for i_ in sl:
                s = f'{s}\n{i_}'
            await msg.reply(f'{s}\nSubCheck')
            # print(s)
        except:
            try:
                sos(m_text)
                await msg.reply('SOS')
            except:
                await msg.reply('Ошибка при выполнении команды')
    return


@dp.message(Command(commands=['alarm']))
async def alarm(msg: Message):
    if msg.from_user.id == owner_id:
        user_ids = await storage_fsm.get_states(column_name='id')
        print(user_ids)
        for id_ in user_ids:
            await bot.send_message(chat_id=id_,
                                   text='!Через 10 минут бот будет отключен для проведения технических работ!')
            await bot.send_message(chat_id=id_,
                                   text='!Через 10 минут бот будет отключен для проведения технических работ!')
            await bot.send_message(chat_id=id_,
                                   text='!Через 10 минут бот будет отключен для проведения технических работ!')


@dp.message(Command(commands=['alarmtext']))
async def alarm(msg: Message):
    if msg.from_user.id == owner_id:
        text_ = msg.text.replace('/alarmtext', '')
        user_ids = await storage_fsm.get_states(column_name='id')
        for id_ in user_ids:
            await bot.send_message(chat_id=id_,
                                   text=text_)




# async def sched_upload():
#     dict_sched = {}
#     results = await aio_schedparse()
#     index =0
#     for i in results[1]:
#         if i.get('link2') is not None:
#             for ii in i.get('groups'):
#                 for _ in range(1, 8):
#                     dict_sched.update({f"{i.get('sharaga')}:{ii}":results[0][index]})
#                     index+=1
#     return dict_sched

async def my_aio():
    link = 'http://www.osu.ru/pages/schedule/?who=1&what=1&filial=1&group=13903&mode=full'
    dt_ = datetime.now()
    dates = []
    for _ in range(1, 8):
        dates.append(dt_)
        dt_ = dt_ + timedelta(days=1)
    z = schedparse(dates=dates, link=link)
    await schedule_db.update_row(key='ОГУ:21пм(б)пмм', days=z)


async def main() -> None:
    await storage_fsm.xui()  # подключение к бд
    await schedule.xui()
    await schedule_db.xui()
    with open('runLog.txt', 'w', encoding='utf8') as f:
        f.write('databases connect success')
    # scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
    # scheduler.add_job(my_aio, trigger='interval', minutes=1440)
    # scheduler.start()
    # await my_aio()
    await bot.delete_webhook(drop_pending_updates=True)  # игнор всех предыдущих сообщений
    dp.include_routers(router_start, router_after_start, router_shedule,
                       router_aneki, router_settings)  # подключение роутеров
    await dp.start_polling(bot)


if __name__ == '__main__':
    aiorun(main())
