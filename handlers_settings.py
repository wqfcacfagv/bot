from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from my_storage import StorageOther
from other_things import Port, Keyboards, States, antispam

schedule = StorageOther(password=Port.password, database='schedule', table='sharagi', port=Port.port, host=Port.host)

router_settings = Router()
temp_s = {}


@router_settings.message(States.settings, F.text == 'Выйти')
@antispam
async def to_after_start(msg: Message, state: FSMContext):
    await msg.reply('Возвращаемся в главное меню', reply_markup=Keyboards.afterstartkb)
    await state.set_state(States.after_start)
    return


@router_settings.message(States.settings, F.text in ('Выбрать группу для расписания',
                                                     'Выбрать доп. группу для расписания')
                         )
@antispam
async def choiceunik(msg: Message, state: FSMContext):
    uniks = await schedule.get_column(column_name='sharaga')
    answer = 'Список доступных шараг:\n'
    for i in uniks:
        answer = f'{answer}{i}, '
    await msg.reply(f'{answer}\n\nВыбери свою шарагу из списка и отправь её название боту',
                    reply_markup=Keyboards.settingskbEx)

    if msg.text == 'Выбрать группу для расписания':
        await state.set_state(States.settings_sharaga)
    else:
        await state.set_state(States.settings_sharaga2)
    return


@router_settings.message(States.settings, F.text == 'Выбрать дни доп. группы')
@antispam
async def choice_days(msg: Message, state: FSMContext):
    await msg.reply('При установленной доп. группе, можно выбрать дни недели, в которые доп. группа'
                    'будет замещать расписание основной группы.\n'
                    'Пример: у вас в среду выходной в основной группе, но есть занятия в ИНПО группе')
    _link = await state.get_data()
    if _link.get('s_link2') is not None:
        await state.set_state(States.settings_days)
        await msg.reply('Введите нужные дни в виде "1,2,3.." где 1 - понедельник; 2 - вторник и т.д.')
    else:
        await msg.reply('Выберите доп. группу для начала')


@router_settings.message(States.settings_days, F.text)
@antispam
async def input_days(msg: Message, state: FSMContext):
    text_ = msg.text.replace(' ', '')
    text_list = text_.split(',')
    try:
        text_list = text_list[0:6]
        for i in text_list:
            if i in ('1', '2', '3', '4', '5', '6'):
                pass
            else:
                raise ZeroDivisionError

    except:
        await msg.reply('Неправильный ввод')
    await state.set_data(data={'days': str.join(text_list)})


@router_settings.message(States.settings_sharaga or States.settings_sharaga2, F.text)
@antispam
async def choicegroup(msg: Message, state: FSMContext):
    if msg.text != 'Выйти':
        if msg.text == 'ОГУ':
            if state == States.settings_sharaga:
                row = await schedule.get_row(column_name='sharaga', key=msg.text)
            else:
                row = await schedule.get_row(column_name='sharaga2', key=msg.text)
            if row is not None:
                temp_s.update({f'{msg.from_user.id}:{msg.chat.id}': msg.text})
                answer = 'Пример названия групп:\n'
                # groups = row['groups']
                answer = f'{answer}З-21ПсН(а)ОПс, 21ПМ(б)ПММ, 21АД(пп)(ИНПО)'

                await msg.reply(f'{answer}\n\nОтправь название своей группы (такое как есть) боту',
                                reply_markup=Keyboards.settingskbEx)
                if state == States.settings_sharaga:
                    await state.set_state(States.settings_group)
                else:
                    await state.set_state(States.settings_group2)
            else:
                await msg.reply('Такой шараги нет!')
            return
        else:
            await msg.reply('Пока доступен только ОГУ')
    else:
        await state.set_state(States.settings)
        await msg.se
        await msg.reply('Настройка не закончена', reply_markup=Keyboards.settingskb)
        try:
            temp_s.pop(f'{msg.from_user.id}:{msg.chat.id}')
        except:
            pass


@router_settings.message(States.settings_group or States.settings_group2, F.text)
@antispam
async def savechoice(msg: Message, state: FSMContext):
    if msg.text != 'Выйти':
        if state == States.settings_group:
            row = await schedule.get_row(column_name='sharaga',
                                         key=temp_s.get(f'{msg.from_user.id}:{msg.chat.id}'))
        else:
            row = await schedule.get_row(column_name='sharaga2',
                                         key=temp_s.get(f'{msg.from_user.id}:{msg.chat.id}'))
        if row is not None:
            groups = row['groups']
            if msg.text in groups:
                _id = row.get('groups').index(msg.text)
                _link = f"{row.get('link1')}{row.get('g_number')[_id]}{row.get('link2')}"
                if state == States.settings_group:
                    await state.set_data(data={'s_link': _link})
                    await state.set_data({'s_db': f"{temp_s.get(f'{msg.from_user.id}:{msg.chat.id}')}:{msg.text}"})
                    await msg.reply('Данные сохранены', reply_markup=Keyboards.afterstartkb)
                    await state.set_state(state=States.after_start)
                else:
                    await state.set_data(data={'s_link2': _link})
                    await state.set_data({'s_db2': f"{temp_s.get(f'{msg.from_user.id}:{msg.chat.id}')}:{msg.text}"})
                    await msg.reply('Данные сохранены')
                temp_s.pop(f'{msg.from_user.id}:{msg.chat.id}')
            else:
                await msg.reply('Такой группы нет!')
        else:
            await msg.reply('Что-то пошло не так')
    else:
        await state.set_state(States.settings)
        await msg.reply('Настройка не закончена', reply_markup=Keyboards.settingskb)
        try:
            temp_s.pop(f'{msg.from_user.id}:{msg.chat.id}')
        except:
            pass
