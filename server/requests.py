from websockets import exceptions
import warnings
import status
import time
import math
import json
import io

# If one of these isn't defined, the default will run
events = [
    'on_client_connect', # Passes the remote_address
    'on_client_disconnect' # Passes the remote_address
    'on_request' # Passes bool for success and remote_address
]

def on_client_connect(remote_address):
    print('{} has connected'.format(':'.join(remote_address) ))


def on_client_disconnect(remote_address):
    print('{} has disconnected'.format(':'.join(remote_address) ))


def on_request(success, remote_address):
    if success:
        status = 'SUCCESSFUL'
    else:
        status = 'FAILED'
    t = time.strftime( '[ %m/%d | %H:%M:%S | {} | "{}" | {}ms | {} ]'.format( websocket.remote_address[0],
        request['request'],
        math.ceil(time.time() - start_time),
        status ) )
    print(t)


all_requests = {}
# Decorator
def request(func):
    all_requests[func.__name__] = func


all_events = {
    'on_client_connect': on_client_connect,
    'on_client_disconnect': on_client_disconnect,
    'on_request': on_request,
}

# Also a decorator
def event(func):
    name = func.__name__

    if name not in events:
        warnings.warn("Event {} was added but will never be called, it's not in list of valid events. ({})".format(
            name, ', '.join(events)
        ))

    all_events[name] = func


async def __response_handler__(websocket, path, request):

    start_time = time.time()

    name = request['request']

    result = None

    if name in all_requests:

        try:
            result = status.ok( await all_requests[name](websocket, path, request) )

        except Exception as e:
            result = status.internal_server_error(0)
            print('{}: {}'.format(type(e).__name__, e))

    else:
        result = status.unknown_request()

    await websocket.send(json.dumps(result))

    if result['code'] == 200:
        success = True

    else:
        sucess = False

    all_events['on_request'](success, websocket.remote_address)


async def handler(websocket, path):

    all_events['on_client_connect'](websocket.remote_address)

    while True:

        result = None

        try:
            request = json.loads(await websocket.recv())
        except exceptions.ConnectionClosed:
            all_events['on_client_disconnect'](websocket.remote_address)
            break

        except TypeError:
            result = status.invalid_request()
            await websocket.send(json.dumps(result))
            continue
            # Skip everything else in this iteration as to not try to
            # process an invalid request

        await __response_handler__(websocket, path, request)
