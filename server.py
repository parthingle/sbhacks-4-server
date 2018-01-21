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
import socket
import asyncio
import json 
import datetime
import time
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://sbhacks4-9f27c.firebaseio.com'
})

# As an admin, the app has access to read and write all data, regradless of Security Rules
ref = db.reference('restricted_access/secret_document/users') ### What does this argument mean?


class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = await json.loads(data.decode())
        #print('Song Received: '+message['song'])

        self.userid = message['user-id']
        self.song = message['song']
        self.time = message['time']
        self.artist = message['artist']
        self.lat = message['lat']
        self.long = message['long']
        self.spotify = message['spotify']

        val, match=self.check_cache()


        self.transport.write('lolreax'.encode())

        print('Close the client socket')
        self.transport.close()

    def check_cache(self):

        #ref.remove() to clear whole database
        all_entries = ref.get()
        for key in list(all_entries.keys()):
            this_spotify = all_entries[key]['spotify']
            for 
        entry = ref.push({'user-id' : self.userid, 'lat' : self.lat, 'long' : self.long, 'time' : self.time, 'song' : self.song, 'artist' : self.artist})
        return (bool(artist_query), artist_query)

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

'''

'''