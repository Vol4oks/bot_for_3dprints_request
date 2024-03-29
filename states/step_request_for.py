from aiogram.dispatcher.filters.state import StatesGroup, State

class StepRequestFor_print3D(StatesGroup):
    name_product = State()
    type_request = State()
    quantity_product = State()
    promptness = State() 
    file_add = State()
    comment = State()
    save = State()

class NewUser(StatesGroup):
    start = State()
    save = State()