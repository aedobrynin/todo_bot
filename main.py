import os
import typing

from aredis_om import Migrator

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.utils.executor import start_polling

from states import MainState
from models.user_data import UserData
from models.task import Task


async def send_welcome(message: types.Message):
    # TODO: fill help command reply
    await message.reply("Hi!\nI'm To Do Bot!\n")


async def cancel_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Cancelled', reply_markup=types.ReplyKeyboardRemove())


async def add_task_got_command(message: types.Message):
    await MainState.add_task.set()
    await message.reply('Enter task description or /cancel to cancel')


async def add_task_got_description(message: types.Message, state: FSMContext):
    await state.finish()

    length_limit = os.environ.get('TODO_BOT_MAX_TASK_LENGTH', default=200)
    if len(message.text) > length_limit:
        await message.reply(f'Task description is too long, max length is {length_limit}')
        return

    user_data = await UserData.get_or_make_new(message.from_id)
    user_data.tasks.append(Task(description=message.text, done=False))
    await user_data.save()
    await message.reply('Your task was added to the list!')


async def show_tasks(message: types.Message):
    user_data: typing.Optional[UserData] = await UserData.get_by_user_id(message.from_id)
    if user_data is None or not user_data.tasks:
        await message.reply('You have no tasks at the moment')
        return

    reply_lines = ["Your tasks:"]
    for i, task in enumerate(user_data.tasks):
        line = f'{i + 1}) {task.description} {"✅" if task.done else ""}'
        reply_lines.append(line)
    await message.reply('\n'.join(reply_lines))


def setup_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(send_welcome, commands=['start', 'help'])
    dispatcher.register_message_handler(cancel_command, commands='cancel',
                                        state=[MainState.add_task, MainState.delete_task, MainState.mark_done,
                                               MainState.mark_undone])
    dispatcher.register_message_handler(add_task_got_command, commands='add')
    dispatcher.register_message_handler(add_task_got_description, state=MainState.add_task)
    dispatcher.register_message_handler(show_tasks, commands='show')


async def on_startup(dispatcher):
    await Migrator().run()
    setup_handlers(dispatcher)


def main():
    bot = Bot(token=os.environ['TODO_BOT_TELEGRAM_BOT_TOKEN'])
    storage = MemoryStorage()
    dispatcher = Dispatcher(bot, storage=storage)
    start_polling(dispatcher, on_startup=on_startup)


if __name__ == "__main__":
    main()
