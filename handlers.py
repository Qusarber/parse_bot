import os

from parse import parse_data
from constants import CATEGORY_CHOISE_DICT, CATEGORY_LIST

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
    step4 = State()
    step5 = State()


async def process_start_command(message: types.Message):
    await Parse.step1.set()
    await message.answer("Enter search field")


async def process_step1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text:
            data["step1"] = message.text
            await Parse.next()
            await message.answer("Enter min filter price")


async def process_step2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if (
            message.text.isdigit()
        ):
            data["step2"] = message.text
            await Parse.next()
            await message.answer("Enter max filter price")
        else:
            await message.answer("Enter number!")


async def process_step3(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if (
            message.text.isdigit()
            and message.text > data["step2"]
        ):
            data["step3"] = message.text
            kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            for i in CATEGORY_LIST:
                kb.add(i)
            await Parse.next()
            await message.answer("Please, select category", reply_markup=kb)
        else:
            await message.answer("Enter number! Max price also must be bigger than min price")


async def process_step4(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['step4'] = CATEGORY_CHOISE_DICT.get(f"{message.text}")
            kb = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            kb.add("Create CSV file")
            await Parse.next()
            await message.answer("Ready to create csv-file", reply_markup=kb)
        except:
            await message.answer("Please, make ur choise from button")


async def process_step5(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        if message.text == "Create CSV file":
            await message.answer("Creating csv....")
            file = await parse_data(category=data['step4'], search_field=data['step1'], lowest_price=data["step2"], highest_price=data["step3"])
            await message.answer_document(document=open(file, 'rb'))
            os.remove(file)
            data.state = None
            await message.answer("Use /start comand to return using bot")


def register_handlers_core(dp: Dispatcher):
    dp.register_message_handler(process_start_command, commands=["start"])
    dp.register_message_handler(process_step1, state=Parse.step1)
    dp.register_message_handler(process_step2, state=Parse.step2)
    dp.register_message_handler(process_step3, state=Parse.step3)
    dp.register_message_handler(process_step4, state=Parse.step4)
    dp.register_message_handler(process_step5, state=Parse.step5)