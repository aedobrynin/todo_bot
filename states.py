from aiogram.dispatcher.filters.state import State, StatesGroup


class MainState(StatesGroup):
    add_task = State()
    mark_done = State()
    mark_undone = State()
    delete_task = State()
