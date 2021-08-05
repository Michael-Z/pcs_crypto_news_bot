from datetime import datetime

from aiogram import types
from asyncpg import Connection
from asyncpg.exceptions import UniqueViolationError

from bot.loader import db


class DBCommands:
    """Class for working with DB."""
    pool: Connection = db

    ADD_NEW_USER = "INSERT INTO users (chat_id, username, full_name, adding_date) " \
                   "VALUES ($1, $2, $3, $4)"
    COUNT_USERS = "SELECT COUNT (*) FROM users"
    GET_USERS = "SELECT (username, full_name) FROM users"

    async def add_new_user(self):
        """Add new user to db."""
        user = types.User.get_current()
        command = self.ADD_NEW_USER

        chat_id = user.id
        username = user.username
        full_name = user.full_name
        adding_date = datetime.now()

        args = chat_id, username, full_name, adding_date

        try:
            await self.pool.fetchval(command, *args)
        except UniqueViolationError:
            pass

    async def count_users(self):
        """Count users in db."""
        command = self.COUNT_USERS
        record = await self.pool.fetchval(command)
        return record

    async def get_users(self):
        """Get all users from the db."""
        command = self.GET_USERS
        data = await self.pool.fetch(command)

        data = [data[i][0] for i in range(len(data))]

        text = ''
        for num, row in enumerate(data):
            text += f'{num + 1}. @{row[0]} {row[1]}\n'
        return text


database = DBCommands()
