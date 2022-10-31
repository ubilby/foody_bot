import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Text, Filter
from aiogram.utils.keyboard import InlineKeyboardBuilder
import datetime

from my_foos import Entry, parse_text, isCorrect, parse_text_from_db
from keyboards.keyboards import confirm_kb, main_kb, view_entrys_kb, yes_no
from mydb import add_to_db, view_last_10_entry, delete_entry_from_db


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

with open("TOKEN") as file:
    token = file.read()

#временное ограничение доступа
user_filter = lambda msg: msg.chat.username in ["ubilby", "Tata_Gapo"]

# Диспетчер
dp = Dispatcher()


#Метод правки
@dp.message(user_filter, Command(commands=["start", "help"]))
async def view_help(message: types.Message) -> None:
    print(message.chat.username)
    await message.answer("Здесь будет справка", reply_markup = main_kb())


#Метод просмотра последних десяти записей
@dp.message(user_filter, Text(text=["Просмотр записей"]))
async def view_entrys(message: types.Message) -> None:
    entry_list = view_last_10_entry()
    if entry_list:
        await message.answer("Последние записи:")
        for entry in entry_list:
            await message.answer(f"{entry}", reply_markup = view_entrys_kb())
    else:
            await message.answer("Еще нет записей.")


# Считывание сообщения для добавления
@dp.message(user_filter)
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
    print(callback.message.text[17:-2])
    entry = parse_text(callback.message.text[17:-2])
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
        f"Запись отменена {(callback.message.text)}",
        reply_markup = main_kb()
    )
    await callback.message.delete()


@dp.callback_query(Text(text=["remove"]))
async def callback_remove_entry(callback: types.CallbackQuery) -> None:
    entry = parse_text_from_db(callback.message.text)
    delete_entry_from_db(entry)
    await callback.message.answer(
        f"Удалить запись {entry}?",
        #reply_markup = yes_no()
    )
    await callback.message.delete()


# Запуск процесса поллинга новых апдейтов
async def main() -> None:
    # Объект бота
    bot = Bot(token, parse_mode="HTML")
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
