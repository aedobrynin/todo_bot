from aiogram import types
from aiogram.dispatcher import FSMContext


async def cancel_command(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply('Cancelled')
