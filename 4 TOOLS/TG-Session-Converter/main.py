import asyncio

from telethon import TelegramClient
from loguru import logger



class Convertor:
    def __init__(self):
        self.client = None

    async def connect(self):
        try:
            await self.client.connect()
            logger.success(f"Session exported as 'converted_session.session'")
            await self.client.disconnect()

        except Exception as error:
            logger.error(f'Failed to connect session: {error}')


    def get_data(self):
        try:
            accounts_api_id = int(input('Enter api_id: '))
            accounts_api_hash = input('Enter api_hash: ')

            if accounts_api_id and accounts_api_hash:
                return accounts_api_id, accounts_api_hash
            else:
                return self.get_data()

        except ValueError:
            return self.get_data()


    async def start(self):
        try:
            api_id, api_hash = self.get_data()
            self.client = TelegramClient('converted_session', api_id=api_id, api_hash=api_hash)

            async with self.client:
                await self.connect()

        except Exception as error:
            logger.error(f"Failed to start convertor: {error}")



if __name__ == '__main__':
    convertor = Convertor()
    asyncio.run(convertor.start())
