from websockets import exceptions
import status
import time
import math
import json
import io
all_requests = {}


# Decorator
def request(func):

    all_requests[func.__name__] = func


async def __response_handler__(websocket, path, request):

    start_time = time.time()

    name = request['request']

    result = None

    try:
        if request['data'] is not None:
            data = request['data']
        else:
            data = {}
    except KeyError:
        data = {}

    if name in all_requests:

        try:
            await all_requests[name](websocket, path, request, data)
            t = time.strftime( '[ %m/%d | %H:%M:%S | {} | "{}" | {}ms ]'.format( websocket.remote_address[0],
                request['request'], math.ceil(time.time() - start_time) ) )
            print(t)
            return

        except Exception as e:
            result = status.internal_server_error(0)
            print('{}: {}'.format(type(e).__name__, e))

    else:
        result = status.unknown_request()

    await websocket.send(json.dumps(result))
    

async def handler(websocket, path):

    print('Client Connected')

    while True:

        result = None

        try:
            request = json.loads(await websocket.recv())

        except exceptions.ConnectionClosed:
            print('Client disconnected.')
            break

        except TypeError:
            result = status.invalid_request()
            await websocket.send(json.dumps(result))
            continue
            # Skip everything else in this iteration as to not try to
            # process an invalid request

        await __response_handler__(websocket, path, request)
