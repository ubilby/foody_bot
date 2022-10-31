from argparse import OPTIONAL
from typing import NamedTuple
from datetime import date


class Entry(NamedTuple):
	"""Структура распарcенного сообщения о новом расходе"""
	value: int
	category: str
	date: date

	def __str__(self):
		return f"{self.date} {self.category} {self.value}"


def isCorrect(line: str) -> bool:
	return line.strip().count(" ") == 1


def parse_text(message: str) -> Entry:
	temp_list = message.lower().split()
	print(temp_list)
	if len(temp_list) != 2:
		return Entry(0,"",date.today())

	temp_list.sort()
	if not temp_list[0].isdigit() or not temp_list[1].isalpha():
		return Entry(0, "", date.today())
	else:
		return Entry(int(temp_list[0]), temp_list[1], date.today())


def parse_text_from_db(text: str) -> Entry:
	temp = text.split()
	return Entry(temp[2], temp[1], temp[0])
