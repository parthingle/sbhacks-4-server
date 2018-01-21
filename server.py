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


log = open('log.txt', 'a')


class EchoServerClientProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

        

    def data_received(self, data):
        message = json.loads(data.decode())
        print('Song Received: '+message['song'])

        self.userid = message['user-id']
        self.song = message['song']
        self.time = message['time']
        self.artist = message['artist']
        self.lat = message['lat']
        self.long = message['long']


        #string = 'user-id: '+message['user-id'] +',song: ' +message['song'] + ',artist: ' + message['artist']+ ',time: '+ str(message['time']) +'\n'
        # log.write(string)
        # log.flush()
        val, match=self.check_cache()

        if(val):
            print("####### MATCH FOUND! ############")
            self.transport.write(("Your match has been found\n").encode())
            print('self.artist: ' + self.artist + '\nretrieved artists: ')
            for key in list(match.keys()):
                # diff = match[key]['time'] - self.time
                # print(datetime.datetime.fromtimestamp(int(diff)).strftime('%Y-%m-%d %H:%M:%S'))
                # new_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # new_sock.connect((match[key]['ip'] ,match[key]['peer'] ))
                print('match[key][ip] = ' + str(match[key]['ip']) + ' math[key][peer] = '+ str(match[key]['peer']))

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

    def check_cache(self):
        '''
        count_dict={}
        with open('log.txt') as lol:
            for line in lol:
                this = line.rstrip().split(',')
                if(this[0] not in count_dict):
                    count_dict[this[0]] = 1
                else:
                    count_dict[this[0]] += 1
        for key in list(count_dict.keys()):
            if(count_dict[key] > 1):
                return True
                break 
        '''
        
        #ref.remove() to clear whole database

        artist_query = ref.order_by_child('artist').equal_to(self.artist).get()
        tcp_sock = self.transport.get_extra_info('socket')

        entry_ip, entry_peer = tcp_sock.getsockname(), tcp_sock.getpeername()
        entry = ref.push({'user-id' : self.userid, 'song' : self.song, 'artist' : self.artist, 'lat' : self.lat, 'long' : self.long, 'time' : self.time, 'ip' : entry_ip, 'port' : entry_peer})
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