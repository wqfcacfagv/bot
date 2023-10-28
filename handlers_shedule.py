from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from datetime import datetime, timedelta
from my_functions import schedparse, from_db
from requests import get as req_get
from other_things import Keyboards, States, antispam

router_shedule = Router()
router_shedule.message.filter(States.schedule)
osu_url = 'http://www.osu.ru/'  # ДОРАБОТАТЬ!!! ДОЛЖНА БЫТЬ УНИВЕРСАЛЬНАЯ ССЫЛКА


@router_shedule.message(F.text == 'Выйти')
@antispam
async def to_afterstart(msg: Message, state: FSMContext):
    await state.set_state(state=States.after_start)
    await msg.reply('Мы в главном меню', reply_markup=Keyboards.afterstartkb)
    return


@router_shedule.message(F.text == 'На неделю')
@antispam
async def schedule_week(msg: Message, state: FSMContext):
    if req_get(osu_url).status_code == 200:
        dt = datetime.now()
        ddt = []
        _link = await state.get_data()
        _link2 = None
        _days = None
        if _link.get('days') is not None:
            _link2 = _link.get('s_link2')
            _days = _link.get('days')
            ddt2 = []
            _link = _link.get('s_link')
            for i in range(7):
                dt = dt + timedelta(days=1)
                if dt.weekday() == 6:
                    dt = dt + timedelta(days=1)
                if str(dt.weekday()) in _days:
                    ddt2.append(dt)
                else:
                    ddt.append(dt)
            ans1 = schedparse(dates=ddt, link=_link)
            ans2 = schedparse(dates=ddt2, link=_link2)
            for ans in sorted([*ans1, *ans2]):
                await msg.reply(ans)
        else:
            _link = _link.get('s_link')
            for i in range(7):
                dt = dt + timedelta(days=1)
                if dt.weekday() == 6:
                    dt = dt + timedelta(days=1)
                ddt.append(dt)
            for ans in schedparse(dates=ddt, link=_link):
                await msg.reply(ans)
    else:
        await msg.reply('Сайт ОГУ недоступен')
        return
        shargroup = await state.get_data()
        shargroup = shargroup.get('s_db')
        for ans in await from_db(key=shargroup, day=7):
            await msg.reply(ans)


@router_shedule.message(F.text)
@antispam
async def schedule(msg: Message, state: FSMContext):
    date = msg.text
    t = ('Сегодня', 'Завтра', 'Послезавтра')
    date_pat = '%d.%m.%Y'
    if date in t:
        if req_get(osu_url).status_code == 200:
            if date == t[0]:
                dt = datetime.now()
            elif date == t[1]:
                dt = datetime.now()
                dt = dt + timedelta(days=1)
            else:
                dt = datetime.now()
                dt = dt + timedelta(days=2)
            _link = await state.get_data()
            _days = _link.get('days')
            if _days is not None:
                if str(dt) in _days:
                    _link = _link.get('s_link2')
                else:
                    _link = _link.get('s_link')

            for ans in schedparse(dates=[dt], link=_link):
                await msg.reply(ans)
        else:
            await msg.reply('Сайт ОГУ недоступен')
            return
            shargroup = await state.get_data()
            shargroup = shargroup.get('s_db')
            ans = await from_db(key=shargroup, day=(t.index(date) + 1))
            await msg.reply(ans)
    elif '-' in date:
        if req_get(osu_url).status_code == 200:
            date1 = date.split('-')[0]
            date2 = date.split('-')[1]
            if len(date1) == 5:
                date1 = f'{date1}.{datetime.now().year}'
            if len(date2) == 5:
                date2 = f'{date2}.{datetime.now().year}'
            try:

                date1 = datetime.strptime(date1, date_pat)
                date2 = datetime.strptime(date2, date_pat)
            except:
                await msg.reply('Что-то не так с датой (1)')
                return
            _link = await state.get_data()
            a_ = [date1, date2]
            a_.sort()
            date1 = a_[0]
            date2 = a_[1]
            _days = _link.get('days')
            if _days is not None:
                _link2 = _link.get('days')
                ddt2 = []
            _link = _link.get('s_link')
            ddt = []
            while True:
                if date1 == date2:
                    break
                if _days and str(date1.weekday()) in _days:
                    ddt2.append(date1)
                else:
                    ddt.append(date1)
                date1 = date1 + timedelta(days=1)

            ans1 = schedparse(dates=ddt, link=_link)
            ans2 = []
            if _days is not None:
                ans2 = schedparse(dates=ddt2, link=_link2)
            for ans in sorted([*ans1, *ans2]):
                await msg.reply(ans)
        else:
            await msg.reply('Сайт ОГУ недоступен')
            return
            await msg.reply('Сервер шараги недоступен, воспользуйся кнопками "Сегодня",...')
    else:
        if req_get(osu_url).status_code == 200:
            if len(date) == 5:
                date = f'{date}.{datetime.now().year}'
            elif len(date) == 8:
                date = f'{date[:-2]}20{date[-2::]}'
            try:
                date = datetime.strptime(date, date_pat)
            except:
                await msg.reply('Что-то не так с датой (2)')
                return
            _link = await state.get_data()
            _link = _link.get('s_link')
            for ans in schedparse(dates=[date], link=_link):
                await msg.reply(ans)
        else:
            await msg.reply('Сайт ОГУ недоступен')
            return
            await msg.reply('Сервер шараги недоступен, воспользуйся встроенными кнопками "Сегодня",...')
    return
