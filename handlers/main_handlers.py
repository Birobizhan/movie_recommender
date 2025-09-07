from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import Message, KeyboardButton
from aiogram import Router, types
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from keyboards.third_question_keyboard import keyboard_for_third_question, \
    get_question, get_list_check
from lexicon.lexicon import LEXICON_RU
from keyboards.main_menu import remove_one_genre, get_fourth_question, get_first_keyboard, get_first_answers, get_start_kb
from list_films.movie_alg import recommend_movies

# Инициализируем роутер уровня модуля
router = Router()


# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=get_start_kb())


# # Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])


# Этот хэндлер будет срабатывать на команду "/cancel" в состоянии
# по умолчанию и сообщать, что эта команда работает внутри машины состояний
@router.message(Command(commands='cancel'), StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text='Отменять нечего. Вы не выбираете фильм\n\n'
             'Чтобы перейти к заполнению опросника - '
             'напишите Подобрать фильм', reply_markup=get_start_kb()
    )


# Этот хэндлер будет срабатывать на команду "/cancel" в любых состояниях,
# кроме состояния по умолчанию, и отключать машину состояний
@router.message(Command(commands='cancel'), ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(
        text='Вы больше не выбираете фильм\n\n'
             'Чтобы снова перейти к заполнению опросника - '
             'напишите Подобрать фильм', reply_markup=get_start_kb()
    )
    # Сбрасываем состояние и очищаем данные, полученные внутри состояний
    await state.clear()


class UserChoices(StatesGroup):
    choice_1 = State()
    choice_2 = State()
    choice_3 = State()
    choice_4 = State()


@router.message(F.text.in_(['Подобрать фильм', 'Начать заново']))
async def start_choices(message: types.Message, state: FSMContext):
    await message.answer("Выберите основной жанр:", reply_markup=get_first_keyboard(),
                         resize_keyboard=True,
                         )
    await state.set_state(UserChoices.choice_1)


@router.message(StateFilter(UserChoices.choice_1))
async def handle_choice_1(message: types.Message, state: FSMContext):
    if message.text not in get_first_answers():
        await message.answer("Пожалуйста, выберите один из предложенных вариантов.")
        return
    await state.update_data(choice_1=message.text)
    data = await state.get_data()
    await message.answer("Выберите поджанр:", reply_markup=remove_one_genre(data['choice_1']), resize_keyboard=True)
    await state.set_state(UserChoices.choice_2)


@router.message(StateFilter(UserChoices.choice_2))
async def handle_choice_2(message: types.Message, state: FSMContext):
    data = await state.get_data()
    listik_three = ['Драма', 'Комедия', 'Боевик (Экшен)', 'Фантастика', 'Триллер', 'Фэнтези', 'Мелодрама', 'Ужасы',
                    'Детектив',
                    'Приключения', 'Исторический', 'Криминал', 'Военный', 'Семейный', 'Биографический', 'Другое']
    spisok = listik_three.copy()
    spisok.remove(data['choice_1'])
    print(spisok)
    if message.text not in spisok:
        await message.answer("Пожалуйста, выберите один из предложенных вариантов.")
        return
    await state.update_data(choice_2=message.text)
    await message.answer(f"{get_question(data['choice_1'])}",
                         reply_markup=keyboard_for_third_question(data['choice_1']),
                         resize_keyboard=True)
    await state.set_state(UserChoices.choice_3)


@router.message(StateFilter(UserChoices.choice_3))
async def handle_choice_3(message: types.Message, state: FSMContext):
    data = await state.get_data()

    if message.text not in get_list_check(data['choice_1']):
        await message.answer("Пожалуйста, выберите один из предложенных вариантов.")
        return
    await state.update_data(choice_3=message.text)
    await message.answer("Временной период:", reply_markup=get_fourth_question(), resize_keyboard=True)
    await state.set_state(UserChoices.choice_4)


@router.message(StateFilter(UserChoices.choice_4))
async def handle_choice_4(message: types.Message, state: FSMContext):
    arr = ['🕰️ Классика (до 2000 года)', '🎥 Современное кино (2000–2020)', '⭐ Новинки (2020–2025)',
           '🤷 Неважно, хочу сюрприз!']
    if message.text not in arr:
        await message.answer("Пожалуйста, выберите один из предложенных вариантов.")
        return
    await state.update_data(choice_4=message.text)
    data = await state.get_data()
    recommended = recommend_movies([data['choice_1'], data['choice_2'], data['choice_3'], data['choice_4']])
    movie_list = "\n".join([f"🎬 {movie}" for movie in recommended])
    response_text = (
        f"🎉 Спасибо! Вот фильмы, которые вам подойдут:\n\n"
        f"{movie_list}\n\n"
        "🍿 Наслаждайтесь просмотром!"
    )
    await message.answer(text=response_text, reply_markup=types.ReplyKeyboardRemove())
    await state.clear()
    keyboard = types.ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Начать заново')]], resize_keyboard=True, )
    await message.answer("Хотите начать заново?", reply_markup=keyboard)


@router.message(F.text == 'Начать заново')
async def start_over(message: types.Message):
    await message.answer("Давайте начнем снова!", reply_markup=get_start_kb())
    await start_choices(message)
