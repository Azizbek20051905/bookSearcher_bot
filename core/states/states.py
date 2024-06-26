from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    index = State()

class UpdateMessage(StatesGroup):
    title = State()

class ChannelsLink(StatesGroup):
    name = State()
    link = State()