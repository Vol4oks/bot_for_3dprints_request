from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command

from loader import dp
from states import StepRequestFor_print3D as srf3D
from utils.db_api.db_commands import add_request, select_user

import datetime
from pathlib import Path

COMMAND_EXIT = "q"
ANSWER_EXIT = "Заявка отменена"

@dp.message_handler(text="/new", state=None)
async def new_request(message: types.Message):
    await message.answer(f"Введите `{COMMAND_EXIT}` для выхода")
    await message.answer("Введите название модели")
    await srf3D.name_product.set()


@dp.message_handler(state=srf3D.name_product)
async def set_name_product(message: types.Message, state: FSMContext):
    name_product = message.text
    user = await select_user(message.from_user.id)
    if message.text == COMMAND_EXIT:
        await message.answer(ANSWER_EXIT)
        await state.reset_state()
    else:
        await state.update_data(name_user=user)
        await state.update_data(name_product=name_product)
        await message.answer("Введите количество моделей, число.")
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
        await message.answer("Отправте файл")
        await srf3D.file_add.set()
    else:
        await message.answer("Не понял вас, попробуйте еще раз\n")
    
@dp.message_handler(state=srf3D.file_add, content_types=types.ContentType.DOCUMENT)
async def set_file(message: types.Message, state: FSMContext):
    path_to_download = Path().joinpath("users_files", f"{message.from_user.id}")
    path_to_download.mkdir(parents=True, exist_ok=True)
    path_to_download = path_to_download.joinpath(f"{datetime.datetime.now().strftime('%d_%m_%Y_%H_%M')}_{message.document.file_name}")
    try:
        await message.document.download(destination=path_to_download)
        #await message.answer(f"Документ был сохранен в путь: {path_to_download}")
        await state.update_data(file_add=path_to_download)
        await state.update_data(file_name=message.document.file_name)
        await message.answer(f"Документ сохранен")
        await message.answer("Введите комментарий.")
        await srf3D.comment.set()
    except Exception as ex:
        await message.answer("Документ не был сохранен")
        await message.answer(f"{ex}")
        await message.answer("Обратитесть к админу или попробуйте еще раз")
        await message.answer(f"Введите `{COMMAND_EXIT}` для выхода")


@dp.message_handler(state=srf3D.file_add, content_types=["text", "sticker", "pinned_message", "photo", "audio", "voice"])
async def no_set_file(message: types.Message, state: FSMContext):
    if message.text == COMMAND_EXIT:
        await message.answer(ANSWER_EXIT)
        await state.reset_state()
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
        f"Документ:\n\t {data.get('file_name')}\n\n"
        f"Комментарий:\n\t {data.get('comment')}\n\n"
        #f"{data} \n"
        "1 - если хотите отправить заявку \n"
        f"{COMMAND_EXIT} - отменить ")
    await srf3D.save.set()


@dp.message_handler(state=srf3D.save)
async def set_save(message: types.Message, state: FSMContext):
    save = message.text
    data = await state.get_data()
    if save.isdigit() and int(save) == 1:
        res = await add_request(
                name_user = data.get('name_user'),
                name_product = data.get('name_product'),
                type_request = '3D',
                quantity = data.get('quantity_product'),
                promptness = data.get('promptness'),
                comment = data.get('comment'),
                path_to_file = data.get('file_add'), 
            )
        await message.answer("Заявка сохранена")
        await message.answer(f"Номер вашей заявки: {res}")
        
        
        await state.reset_state()
    elif save == COMMAND_EXIT:
        Path(data.get('file_add')).unlink()
        await message.answer(ANSWER_EXIT)
        await state.reset_state()

        
    else:
        await message.answer(
            "Не понял вас, попробуйте еще раз\n"
            "1 - если хотите отправить заявку \n"
            f"{COMMAND_EXIT} - отменить ")
   

