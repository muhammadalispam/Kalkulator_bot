import logging

from aiogram import Bot, Dispatcher, executor
from aiogram.types import *
from keyboards import *


logging.basicConfig(level=logging.INFO)

BOT_TOKEN = "6786137795:AAFj3mMQ60-NaaDFzX27c7ksVxLCHFgbn-8"


bot = Bot(token=BOT_TOKEN, parse_mode='html')
dp = Dispatcher(bot=bot)


@dp.message_handler(commands=['start'])
async def start_bot(message: Message):
    btn = await calc_btn()
    await message.answer("0", reply_markup=btn)


@dp.callback_query_handler(text_contains='num')
async def calc_num_callback(call: CallbackQuery):
    selected_num = call.data.split(":")[-1]
    now_num = call.message.text
    if now_num != '0':
        new_num = now_num + selected_num
    else:
        new_num = selected_num
    btn = call.message.reply_markup
    await call.message.edit_text(new_num, reply_markup=btn)


@dp.callback_query_handler(text_contains='equ')
async def calc_equ_callback(call: CallbackQuery):
    selected_equ = call.data.split(":")[-1]
    equ_list = ['/', '*', '+', '-', '**', '%', '.']
    now_num = call.message.text
    if now_num[-1] in equ_list:
        await call.answer("❌", show_alert=True)
    else:
        new_num = now_num + selected_equ
        btn = call.message.reply_markup
        await call.message.edit_text(new_num, reply_markup=btn)


@dp.callback_query_handler(text='clear')
async def calc_clear_callback(call: CallbackQuery):
    now_num = call.message.text
    if now_num != '0':
        btn = call.message.reply_markup
        await call.message.edit_text('0', reply_markup=btn)


@dp.callback_query_handler(text='back')
async def calc_back_callback(call: CallbackQuery):
    now_num = call.message.text
    if now_num != '0' and len(now_num) > 1:
        new_num = now_num[:-1]
    else:
        new_num = "0"
    btn = call.message.reply_markup
    await call.message.edit_text(new_num, reply_markup=btn)


@dp.callback_query_handler(text='.')
async def calc_comma_callback(call: CallbackQuery):
    now_num = call.message.text
    equ_list = ['/', '*', '+', '-', '**', '%']
    if now_num[-1] != '.' and now_num[-1] not in equ_list:
        new_num = now_num + '.'
        btn = call.message.reply_markup
        await call.message.edit_text(new_num, reply_markup=btn)


@dp.callback_query_handler(text='result')
async def calc_result_callback(call: CallbackQuery):
    now_num = call.message.text
    new_num = eval(now_num)
    btn = call.message.reply_markup
    await call.message.edit_text(new_num, reply_markup=btn)


if __name__ == '__main__':
    executor.start_polling(dp)
