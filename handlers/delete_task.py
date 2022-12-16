from aiogram import types
from aiogram.dispatcher import FSMContext

from states import MainState
from models.user_data import UserData
import handlers.helpers as helpers


async def delete_task_got_command(message: types.Message):
    await MainState.delete_task.set()
    await message.reply('Enter task index to remove or /cancel to cancel')


async def delete_task_got_index(message: types.Message, state: FSMContext):
    task_index = await helpers.get_task_index(message)
    if task_index is None:
        return

    user_data = await UserData.get_by_user_id(message.from_id)
    if not await helpers.check_task_index_bounds(user_data, task_index, message):
        return

    await state.finish()
    del user_data.tasks[task_index]
    await user_data.save()
    await message.reply('Removed the task')
