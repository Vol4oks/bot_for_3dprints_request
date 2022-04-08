from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from states import StepRequestFor_print3D as srf3D

COMMAND_EXIT = "q"
ANSWER_EXIT = "Заявка отменина"

@dp.message_handler(text="/new", state=None)
async def new_request(message: types.Message):
    await message.answer(f"Введите `{COMMAND_EXIT}` для выхода")
    await message.answer("Введите ваше имя")
    await srf3D.name_user.set()

@dp.message_handler(state=srf3D.name_user)
async def set_name_user(message: types.Message, state: FSMContext):
    name_user = message.text
    if message.text == COMMAND_EXIT:
        await message.answer(ANSWER_EXIT)
        await state.reset_state()
    else:
        await state.update_data(name_user=name_user)
        await message.answer("Введите название модели")
        await srf3D.name_product.set()

@dp.message_handler(state=srf3D.name_product)
async def set_name_product(message: types.Message, state: FSMContext):
    name_product = message.text
    if message.text == COMMAND_EXIT:
        await message.answer(ANSWER_EXIT)
        await state.reset_state()
    else:
        await state.update_data(name_product=name_product)
        await message.answer("Введите количество моделей")
        await srf3D.quantity_product.set()

@dp.message_handler(state=srf3D.quantity_product)
async def set_quantity_product(message: types.Message, state: FSMContext):
    quantity_product = message.text
    if message.text == COMMAND_EXIT:
        await message.answer(ANSWER_EXIT)
        await state.reset_state()
    elif quantity_product.isdigit():
        await state.update_data(quantity_product=int(quantity_product))
        await message.answer("Введите степень важности от 1(срочно) до 5(игрушка для себя)")
        await srf3D.promptness.set()
    else:
        await message.answer("Не понял вас, попробуйте еще раз\n")   

@dp.message_handler(state=srf3D.promptness)
async def set_promptness(message: types.Message, state: FSMContext):
    promptness= message.text
    if message.text == COMMAND_EXIT:
        await message.answer(ANSWER_EXIT)
        await state.reset_state()
    elif promptness.isdigit() and int(promptness) in range(1, 6):
        await state.update_data(promptness=int(promptness))
        await message.answer("Введите комментарий, если нужно")
        await srf3D.comment.set()
    else:
        await message.answer("Не понял вас, попробуйте еще раз\n")


@dp.message_handler(state=srf3D.comment)
async def set_comment(message: types.Message, state: FSMContext):
    comment = message.text
    await state.update_data(comment=comment)
    data = await state.get_data()
    await message.answer(
        "Проверте введенный текст\n\n"
        f"Ваше Имя:\n\t {data.get('name_user')}\n\n"
        f"Имя модели:\n\t {data.get('name_product')}\n\n"
        f"Количесто деталий:\n\t {data.get('quantity_product')}\n\n"
        f"Степень важности:\n\t {data.get('promptness')}\n\n"
        f"Комментарий:\n\t {data.get('comment')}\n\n"
        #f"{data} \n"
        "1 - если хотите отправить заявку \n"
        f"{COMMAND_EXIT} - отменить ")
    await srf3D.save.set()


@dp.message_handler(state=srf3D.save)
async def set_save(message: types.Message, state: FSMContext):
    save = message.text
    if save.isdigit() and int(save) == 1:
        await message.answer("Заявка сохранена")
        await state.reset_state()
    elif save == COMMAND_EXIT:
        await message.answer(ANSWER_EXIT)
        await state.reset_state()
    else:
        await message.answer(
            "Не понял вас, попробуйте еще раз\n"
            "1 - если хотите отправить заявку \n"
            f"{COMMAND_EXIT} - отменить ")
   

