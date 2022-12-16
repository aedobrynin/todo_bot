import os
import typing

from redis_om import Migrator
from aredis_om import NotFoundError

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor

from states import MainState
from models.user_data import UserData

bot = Bot(token=os.environ['TODO_BOT_TELEGRAM_BOT_TOKEN'])
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    # TODO: fill help command reply
    await message.reply("Hi!\nI'm To Do Bot!\n")


@dp.message_handler(commands='cancel',
                    state=[MainState.add_task, MainState.delete_task, MainState.mark_done, MainState.mark_undone])
async def cancel_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Cancelled', reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(commands='add')
async def add_task_got_command(message: types.Message):
    await MainState.add_task.set()
    await message.reply('Enter task description or /cancel to cancel')


@dp.message_handler(state=MainState.add_task)
async def add_task_got_description(message: types.Message, state: FSMContext):
    await state.finish()

    length_limit = os.environ.get('TODO_BOT_MAX_TASK_LENGTH', default=200)
    if len(message.text) > length_limit:
        await message.reply(f'Task description is too long, max length is {length_limit}')
        return

    # TODO: save the task
    await message.reply('Your task was added to the list!')


@dp.message_handler(commands='show')
async def show_tasks(message: types.Message):
    user_data: typing.Optional[UserData] = None
    try:
        user_data = await UserData.find(UserData.user_id == message.from_id).first()
    except NotFoundError:
        pass

    if user_data is None or not user_data.tasks:
        await message.reply('You have no tasks at the moment')
        return

    reply_lines = ["Your tasks:"]
    for i, task in user_data.tasks:
        line = f'{i}) {task.description} {"✅" if task.done else ""}'
        reply_lines.append(line)
    await message.reply('\n'.join(reply_lines))


def main():
    Migrator().run()
    executor.start_polling(dp, skip_updates=True)


if __name__ == "__main__":
    main()
