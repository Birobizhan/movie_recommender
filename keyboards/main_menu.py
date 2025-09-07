from aiogram.types import (
    KeyboardButton
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_first_keyboard():
    listik = ['Драма', 'Комедия', 'Боевик (Экшен)', 'Фантастика', 'Триллер', 'Фэнтези', 'Мелодрама', 'Ужасы', 'Детектив',
              'Приключения', 'Исторический', 'Криминал', 'Военный', 'Семейный', 'Биографический']

    kb_builder = ReplyKeyboardBuilder()

    buttons = [KeyboardButton(text=x) for x in listik]
    kb_builder.row(*buttons, width=3)
    return kb_builder.as_markup(resize_keyboard=True)


def get_first_answers():
    answers = ['Драма', 'Комедия', 'Боевик (Экшен)', 'Фантастика', 'Триллер', 'Фэнтези', 'Мелодрама', 'Ужасы', 'Детектив',
              'Приключения', 'Исторический', 'Криминал', 'Военный', 'Семейный', 'Биографический']
    return answers


def remove_one_genre(genre: str):
    listik_two = ['Драма', 'Комедия', 'Боевик (Экшен)', 'Фантастика', 'Триллер', 'Фэнтези', 'Мелодрама', 'Ужасы', 'Детектив',
              'Приключения', 'Исторический', 'Криминал', 'Военный', 'Семейный', 'Биографический', 'Другое']

    kb_builders = ReplyKeyboardBuilder()
    listik_two.remove(genre)
    buttons = [KeyboardButton(text=x) for x in listik_two]
    kb_builders.row(*buttons, width=3)
    keyboard_choice_genre_two = kb_builders.as_markup(resize_keyboard=True)
    return keyboard_choice_genre_two


def get_fourth_question():
    arr = ['🕰️ Классика (до 2000 года)', '🎥 Современное кино (2000–2020)', '⭐ Новинки (2020–2025)', '🤷 Неважно, хочу сюрприз!']
    kb_build = ReplyKeyboardBuilder()
    buttons = [KeyboardButton(text=x) for x in arr]
    kb_build.row(*buttons, width=2)
    keyboard_choice_genre_two = kb_build.as_markup(resize_keyboard=True)
    return keyboard_choice_genre_two


def get_start_kb():
    kb_builders = ReplyKeyboardBuilder()
    buttons = [KeyboardButton(text='Подобрать фильм')]
    kb_builders.row(*buttons, width=1)
    start_kb = kb_builders.as_markup(resize_keyboard=True)
    return start_kb
