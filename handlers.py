from ast import Pass
import os
from parse import parse_data
from aiogram import types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (
    ReplyKeyboardMarkup,
)

class Parse(StatesGroup):
    step1 = State()
    step2 = State()
    step3 = State()


async def process_start_command(message: types.Message):
    await Parse.step1.set()
    await message.answer("Enter search field")


async def process_step1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text:
            data["step1"] = message.text
            await Parse.next()
            await message.answer("Enter min and max price for search (as example 10000-20000)s")


async def process_step2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        answer = message.text
        if (
            len(answer.split("-")) == 2
            and answer.replace("-", "").isdigit()
        ):
            data["step2"] = answer
            kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            b1 = "Create CSV file"
            kb.add(b1)
            await Parse.next()
            await message.answer("Ready to create csv-file", reply_markup=kb)
        else:
            await message.answer("Wrong text. Enter min and max price according to example")


async def process_step3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "Create CSV file":
            await message.answer("Creating csv....")
            print(data["step1"] + data["step2"])
            search_field = data['step1']
            price = data["step2"].split("-")
            file = await parse_data(search_field=search_field, lowest_price=price[0], highest_price=price[1])
            await message.answer_document(document=open(file, 'rb'))
            os.remove(file)
            data.state = None
            await message.answer("Use /start comand to return using bot")


def register_handlers_core(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands=["start"])
    dp.register_message_handler(process_step1, state=Parse.step1)
    dp.register_message_handler(process_step2, state=Parse.step2)
    dp.register_message_handler(process_step3, state=Parse.step3)