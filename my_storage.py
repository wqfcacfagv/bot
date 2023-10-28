from aiogram.fsm.storage.base import BaseStorage, StorageKey
from typing import Optional, Dict, Any, Union
from aiogram.fsm.state import State
from asyncpg import connect

StateType = Optional[Union[str, State]]


class StorageFSM(BaseStorage):
    def __init__(self, user: str = 'postgres', database: str = 'users', port: str = '1488', password: str = '0000',
                 table: str = 'users', host: str = '127.0.0.1'):
        self.conn = None
        self.user = user
        self.db = database
        self.port = port
        self.password = password
        self.table = table
        self.host = host

    async def xui(self) -> None:
        self.conn = await connect(host=self.host, user=self.user, database=self.db,
                                  port=self.port, password=self.password)
        print(self.conn)
        return

    async def set_state(self, key: StorageKey, state: StateType = None) -> None:
        state = state.state if isinstance(state, State) else state
        _id = f'{key.user_id}:{key.chat_id}'

        if await self.conn.execute(f'SELECT * FROM {self.table} WHERE id = $1', _id) == 'SELECT 0':
            await self.conn.execute(f'INSERT INTO {self.table} (id, state) VALUES($1, $2)', _id, state)
        else:
            await self.conn.execute(f'UPDATE {self.table} SET state = $2 WHERE id = $1', _id, state)

        return

    async def get_state(self, key: StorageKey) -> Optional[str]:
        _id = f'{key.user_id}:{key.chat_id}'
        _state = await self.conn.fetchrow(f'SELECT * FROM {self.table} WHERE id = $1', _id)
        if _state is None:
            return _state
        else:
            return _state['state']

    async def get_states(self, column_name: str):
        column = await self.conn.fetch(f'SELECT DISTINCT {column_name} FROM {self.table}')
        _a = [i[f'{column_name}'][:i[f'{column_name}'].find(':')] for i in column]
        return _a

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        _id = f'{key.user_id}:{key.chat_id}'
        await self.conn.execute(f'UPDATE {self.table} SET {list(data.keys())[0]} = $2 WHERE id = $1',
                                _id, list(data.values())[0])
        return

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        _id = f'{key.user_id}:{key.chat_id}'
        data = await self.conn.fetchrow(f'SELECT * FROM {self.table} WHERE id = $1', _id)
        if data is not None:
            d = {}
            for i in data.items():
                d.update({i[0]: i[1]})
            return d
        else:
            return {'xui': 'xui'}

    async def update_data(self, key: StorageKey, data: Dict[str, Any]) -> Dict[str, Any]:
        pass

    async def close(self) -> None:
        if self.conn is not None:
            await self.conn.close()


class StorageOther:
    def __init__(self, user: str = 'postgres', database: str = 'users', port: str = '1488', password: str = '0000',
                 table: str = 'users', host: str = '127.0.0.1'):
        self.conn = None
        self.user = user
        self.db = database
        self.port = port
        self.password = password
        self.table = table
        self.host = host

    async def xui(self) -> None:
        self.conn = await connect(host=self.host, user=self.user, database=self.db,
                                  port=self.port, password=self.password)
        print(self.conn)
        return

    async def update_row(self, key: str, days: list) -> None:
        await self.conn.execute(f'UPDATE {self.table} SET (d1,d2,d3,d4,d5,d6,d7) = ($2, $3, $4, $5, $6, $7, $8)'
                                f' WHERE shargroup1 = $1', key, *days)

        return

    async def get_row(self, key: str, column_name: str):
        row = await self.conn.fetchrow(f'SELECT * FROM {self.table} WHERE {column_name} = $1', key)
        return row

    async def get_rows(self):
        rows = await self.conn.fetch(f'SELECT * FROM {self.table}')
        return rows

    async def get_column(self, column_name: str):
        column = await self.conn.fetch(f'SELECT DISTINCT {column_name} FROM {self.table}')
        _a = [i[f'{column_name}'] for i in column]
        return _a

    async def close(self) -> None:
        if self.conn is not None:
            await self.conn.close()
