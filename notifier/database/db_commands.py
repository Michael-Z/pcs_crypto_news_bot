import logging

from asyncpg import Connection

from loader import db


class DBCommands:
    """Class for working with DB."""
    pool: Connection = db

    DELETE_ALL_MESSAGES = "DELETE FROM messages"
    ADD_MESSAGE = "INSERT INTO messages (message_id, chat_id) VALUES ($1, $2)"
    GET_ALL_MESSAGES = "SELECT (chat_id, message_id) FROM messages"

    async def add_message(self, message_id: int, chat_id: int):
        """Add message to db."""
        logging.info('Db: Add new message.')
        command = self.ADD_MESSAGE
        return await self.pool.fetchval(command, message_id, chat_id)

    async def delete_messages(self):
        """Delete all messages."""
        logging.info('Db: Starting deleting old messages.')
        command = self.DELETE_ALL_MESSAGES
        try:
            await self.pool.fetchval(command)
        except Exception as er:
            logging.info('Db Error: %s' % er)
        logging.info('Db: Delete old messages success.')
        return

    async def get_all_messages(self) -> list:
        """Get all messages."""
        command = self.GET_ALL_MESSAGES
        logging.info('Db: Get all messages.')
        data = await self.pool.fetch(command)
        logging.info(data)
        data = [data[i][0] for i in range(len(data))]
        data = [(row[0], row[1]) for row in data]
        return data


database = DBCommands()
