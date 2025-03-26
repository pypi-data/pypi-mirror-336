import asyncio
import sys
import time


async def play():
    try:
        reader, writer = await asyncio.open_connection(
            #'127.0.0.1', 8888)
            '192.168.2.104', 31335)
        print(f'Successfully connected to: ')
    except OSError:
        print("Can't open connection ")
        sys.exit(0)

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            sys.exit(0)

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

loop.run_until_complete(play())
