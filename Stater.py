from aiogram.dispatcher.filters.state import StatesGroup,State

class Stater(StatesGroup):
    name = State()
    age = State()
    contact = State()
    info = State()
    change = State()
    about = State()
    delete = State()
    question = State()
    answer = State()
    revealing = State()
    admin_message = State()
    message_confirmation = State()

    give_info = State()
    ask_info = State()