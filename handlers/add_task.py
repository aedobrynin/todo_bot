import os

from aiogram import types
from aiogram.dispatcher import FSMContext

from states import MainState
from models.user_data import UserData
from models.task import Task


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

    tasks_limit = os.environ.get('TODO_BOT_MAX_TASKS_IN_LIST', default=1000)
    if len(user_data.tasks) > tasks_limit:
        await message.reply(f'You have too much tasks in your list, max tasks count is {tasks_limit}')
        return

    user_data.tasks.append(Task(description=message.text, done=False))
    await user_data.save()
    await message.reply('Your task was added to the list!')