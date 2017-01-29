"""
This is a basic client which allows you to send requests and write a dictionary
to send along with it under the "data" key. You can use it to test requests
with different inputs.
"""


import asyncio
import websockets
import json
import sys

try:
    port = sys.argv[1]
    ip = sys.argv[2]
except Exception as e:
    print('Error parsing arguments: {}'.format(e))
    sys.exit()

async def hello():

    async with websockets.connect('ws://{}:{}'.format(ip, port)) as websocket:
        while True:

            inpt = input("request name:> ")
            name = inpt
            value = {}
            while True:

                inpt = input('data key:> ')
                if inpt == '':
                    break
                tmp_list = [inpt]
                inpt = input('data[{}] value:> '.format(tmp_list[0]))
                tmp_list.append(inpt)
                value[tmp_list[0]] = json.loads(inpt)

            await websocket.send( json.dumps({'request': name, 'data': value}) )
            print('Sent "{}"'.format(json.dumps({'request': name, 'data': value})))

            response = await websocket.recv()
            print('(Recieved) ' + str(response) + '\n\n')

asyncio.get_event_loop().run_until_complete(hello())
