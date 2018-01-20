import asyncio
import json
import time
async def tcp_echo_client(message, loop):
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888,
                                                   loop=loop)

    print('Send: %r' % message)
    writer.write((json.dumps(message)).encode())

    data = await reader.read(100)
    print('Received: %r' % data.decode())

    print('Close the socket')
    writer.close()


message = { "user-id":"Sue","lat":'+321', "long":"-321", "song":"Paris", "artist":"chainsmokers", "time":time.time()}
#message=json_message.
loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(message, loop))
loop.close()