import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Text, Filter
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext
import datetime
from os import environ
from os.path import abspath

from my_foos import Entry, parse_text_from_input, isCorrect, parse_text_from_db
from keyboards.keyboards import confirm_kb, main_kb, view_entrys_kb, yes_no
from mydb import add_to_db, view_last_10_entry, delete_entry_from_db, edit_entry_in_db
from myfilter import AccesedUsersFilter
from states import Mode

# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)


token = environ["FOODY_TOKEN"]
# with open("TOKEN") as file:
#     token = file.read()


#временный объект записи для передачи между методами
entry = Entry(0,"",datetime.date.today())


# Диспетчер
dp = Dispatcher()
dp.message.filter(AccesedUsersFilter(users = ["ubilby", "Tata_Gapo"]))


#Метод справки
@dp.message(Command(commands=["start", "help"]))
async def view_help(message: types.Message) -> None:
    print(abspath(""))

    await message.answer(
        "Чтобы добавить запись нужно ввести число и слово,т.е.\
указать сумму и категорию в любом порядке. При редактировании\
и удалении (или отмены удаления) записей требуется подтвердить\
или отменить последние действия прежде чем приступать к новым\
 - мы работаем над тем, чтобы упростить взаимодействие, но пока так",
        reply_markup = main_kb()
    )


# Считывание сообщения для изменения
@dp.message(Mode.edit)
async def read_message(message: types.Message, state: FSMContext, temp_Entry: Entry) -> None:
    if (isCorrect(message.text)):
        await message.answer(
                f"Изменить данные в записи {temp_Entry} на:\n'{message.text}'?",
                reply_markup = confirm_kb()
            )
    else:
        await message.answer(
            f"Некорректный формат ввода. Для изменения записи введите число и слово.\
             Введите новые данные (категорию и сумму) для записи:\n{temp_Entry}", reply_markup = main_kb())


@dp.callback_query(Mode.edit, Text(text=["confirm"]))
async def send_confirm_msg(callback: types.CallbackQuery, state: FSMContext, temp_Entry: Entry) -> None:
    #Здесь будет вызов метода редактирования записи
    new_values = callback.message.text.split("\n")[1][1:-2]
    edit_entry_in_db(temp_Entry, new_values)
    await callback.message.delete()
    await state.clear()
    await callback.message.answer(f"Данные в записи {temp_Entry} изменены на {new_values}")


#добавить информацию об удаленной записи
@dp.callback_query(Mode.edit, Text(text=["cancel"]))
async def send_cancel_msg(callback: types.CallbackQuery, state: FSMContext, temp_Entry: Entry) -> None:
    await callback.message.answer(
        f"Отменено изменение в записи {temp_Entry}",
        reply_markup = main_kb()
    )
    await callback.message.delete()
    await state.clear()


#Метод просмотра последних десяти записей
@dp.message(Text(text=["Просмотр записей"]))
async def view_entrys(message: types.Message) -> None:
    entry_list = view_last_10_entry()
    if entry_list:
        await message.answer("Последние записи:")
        for entry in entry_list:
            await message.answer(f"{entry}", reply_markup = view_entrys_kb())
    else:
            await message.answer("Еще нет записей.")


# Считывание сообщения для добавления
@dp.message()
async def read_message(message: types.Message) -> None:
    if (isCorrect(message.text)):
        await message.answer(
                f"Добавить запись \"{message.text}\"?",
                reply_markup = confirm_kb()
            )
    else:
        await message.answer("Некорректный формат ввода. Для добавления записи введите число и слово", reply_markup = main_kb())


#добавить информацию о поддвержденной записи
@dp.callback_query(Text(text=["confirm"]))
async def send_confirm_msg(callback: types.CallbackQuery) -> None:
    entry = parse_text_from_input(callback.message.text[17:-2])
    print(entry)
    await callback.message.answer(
        f"Запись добавлена: {entry}",
        reply_markup = main_kb()
    )
    add_to_db(entry)
    await callback.message.delete()


#добавить информацию об удаленной записи
@dp.callback_query(Text(text=["cancel"]))
async def send_cancel_msg(callback: types.CallbackQuery) -> None:
    await callback.message.answer(
        f"Запись отменена {(callback.message.text[17:-2])}",
        reply_markup = main_kb()
    )
    await callback.message.delete()


@dp.callback_query(Text(text=["remove"]))
async def callback_remove_entry(callback: types.CallbackQuery) -> None:
    entry = parse_text_from_db(callback.message.text)
    await callback.message.answer(
        f"Удалить запись: {entry}?",
        reply_markup = yes_no()
    )


#добавить информацию о поддвержденной записи
@dp.callback_query(Text(text=["yes"]))
async def send_confirm_msg(callback: types.CallbackQuery) -> None:
    entry = parse_text_from_db(callback.message.text[16:-1])
    delete_entry_from_db(entry)
    await callback.message.answer(
        f"Запись удалена: {entry}",
        reply_markup = main_kb()
    )
    await callback.message.delete()


@dp.callback_query(Text(text=["no"]))
async def send_confirm_msg(callback: types.CallbackQuery) -> None:
    await callback.message.answer(
        f"Удаление записи отменено.",
        reply_markup = main_kb()
    )
    await callback.message.delete()


@dp.callback_query(Text(text=["edit"]))
async def send_confirm_msg(callback: types.CallbackQuery, state: FSMContext, temp_Entry: Entry) -> None:
    temp_Entry.update(parse_text_from_db(callback.message.text))
    await callback.message.answer(
        f"Введите новые данные (категорию и сумму) для записи:\n{temp_Entry}"
    )
    await state.set_state(Mode.edit)


# Запуск процесса поллинга новых апдейтов
async def main() -> None:
    # Объект бота
    bot = Bot(token, parse_mode="HTML")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, temp_Entry = entry)


if __name__ == "__main__":
    asyncio.run(main())