import asyncio
import logging

import aioschedule
from aiogram import Bot, Dispatcher
from aiogram import types
from aiogram.dispatcher import FSMContext
import db
import os
import keyboards as kb
from keyboards import *
import random
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup


logging.basicConfig(level=logging.INFO)
bot = Bot(token='your_token')
dp = Dispatcher(bot, storage=MemoryStorage())
users = [511800914, 1218486392]

class ANSWER(StatesGroup):
    answer = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.from_user.id not in users:
        await message.answer('Вы не машик, уходите')
    else:
        await message.answer(
            'Привет, машик, я создан чтоб писать тебе каждый день милые сообщения<3. Мой создатель, егрик,'
            ' очень сильно тебя любит, как и ты его<3 Нажми на кнопку help и узнай команды, которыя я знаю!',
            reply_markup=kb.greet_kb)
        db.put_id(message.from_user.id)
    await bot.send_message('511800914', 'нажал кнопку start')


@dp.message_handler(commands=['help'])
async def process_relpy(message: types.Message):
    await message.answer("Вот все команды, которые я знаю: \n schedule - рассписание милых сообщений \n ",
                         reply_markup=kb.schedule_kb)


@dp.message_handler(commands=['schedule'])
async def process_relpy(message: types.Message):
    await message.reply("Вот ваше рассписание: \n    09:00 \n    11:00 \n    13:00 \n    15:00 \n    17:00 \n    19:00")



@dp.callback_query_handler(text="love")
async def cumback(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message('511800914', 'нажала love')
    await call.message.answer("❤️")


@dp.callback_query_handler(text="mii")
async def miiback(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message('511800914', 'нажала mii')
    await call.message.answer("Дяяяяя это миии")


@dp.callback_query_handler(text="answerr")
async def back(call: types.CallbackQuery):
    await call.answer()
    await bot.send_message('511800914', 'нажала answerr')
    await call.message.answer("Введи сообщение, которое хочешь прислать❤️")
    await ANSWER.answer.set()




@dp.message_handler(state=ANSWER.answer)
async def answer(message: types.Message, state: FSMContext):
    await bot.send_message(511800914, message.text)
    await state.finish()
    await message.answer("Спасибо за сообщение, егрику очень приятно❤️")


async def printl():
    with open('phrase.txt', 'r', encoding='utf-8') as file:
        phrases = [i.split('\n')[0] for i in file.readlines()]
        phrazes = phrases[random.randint(0, len(phrases) - 1)]
    files = os.listdir('photos/')
    len_photo = len(files)
    path = 'photos/image{}.png'.format(random.randint(1, len_photo))
    for i in db.get_id():
        with open(path, 'rb') as photo:
            await bot.send_photo(chat_id=int(i[0]), photo=photo)
        await bot.send_message(int(i[0]), phrazes, reply_markup=main_keyboard())


async def scheduler():
    aioschedule.every().day.at("09:00").do(printl)
    aioschedule.every().day.at("11:00").do(printl)
    aioschedule.every().day.at("13:00").do(printl)
    aioschedule.every().day.at("15:00").do(printl)
    aioschedule.every().day.at("17:00").do(printl)
    aioschedule.every().day.at("19:00").do(printl)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(60)


async def on_startup(_):
    asyncio.create_task(scheduler())


field = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]
current_player = 'X'


async def show_board(message):
    board = ''
    for row in field:
        board += ' '.join(row) + '\n'
    if not board.strip():
        board = "Игровое поле пусто."
    await message.answer(board, parse_mode=ParseMode.MARKDOWN)


def check_winner():
    for i in range(3):
        if field[i][0] == field[i][1] == field[i][2] != ' ':
            return True
        if field[0][i] == field[1][i] == field[2][i] != ' ':
            return True


    if field[0][0] == field[1][1] == field[2][2] != ' ':
        return True
    if field[0][2] == field[1][1] == field[2][0] != ' ':
        return True

    return False


def check_draw():
    for row in field:
        if ' ' in row:
            return False
    return True


@dp.message_handler(commands=['tictac'])
async def start_game(message: types.Message):
    global field, current_player
    field = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]
    current_player = 'X'
    await show_board(message)
    await message.answer("Игра началась! Крестики - 'X', нолики - 'O'. Сделайте свой ход.")


@dp.message_handler(lambda message: message.text.lower() in ['1', '2', '3', '4', '5', '6', '7', '8', '9'])
async def make_move(message: types.Message):
    global field, current_player
    move = int(message.text) - 1
    row = move // 3
    col = move % 3

    if field[row][col] == ' ':
        field[row][col] = current_player
        if check_winner():
            await show_board(message)
            await message.answer(f"Игрок {current_player} победил!")
            await message.answer("Чтобы начать новую игру, введите /start.")
        elif check_draw():
            await show_board(message)
            await message.answer("Ничья!")
            await message.answer("Чтобы начать новую игру, введите /start.")
        else:
            current_player = 'O' if current_player == 'X' else 'X'
            await show_board(message)
            await message.answer(f"Ход игрока {current_player}.")
    else:
        await message.answer("Эта клетка уже занята. Выберите другую.")

if __name__ == "__main__":
    from aiogram import executor

    db.init()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
