import os

from aredis_om import Migrator
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils.executor import start_polling

from states import MainState
import handlers.add_task
import handlers.cancel_command
import handlers.show_tasks
import handlers.welcome
import handlers.mark_done
import handlers.mark_undone


def setup_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(handlers.welcome.send_welcome, commands=['start', 'help'])

    dispatcher.register_message_handler(handlers.cancel_command.cancel_command, commands='cancel',
                                        state=[MainState.add_task, MainState.delete_task, MainState.mark_done,
                                               MainState.mark_undone])

    dispatcher.register_message_handler(handlers.add_task.add_task_got_command, commands='add')
    dispatcher.register_message_handler(handlers.add_task.add_task_got_description, state=MainState.add_task)

    dispatcher.register_message_handler(handlers.show_tasks.show_tasks, commands='show')

    dispatcher.register_message_handler(handlers.mark_done.mark_done_got_command, commands='done')
    dispatcher.register_message_handler(handlers.mark_done.mark_done_got_index, state=MainState.mark_done)

    dispatcher.register_message_handler(handlers.mark_undone.mark_undone_got_command, commands='undone')
    dispatcher.register_message_handler(handlers.mark_undone.mark_undone_got_index, state=MainState.mark_undone)


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
