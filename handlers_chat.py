from aiogram import Router, F
from states import States
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards import Keyboards
from asyncio import sleep as asleep
from random import randint as rd
from aiogram.types import ReplyKeyboardRemove as RKR
from aiogram.filters import Command
from aiogram import Bot
from time import time

router_chat = Router()
router_chat.message.filter(States.anonchat)

id_key = {}
chat_check = {}
chat_in = {}
warn = []
ids = []
canc = []
chat_deck = []


@router_chat.message(F.text == 'Выйти')
async def to_afterstart(msg: Message, state: FSMContext):
    await msg.reply('Мы в начале', reply_markup=Keyboards.afterstartkb)
    await state.set_state(States.after_start)
    return


@router_chat.message(F.text == 'Найти собеседника')
async def chat_t(msg: Message, state: FSMContext):
    _user_id = msg.from_user.id
    if _user_id in ids:
        await msg.reply('Чат временно не работает, мы уже решаем эту проблему',
                        reply_markup=Keyboards.afterstartkb)
        return
    if msg.chat.type != 'private':
        await msg.reply('Он работает только в лс', reply_markup=Keyboards.afterstartkb)
        return
    await state.set_state(States.anonchat_poisk)
    await msg.reply('Идёт поиск собеседника...', reply_markup=Keyboards.anonchatkb2)

    async def chat_tv(msg_: Message):
        _user_id_ = msg_.from_user.id

        chat_check.update({_user_id: 1})
        ids.append(_user_id)

        while True:
            if len(ids) < 2:
                if len(ids) == 0:
                    return
                await asleep(1)

            else:
                break
        x = rd(0, len(ids) - 1)
        if ids[x] == _user_id_:
            try:
                chat_in.update({_user_id_: ids[x - 1]})
            except IndexError:
                chat_in.update({_user_id_: ids[x + 1]})
        else:
            chat_in.update({_user_id_: ids[x]})

        while True:
            if _user_id_ == chat_in.get(chat_in.get(_user_id_)):
                ids.remove(_user_id_)
                await state.set_state(States.anonchat_chat)
                await msg_.reply('Собеседник найден\nЧтобы закончить чат, напиши или нажми /cancel',
                                 reply_markup=RKR())
                break
            else:
                if not chat_in:
                    return
                await asleep(0.5)
        if len(ids) < 2 and len(chat_deck) > 0:
            ids.append(chat_deck[0])
            chat_deck.pop(0)

    if len(ids) > 1:
        chat_deck.append(_user_id)
    else:
        await chat_tv(msg)
    return


router_chat2 = Router()
router_chat2.message.filter(States.anonchat_poisk)


@router_chat2.message(F.text == 'Отмена')
async def to_chat(msg: Message, state: FSMContext):
    _user_id = msg.from_user.id
    chat_deck.remove(_user_id)
    await msg.reply('Поиск отменён', reply_markup=Keyboards.anonchatkb1)
    await state.set_state(States.anonchat)


router_chat3 = Router()
router_chat3.message.filter(States.anonchat_chat)


@router_chat3.message(Command(commands=['cancel']))
async def to_cancel(bot: Bot,msg: Message, state: FSMContext):
    mid = msg.from_user.id
    t_mid = chat_in.get(mid)
    await state.set_state(States.anonchat)
    chat_in.pop(mid)
    chat_check.pop(mid)
    if mid in canc:
        canc.remove(mid)
    else:
        await bot.send_message(t_mid, 'Собеседник ливнул')
        canc.append(t_mid)
    await bot.send_message(mid, 'Перестали общаться', reply_markup=Keyboards.anonchatkb1)
    return


@router_chat3.message(F.text)
async def chatt(msg: Message, state: FSMContext, bot: Bot):
    mid = msg.from_user.id
    if id_key.get(mid) is not None:
        if time() - id_key.get(mid) < 3:
            warn.append(mid)
        elif id_key.get(mid) is not None and time() - id_key.get(mid) > 3:
            try:
                warn.remove(mid)
            except ValueError:
                pass
    if id_key.get(mid) is None:
        id_key.update({mid: 0})
    else:
        id_key.update({mid: time()})
    if mid not in warn:
        if chat_check.get(mid) == 1:
            t_mid = chat_in.get(mid)
            if chat_in.get(t_mid) is not None:
                await bot.send_message(t_mid, msg.text)
            else:
                await bot.send_message(mid, 'Собеседник ливнул')
                await state.set_state(States.anonchat)
                chat_check.pop(mid)
                chat_in.pop(mid)
    return
