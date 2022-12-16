from aiogram import types
from aiogram.dispatcher import FSMContext

from states import MainState
from models.user_data import UserData
import handlers.helpers as helpers


async def mark_undone_got_command(message: types.Message):
    await MainState.mark_undone.set()
    await message.reply('Enter task index to remove the mark or /cancel to cancel')


async def mark_undone_got_index(message: types.Message, state: FSMContext):
    task_index = await helpers.get_task_index(message)
    if task_index is None:
        return

    user_data = await UserData.get_by_user_id(message.from_id)
    if not await helpers.check_task_index_bounds(user_data, task_index, message):
        return

    await state.finish()
    user_data.tasks[task_index].done = False
    await user_data.save()
    await message.reply('Removed the mark')
