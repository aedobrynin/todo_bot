from aiogram import types
from aiogram.dispatcher import FSMContext

from states import MainState
from models.user_data import UserData


async def mark_done_got_command(message: types.Message):
    await MainState.mark_done.set()
    await message.reply('Enter task number to mark it done or /cancel to cancel')


async def mark_done_got_index(message: types.Message, state: FSMContext):
    try:
        task_index = int(message.text) - 1
    except ValueError:
        await message.reply('It\'s not a number')
        return

    user_data = await UserData.get_by_user_id(message.from_id)
    if user_data is None or task_index not in range(len(user_data.tasks)):
        await message.reply('Bad task index')
        return

    await state.finish()
    user_data.tasks[task_index].done = True
    await user_data.save()
    await message.reply('Marked as done. Good job!')
