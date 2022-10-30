from aiogram.types import InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def confirm_kb() -> InlineKeyboardBuilder:
	
	kb = InlineKeyboardBuilder()

	buttons = [
		InlineKeyboardButton(text = "Подтвердить", callback_data = "confirm"),
		InlineKeyboardButton(text = "Отменить", callback_data = "cancel")
	]

	for b in buttons:
		kb.add(b)

	return kb


def main_kb() -> ReplyKeyboardMarkup:
	kb = [
		[KeyboardButton(text="Просмотр записей")],
		[KeyboardButton(text="/help")]
	]

	keyboard = ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)

	return keyboard


