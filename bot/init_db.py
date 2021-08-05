import asyncio
import logging

import asyncpg

from config import host, PG_PASS, PG_USER, PG_DATABASE

logging.basicConfig(format=u'%(filename)s [LINE:%(lineno)d] #%(levelname)-8s [%(asctime)s]  %(message)s',
                    level=logging.INFO)


async def create_db():
    create_db_command = open("database/create_db.sql", "r").read()

    logging.info("Connecting to database...")
    conn: asyncpg.Connection = await asyncpg.connect(user=PG_USER,
                                                     password=PG_PASS,
                                                     host=host,
                                                     timeout=10,
                                                     database=PG_DATABASE)
    try:
        await conn.execute(create_db_command)
    except asyncpg.exceptions.DuplicateTableError as e:
        logging.info(f'Db error: {e}')

    await conn.close()

    await conn.close()
    logging.info("Tables created successfully.")


async def create_pool():
    return await asyncpg.create_pool(user=PG_USER,
                                     password=PG_PASS,
                                     host=host)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_db())
