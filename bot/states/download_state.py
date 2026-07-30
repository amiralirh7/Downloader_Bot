from aiogram.fsm.state import StatesGroup, State


class DownloadState(StatesGroup):
    waiting_for_join = State()