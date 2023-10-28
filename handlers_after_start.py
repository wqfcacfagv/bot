from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from my_functions import anekparse
from other_things import antispam, Keyboards, States, schedule_dop_days


router_after_start = Router()
router_after_start.message.filter(States.after_start)


@router_after_start.message(F.text == 'Расписание')
@antispam
async def to_shedule(msg: Message, state: FSMContext):
    _d = await state.get_data()
    if _d.get('s_link') is not None and _d.get('s_db') is not None:

        await msg.reply('DD - день, MM - месяц, YY - год\n\n'
                        'Напиши дату в формате DD.MM, чтобы получить расписание этот день\n\n'
                        'Напиши дату в формате DD.MM-DD.MM, чтобы получить расписание на дни в этом интервале\n\n'
                        'По умолчанию выбирается текущий год, если тебя это не устраивает,'
                        'пиши дату в формате DD.MM.YY\n\n',
                        reply_markup=Keyboards.schedulekb)
        await state.set_state(state=States.schedule)
        if _d.get('days') is not None:
            schedule_dop_days.update({f'{msg.from_user.id}:{msg.chat.id}': _d.get('days')})

        return
    else:
        await state.set_state(state=States.settings)
        await msg.reply('Выбери свои шарагу и группу для расписания', reply_markup=Keyboards.settingskb)


@router_after_start.message(F.text == 'Настройки')
@antispam
async def to_settings(msg: Message, state: FSMContext):
    await state.set_state(state=States.settings)
    await msg.reply('Мы в настройках', reply_markup=Keyboards.settingskb)

    return


# @router_after_start.message(F.text == 'Чат')
# async def to_chat(msg: Message, state: FSMContext):
#     await state.set_state(States.anonchat)
#     await msg.reply('Функция пока недоступна', reply_markup=Keyboards.anonchatkb1)
#     return

@router_after_start.message(F.text == 'Замутить')
@antispam
async def to_aneki(msg: Message, state: FSMContext):
    await state.set_state(state=States.mute)
    await msg.reply(text='Теперь бот не будет реагировать на сообщения. Для включения напиши /restart')
    return


@router_after_start.message(F.text == 'Анекдоты')
@antispam
async def to_aneki(msg: Message, state: FSMContext):
    await state.set_state(state=States.aneki)
    await msg.reply(anekparse(), reply_markup=Keyboards.anekikb)
    return


router_aneki = Router()


@router_aneki.message(States.aneki)
@antispam
async def aneki(msg: Message, state: FSMContext):
    if msg.text == 'Следующий':
        await msg.reply(anekparse())
    elif msg.text == 'Выйти':
        await state.set_state(state=States.after_start)
        await msg.reply('Мы в главном меню', reply_markup=Keyboards.afterstartkb)
    return
