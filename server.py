'''
import asyncio
import json
async def handle_echo(reader, writer):
    data = await reader.read(100)
    #message = data.decode()
    message = json.loads(data.decode())
    print(message['song'])
    addr = writer.get_extra_info('peername')
    print("Received %r from %r" % (message, addr))
    print("Send: %r" % message)
    writer.write('lolreax'.encode())
    await writer.drain()

    print("Close the client socket")
    writer.close()

loop = asyncio.get_event_loop()
coro = asyncio.start_server(handle_echo, '127.0.0.1', 8888, loop=loop)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()


'''

import asyncio

class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = json.loads(data.decode())
        print('Song Received: '+message['song'])

        print('Send: {!r}'.format(message))
        self.transport.write('lolreax'.encode())

        print('Close the client socket')
        self.transport.close()

        ###################################################
        # data = await reader.read(100)
        # #message = data.decode()
        # message = json.loads(data.decode())
        # print(message['song'])
        # addr = writer.get_extra_info('peername')
        # print("Received %r from %r" % (message, addr))
        # print("Send: %r" % message)
        # writer.write('lolreax'.encode())
        # await writer.drain()

        # print("Close the client socket")
        # writer.close()

        ###################################################
loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(EchoServerClientProtocol, '127.0.0.1', 8888)
server = loop.run_until_complete(coro)

# Serve requests until Ctrl+C is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()