from argparse import OPTIONAL
from typing import NamedTuple
from datetime import date
from mydb import add_description_to_db


hard_code_categories = {
    "продукты" : ["продукты", "магазин", "овощи", "фрукты"],
    "транспорт": ["транспорт", "такси", "метро", "taxi"],
    "общепит": ["общепит", "кафе", "перекус"],
    "досуг": ["досуг", "развлечения", "бар", "тусовка"],
    "красота": ["красота"],
    "квартира": ["квартира", "к/у", "аренда", "ку"],
    "быт": ["быт"],
    "дети": ["дети", "школа"],
    "спорт": ["гошаспорт", "татаспорт"]
}


def fill_category_table(categories: dict):
	check_query = """"""
	for category, descriptions in categories.items():
		for description in descriptions:
			if not is_description_in_db(description):
				add_description_to_db(description, category)


class Entry:
	"""Структура распарcенного сообщения о новом расходе"""
	value: int
	description: str
	date: date

	def __init__(self, value, description, date):
		self.value = value
		self.description = description
		self.date = date


	def __str__(self):
		return f"{self.date} {self.description} {self.value}"


	def update(self, entry):
		self.value = entry.value
		self.description = entry.description
		self.date = entry.date


def isCorrect(line: str) -> bool:
	return line.strip().count(" ") == 1


def parse_text_from_input(message: str) -> Entry:
	temp_list = message.lower().split()
	if len(temp_list) != 2:
		return Entry(0,"",date.today())

	temp_list.sort()
	if not temp_list[0].isdigit() or not temp_list[1].isalpha():
		return Entry(0, "", date.today())
	else:
		return Entry(int(temp_list[0]), temp_list[1], date.today())


def parse_text_from_db(text: str) -> Entry:
	temp = text.split()
	match temp:
		case [x, int]:
			return Entry(temp[1], "", temp[0])

	return Entry(temp[2], temp[1], temp[0])
