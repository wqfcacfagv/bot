from aiogram.fsm.state import StatesGroup, State
from aiogram.types import KeyboardButton as KB
from aiogram.types import ReplyKeyboardMarkup as RKM
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from time import time

owner_id = 5285316026
token = '6403990035:AAGQ45WulsPGAeET_V-CDmfM16kIK5OCFrY'
# token = '6308381327:AAE4sgDySfwMbnvZfrpOsYe43oqu5kbzEA0'

schedule_dop_days = {}

class Port:  # params for database server
    port = '5432'
    password = 'postgres'
    host = '100.90.128.99'
    # port = '1488'
    # password = '0000'
    # host = 'localhost'


class States(StatesGroup):  # class of FSM states
    start = State()
    after_start = State()
    mute = State()
    schedule = State()
    settings = State()
    settings_sharaga = State()
    settings_sharaga2 = State()
    settings_group = State()
    settings_group2 = State()
    settings_days = State()
    aneki = State()
    anonchat = State()
    anonchat_poisk = State()
    anonchat_chat = State()


class Keyboards:  # class of keyboards for each state
    afterstartkb = RKM(keyboard=[[KB(text='Анекдоты'), KB(text='Расписание')],
                                 [KB(text='Замутить'), KB(text='Настройки')]
                                 ],
                       resize_keyboard=True,
                       input_field_placeholder='Меню',
                       selective=True)
    schedulekb = RKM(keyboard=[[KB(text='Сегодня'), KB(text='Завтра'), KB(text='На неделю')],
                               [KB(text='Послезавтра'), KB(text='Выйти')]
                               ],
                     resize_keyboard=True,
                     input_field_placeholder='Пиши дату...',
                     selective=True)
    anekikb = RKM(keyboard=[[KB(text='Следующий')],
                            [KB(text='Выйти')]],
                  resize_keyboard=True,
                  input_field_placeholder='Можно поржать',
                  selective=True)
    settingskb = RKM(keyboard=[
        [KB(text='Выбрать группу для расписания')],
        [KB(text='Выбрать доп. группу для расписания')],
        [KB(text='Выйти')]],
        resize_keyboard=True,
        input_field_placeholder='Отчисление',
        selective=True)
    settingskbEx = RKM(keyboard=[[KB(text='Выйти')]],
                       resize_keyboard=True,
                       input_field_placeholder='Го в дурака',
                       selective=True)
    # anonchatkb1 = RKM(keyboard=[[KB(text='Найти собеседника')],
    #                             [KB(text='Выйти')]],
    #                   resize_keyboard=True,
    #                   input_field_placeholder='Кто знает, что тебя ждёт...')
    # anonchatkb2 = RKM(keyboard=[[KB(text='Отмена')]],
    #                   resize_keyboard=True,
    #                   input_field_placeholder='Кто знает, что тебя ждёт...')
    # anonchatkb3 = RKM(keyboard=[[KB(text='/cancel')]],
    #                   resize_keyboard=True,
    #                   input_field_placeholder='Общайся')


antispam_dict = {}


def antispam(func):  # simple antispam in memory function
    async def def_spam(msg: Message, state: FSMContext):
        if antispam_dict.get(msg.from_user.id) is None:
            antispam_dict.update({msg.from_user.id: time()})
            await func(msg, state)
        else:
            if time() - antispam_dict.get(msg.from_user.id) < 0.3:
                await msg.reply('Ты отправляешь сообщения слишком часто!')
                return
            else:
                await func(msg, state)
                antispam_dict.pop(msg.from_user.id)

    return def_spam
