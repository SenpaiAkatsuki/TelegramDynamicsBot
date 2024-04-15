import asyncio
import logging
from pathlib import Path

from pyrogram import Client

from config import load_config


async def main():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    config = load_config('.env')
    this_dir = Path(__file__).parent

    client = Client(
        config.user.phone_number,
        phone_number=config.user.phone_number,
        api_id=config.user.api_id,
        api_hash=config.user.api_hash,

    )

    await client.start()


if __name__ == '__main__':
    asyncio.run(main())
