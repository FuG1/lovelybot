from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup

btnhelp = KeyboardButton('/help')
greet_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnhelp)
btnschedule = KeyboardButton('/schedule')
schedule_kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(btnschedule)


def main_keyboard():
    buttons = [
        [
            InlineKeyboardButton(text="я тебя люблю❤️", callback_data="love"),
            InlineKeyboardButton(text="это мииии❤️", callback_data="mii")
        ],
        [
            InlineKeyboardButton(text="Написать сообщение егрику❤️", callback_data="answerr")
        ]
    ]
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard