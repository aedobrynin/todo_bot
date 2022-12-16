from aiogram import types


async def send_welcome(message: types.Message):
    # TODO: fill help command reply
    await message.reply("Hi!\nI'm To Do Bot!\n")
