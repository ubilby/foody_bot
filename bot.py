import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, Text, Filter
from aiogram.utils.keyboard import InlineKeyboardBuilder

from my_foos import Entry, parse_text
from keyboards.keyboards import confirm_kb, main_kb
from mydb import add_to_db, view_last_10_entry


# Включаем логирование, чтобы не пропустить важные сообщения
logging.basicConfig(level=logging.INFO)

with open("TOKEN") as file:
    token = file.read()

user_filter = lambda msg: msg.chat.username in ["ubilby", "Tata_Gapo"]

temp_list=[Entry(0, ""), ]

# Диспетчер
dp = Dispatcher()


#Метод правки
@dp.message(user_filter, Command(commands=["start", "help"]))
async def cmd_random(message: types.Message) -> None:
    print(message.chat.username)
    await message.answer("Здесь будет справка", reply_markup = main_kb())


#Метод просмотра последних десяти записей
@dp.message(user_filter, Text(text=["Просмотр записей"]))
async def cmd_random(message: types.Message) -> None:
    entry_list = view_last_10_entry()
    if entry_list:
        await message.answer("Последние записи:")
        for entry in entry_list:
            await message.answer(f"{entry.category} {entry.value}")
    else:
            await message.answer("Еще нет записей.")


# Считывание сообщения для добавления
@dp.message(user_filter)
async def read_message(message: types.Message) -> None:

    entry = parse_text(message.text)

    if not entry.value or not entry.category:
        await message.answer(
            "Некорректный формат. Введит одно число и одно слово",
            reply_markup = main_kb()
        )

    else:
        await message.answer(
            f"{entry.value} {entry.category}",
            reply_markup = confirm_kb().as_markup()
        )


#добавить информацию о поддвержденной записи
@dp.callback_query(Text(text=["confirm"]))
async def send_confirm_msg(callback: types.CallbackQuery) -> None:
    entry = parse_text(callback.message.text)
    await callback.message.answer(
        f"Запись добавлена: {entry.value} - {entry.category}",
        reply_markup = main_kb()
    )
    add_to_db(entry)
    await callback.message.delete()


#добавить информацию об удаленной записи
@dp.callback_query(Text(text=["cancel"]))
async def send_confirm_msg(callback: types.CallbackQuery) -> None:
    entry = parse_text(callback.message.text)
    await callback.message.answer(
        f"Запись отменена {entry.value} - {entry.category}",
        reply_markup = main_kb()
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
