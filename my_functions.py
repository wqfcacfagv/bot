from random import randint as rd
from bs4 import BeautifulSoup as bs
from requests import get as req_get
from my_storage import StorageOther
from other_things import Port
from typing import List

schedule_db = StorageOther(password=Port.password, database='schedule', table='download', port=Port.port,
                           host=Port.host)

d_anek = {-2:'На чужой хентай свои тентакли не распускай!\n\n(А. Н. Павленко, aka Лысый)', -1:'Нынешние студенты - лучшая борьба с утечкой мозгов'}

def anekparse() -> str:
    try:
        sr = req_get('https://www.anekdot.ru/release/anekdot/day/').text
        s = bs(sr, features='html.parser')
        data = s.find_all('div', class_='text')
        x = rd(-2, len(data) - 1)
        if x != -1:
            return f'{data[x].text}\n\nАнек шлак, взят с кое-какого сайта, я над этим работаю'
        else:
            return d_anek.get(x)
    except:
        return 'Это временно не работает'


def schedparse(dates: list, link: str) -> List[str]:
    kolvo_par = '12345678'
    vremya_par = ('0', '08:00-9:30', '09:40-11:10', '11:20-12:50', '13:20-14:50', '15:00-16:30', '16:40-18:10',
                  '18:20-19:50', '20:00-21:30')
    wdayd = {0: 'Понедельник', 1: 'Вторник', 2: 'Среда', 3: 'Четверг', 4: 'Пятница', 5: 'Суббота', 6: 'Воскресенье'}
    sr = req_get(link).text
    s = bs(sr, features='html.parser')
    data = s.find_all('tr')
    parys = []
    for date in dates:

        wday = date.date().weekday()
        date = str(date.date()).replace('-', '.')
        date = f'{date[-2:]}.{date[5:7]}.{date[:4]}'
        if wday == 6:
            parys.append(f'{date}\nЭто воскресенье, гений')
            continue
        pary = ''
        for i in data:
            if i.find(string=date) is not None:
                pary = ''
                for n in kolvo_par:
                    pary = f'{pary}✅{n}   {vremya_par[(int(n))]}\n'
                    if len(i.find_all(pare_id=n)) > 1:
                        for i1 in i.find_all(pare_id=n):
                            try:
                                int(i1.text[0])
                                pary = f'{pary}{i1.text[10:]}\n'
                            except:
                                pary = f'{pary}{i1.text}\n'
                    else:
                        try:
                            try:
                                int(i.find(pare_id=n).text[0])
                                pary = f'{pary}{i.find(pare_id=n).text[10:]}\n'
                            except:
                                pary = f'{pary}{i.find(pare_id=n).text}\n'
                        except:
                            pary = f'{pary}Нет пары\n'
                break
        if pary != '':
            pary = f'{date}  {wdayd.get(wday)}\n{pary}'
            parys.append(pary)
        else:
            pary = f'{date}  {wdayd.get(wday)}\nНа эту дату расписания нет'
            parys.append(pary)
    return parys


async def from_db(key: str, day: int) -> List[str]:
    row = await schedule_db.get_row(column_name='shargroup1', key=key)
    if row is not None:
        if day == 1:
            return row.get('d1')
        elif day == 2:
            return row.get('d2')
        elif day == 3:
            return row.get('d3')
        elif day == 7:
            return [row.get(f'd{i}') for i in range(1, 8)]
    else:
        return ['Расписание  временно недоступно']
