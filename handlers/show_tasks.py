import typing

from aiogram import types

from models.user_data import UserData


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
