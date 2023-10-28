import asyncpg
import asyncio


# async def main():
#     # Establish a connection to an existing database named "test"
#     # as a "postgres" user.
#     conn = await asyncpg.connect(host='127.0.0.1', user='postgres', database='schedule', port=1488, password='0000')
#     # Execute a statement to create a new table.
#     await conn.execute('''
#         CREATE TABLE groups(
#             sharaga text PRIMARY KEY,
#             group
#         )
#     ''')
#     await conn.execute('INSERT INTO sharagi(sharaga) VALUES($1)','oren_osu')
#     await conn.close()

async def main():
    conn = await asyncpg.connect(host='127.0.0.1', user='postgres', database='schedule', port=1488, password='0000')
    # Execute a statement to create a new table.
    # t = await conn.execute(f'SELECT 1 FROM users WHERE id = $1','2522:7886')
    # print(type(t))
    data = await conn.fetchrow(f'SELECT * FROM download WHERE shargroup1 = $1','ОГУ:21пм(б)пмм')
    print(data.get('d1'))
    # #     pass
    # # else:
    # await conn.execute(f'INSERT INTO users (id, state) VALUES($1, $2) ', '2522:7886', 'start')
    await conn.close()


asyncio.get_event_loop().run_until_complete(main())
