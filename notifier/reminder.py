import asyncio
import logging
from datetime import datetime

from config import *
from loader import bot
from parser import CryptoPanic, CoinMarketCap
from database.db_commands import DBCommands


class Reminder:
    db_worker = DBCommands()

    def __init__(self):
        self.categories = ['hot', 'losers', 'gainers']

    @staticmethod
    async def sleeping():
        now = datetime.now(tz=timezone)
        seconds = (datetime.strptime('23:00:00', '%H:%M:%S') -
                   datetime.strptime(f'{now.hour}:{now.minute}:{now.second}', '%H:%M:%S')).seconds
        logging.info(f'Sleep {seconds} sec')
        return await asyncio.sleep(seconds)

    async def main(self):
        logging.info(f'Started successfully.')
        while True:
            await self.sleeping()
            await self.delete_messages()
            for i in self.categories:
                if i not in ['losers', 'gainers', 'trending']:
                    text = CryptoPanic().format_data(i)
                else:
                    text = CoinMarketCap().format_data(i)
                try:
                    message = await bot.send_message(chat_id=CHANNEL_ID, text=text, disable_web_page_preview=True)
                    logging.info('Sent')
                except Exception as er:
                    logging.info(er)
                else:
                    await self.db_worker.add_message(message_id=message.message_id, chat_id=message.chat.id)

    async def delete_messages(self):
        """Delete messages from chat."""
        logging.info('Delete messages.')
        for chat_id, message_id in await self.db_worker.get_all_messages():
            try:
                await bot.delete_message(chat_id, message_id)
            except Exception as e:
                logging.info("Delete message error: %s" % e)
            else:
                logging.info("Delete message success.")
        await self.db_worker.delete_messages()


def start_reminder():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Reminder().main())
    loop.close()
