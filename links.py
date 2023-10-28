import asyncio
import aiohttp
from bs4 import BeautifulSoup as bs
# from requests import get as req_get
link1 = 'http://www.osu.ru/pages/schedule/?who=2&what=1&filial=1&prep='
link2 = '&mode=full'
d = {}


async def scrape(url, number):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            body = await resp.text()
            s = bs(body, features='html.parser')
            if s.find_all('h2')[3].text == '':
                pass
            else:
                d.update({number: s.find_all('h2')[3].text})


async def main():
    tasks = []
    for i in range(47800, 48000):
        link = f'{link1}{i}{link2}'
        task = asyncio.create_task(scrape(link, number=i))
        tasks.append(task)
    await asyncio.gather(*tasks)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

print(d)