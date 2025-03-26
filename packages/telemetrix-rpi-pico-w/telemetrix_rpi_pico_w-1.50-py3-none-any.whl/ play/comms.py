import asyncio
import socket
import sys


class Player:

    def __init__(self, loop):
        self.ip_address = '192.168.2.102'
        self.ip_port = 31335
        self.loop = loop
        self.loop.run_until_complete(self.init_connection())
        self.reader = None
        self.writer = None

    async def init_connection(self):
        try:
            self.reader, self.writer = await asyncio.open_connection(
                self.ip_address, self.ip_port)

            print(f'Successfully connected to: {self.ip_address}:{self.ip_port}')
            # while True:
            #     try:
            #         await asyncio.sleep(.1)
            #     except KeyboardInterrupt:
            #         sys.exit(0)
        except OSError:
            print("Can't open connection to " + self.ip_address)
            sys.exit(0)

    async def write(self, data):
        """
        This method writes sends data to the IP device
        :param data:

        :return: None
        """
        # we need to convert data formats,
        # so all of the below.
        output_list = []

        # create an array of integers from the data to be sent
        for x in data:
            # output_list.append((ord(x)))
            output_list.append(x)

        # now convert the integer list to a bytearray
        to_wifi = bytearray(output_list)
        self.write(to_wifi)
        # print(f' to_wifi {to_wifi}')
        # await self.writer.drain()

    async def read(self, num_bytes=1):
        """
        This method reads one byte of data from IP device

        :return: num_bytes
        """
        buffer = await self.reader.read(1)

        # print(f'the buffer: {buffer}')
        return buffer

    async def loopback(self, data):
        command = [0, ord(data)]
        await self._send_command(command)

    async def _send_command(self, command):
        """
        This is a private utility method.


        :param command:  command data in the form of a list

        """
        # the length of the list is added at the head
        command.insert(0, len(command))

        send_message = bytes(command)

        await self.write(bytearray(send_message))

        await asyncio.sleep(.2)

        buffer = await self.read()
        print(buffer)
        await asyncio.sleep(1)


loopx = asyncio.new_event_loop()
asyncio.set_event_loop(loopx)
z = Player(loopx)
loopx.run_until_complete(z.loopback('a'))
