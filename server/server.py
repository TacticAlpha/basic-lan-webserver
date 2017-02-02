import websockets
import asyncio
import requests


def run(ip, port, *, client_timeout:int=45, request_timeout:int=2):

    print('Starting server...')

    requests.timeout_delay = client_timeout
    requests.request_timeout = request_timeout

    start_server = websockets.serve(requests.handler, ip, port)

    asyncio.get_event_loop().run_until_complete(start_server)

    print('Server started and listening for requests.')

    asyncio.get_event_loop().run_forever()
