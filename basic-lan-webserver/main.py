from requests import request
from server import run
import status
import socket
import sys

try:
    ip = sys.argv[2]
except:
    ip = socket.gethostbyname(socket.gethostname())
    
port = sys.argv[1]

@request
async def hello(websocket, path, request, args):

    await websocket.send('Hello, world!')

@request
async def echo(websocket, path, request, args):

    await websocket.send( status.ok(''.join(args['msg'])) )

run(ip, port)
