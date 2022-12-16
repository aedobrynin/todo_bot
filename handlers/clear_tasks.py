import typing

from aiogram import types

from models.user_data import UserData


async def clear_tasks(message: types.Message):
    user_data: typing.Optional[UserData] = await UserData.get_by_user_id(message.from_id)
    if user_data is None or not user_data.tasks:
        await message.reply('You have no tasks at the moment')
        return

    user_data.tasks = []
    await user_data.save()
    await message.reply('The list was cleared')
