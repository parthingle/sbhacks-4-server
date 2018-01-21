import socket
import json

message = { "user-id":"John","lat":'+123', "long":"-123", "song":"Paris", "artist":"chainsmokers", "time":time.time()}

while True:
    # accept connections from outside
    (clientsocket, address) = serversocket.accept()
    # now do something with the clientsocket
    # in this case, we'll pretend this is a threaded server
    ct = client_thread(clientsocket)
    ct.run()