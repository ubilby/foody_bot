from typing import NamedTuple

class Entry(NamedTuple):
    """Структура распарcенного сообщения о новом расходе"""
    value: int
    category: str


def parse_text(message: str) -> Entry:
	temp_list = message.lower().split()
	if len(temp_list) != 2:
		return Entry(0,"")

	temp_list.sort()
	if not temp_list[0].isdigit() or not temp_list[1].isalpha():
		return Entry(0,"")
	else:
		return Entry(int(temp_list[0]), temp_list[1])