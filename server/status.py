import json as json_


# Template for code 200 requests so data can easily be added
def ok(d=None, *, json=True):
    code = {'code': 200, 'status': 'OK', 'data': d}
    if json:
        code = json_.dumps(code)
    return code


# The 400 codes shouldn't require any special aruments.
def invalid_request(*, json=True):
    code = {'code': 400, 'status': 'MALFORMED_REQUEST'}
    if json:
        code = json_.dumps(code)
    return code


def unknown_request(*, json=True):
    code = {'code': 400, 'status': 'UNKNOWN_REQUEST'}
    if json:
        code = json_.dumps(code)
    return code


# You can assign the internal server error a number for debugging purposes.
def internal_server_error(n=None, *, json=True):
    status_string = 'INTERNAL_SERVER_ERROR'
    if n is not None:
        status_string += '_{}'.format(n)
    code = {'code': 500, 'status': status_string}
    if json:
        code = json_.dumps(code)
    return code
