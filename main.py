import asyncio
import os

from redis_om import Migrator
from aiogram import Bot, Dispatcher, executor, types


# Initialize bot and dispatcher
bot = Bot(token=os.environ['TELEGRAM_BOT_TOKEN'])
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm EchoBot!\nPowered by aiogram.")


def main():
    Migrator().run()
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
