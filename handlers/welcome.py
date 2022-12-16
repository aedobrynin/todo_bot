from aiogram import types


async def send_welcome(message: types.Message):
    await message.reply('Hi!\n'
                        "I'm To Do Bot!\n"
                        'You can communicate with me through the commands:\n'
                        '/add - Add new task'
                        '/show - Show list of tasks\n'
                        '/done - Mark task as done\n'
                        '/undone - Mark task as undone\n'
                        '/clear - Clear the whole task list\n'
                        '/delete - Delete a particular task\n'
                        '/help - Show this help\n'
                        'You can also see this command in the menu')
