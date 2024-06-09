from src.PVZ import PVZ
import asyncio

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    a1 = loop.create_task(PVZ().start())
    loop.run_until_complete(a1)
