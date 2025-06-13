import asyncio
from datetime import date, timedelta

from src.serviço_scraper.app import Config
from src.serviço_scraper.app import main as app_main

FIRST_DATE = date(2025, 4, 1)
TODAY = date.today()


async def main():
    current = FIRST_DATE

    while current <= TODAY:
        Config.DATA = current
        await app_main()
        current += timedelta(days=1)


asyncio.run(main())
