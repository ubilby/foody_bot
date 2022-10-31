from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup

def confirm_kb() -> InlineKeyboardMarkup:
	
	kb = InlineKeyboardBuilder()

	buttons = [
		InlineKeyboardButton(text = "Подтвердить", callback_data = "confirm"),
		InlineKeyboardButton(text = "Отменить", callback_data = "cancel")
	]

	for b in buttons:
		kb.add(b)

	return kb.as_markup()


def view_entrys_kb() -> InlineKeyboardMarkup:
	
	kb = InlineKeyboardBuilder()

	buttons = [
		InlineKeyboardButton(text = "Изменить", callback_data = "edit"),
		InlineKeyboardButton(text = "Удалить", callback_data = "remove")
	]

	for b in buttons:
		kb.add(b)

	return kb.as_markup()


def yes_no() -> InlineKeyboardMarkup:
	
	kb = InlineKeyboardBuilder()

	buttons = [
		InlineKeyboardButton(text = "Да", callback_data = "yes"),
		InlineKeyboardButton(text = "Нет", callback_data = "no")
	]

	for b in buttons:
		kb.add(b)

	return kb.as_markup()


def main_kb() -> ReplyKeyboardMarkup:
	kb = [
		[KeyboardButton(text="Просмотр записей")],
		[KeyboardButton(text="/help")]
	]

	keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

	return keyboard


