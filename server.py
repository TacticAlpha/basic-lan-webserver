import websockets
import asyncio
import requests


def run(ip, port):

    print('Starting server...')
    start_server = websockets.serve(requests.handler, ip, port)

    asyncio.get_event_loop().run_until_complete(start_server)
    print('Server started and listening for requests.')
    asyncio.get_event_loop().run_forever()
