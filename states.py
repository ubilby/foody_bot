from aiogram.fsm.state import State, StatesGroup


class Mode(StatesGroup):
	default = State()
	edit = State()