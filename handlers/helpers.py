import typing

from aiogram import types

from models.user_data import UserData


async def get_task_index(message: types.Message) -> typing.Optional[int]:
    try:
        task_index = int(message.text) - 1
        return task_index
    except ValueError:
        await message.reply('It\'s not a number')
        return None


async def check_task_index_bounds(user_data: UserData, task_index: int, message: types.Message) -> bool:
    if user_data is None or task_index not in range(len(user_data.tasks)):
        await message.reply('Bad task index')
        return False
    return True
