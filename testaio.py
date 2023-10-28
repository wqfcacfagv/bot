from bs4 import BeautifulSoup as bs
from requests import get as req_get
from datetime import datetime, timedelta


def schedparse(dates: list, link: str):
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

link = 'http://www.osu.ru/pages/schedule/?who=1&what=1&filial=1&group=13903&mode=full'
date = datetime.now() + timedelta(days=1)
dates = [date, date+timedelta(days=1), date+timedelta(days=2), date, date+timedelta(days=1), date+timedelta(days=2)]

a = schedparse(dates=dates, link=link)

print(a[0])
print('/////////////////')
print(a[2])