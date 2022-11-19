from aiogram.filters.base import Filter
from aiogram.types import Message


class AccesedUsersFilter(Filter):
    users: list[str]

    def __init__(self, users: list[str]) -> None:
        self.users = users

    async def __call__(self, message: Message) -> bool:  # [3]
        return message.chat.username in self.users