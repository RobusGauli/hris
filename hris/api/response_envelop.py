import os
from flask import jsonify


COMMON_STATUS_CODES = {
    200: b'OK',
    400: b'Bad Request',
    404: b'Not Found',
    500: b'Internal Server Error',
}


ALL_STATUS_CODES = {
    100: b'Continue',
    101: b'Switching Protocols',
    102: b'Processing',
    200: b'OK',
    201: b'Created',
    202: b'Accepted',
    203: b'Non-Authoritative Information',
    204: b'No Content',
    205: b'Reset Content',
    206: b'Partial Content',
    207: b'Multi-Status',
    208: b'Already Reported',
    226: b'IM Used',
    300: b'Multiple Choices',
    301: b'Moved Permanently',
    302: b'Found',
    303: b'See Other',
    304: b'Not Modified',
    305: b'Use Proxy',
    307: b'Temporary Redirect',
    308: b'Permanent Redirect',
    400: b'Bad Request',
    401: b'Unauthorized',
    402: b'Payment Required',
    403: b'Forbidden',
    404: b'Not Found',
    405: b'Method Not Allowed',
    406: b'Not Acceptable',
    407: b'Proxy Authentication Required',
    408: b'Request Timeout',
    409: b'Conflict',
    410: b'Gone',
    411: b'Length Required',
    412: b'Precondition Failed',
    413: b'Request Entity Too Large',
    414: b'Request-URI Too Long',
    415: b'Unsupported Media Type',
    416: b'Requested Range Not Satisfiable',
    417: b'Expectation Failed',
    422: b'Unprocessable Entity',
    423: b'Locked',
    424: b'Failed Dependency',
    426: b'Upgrade Required',
    428: b'Precondition Required',
    429: b'Too Many Requests',
    431: b'Request Header Fields Too Large',
    500: b'Internal Server Error',
    501: b'Not Implemented',
    502: b'Bad Gateway',
    503: b'Service Unavailable',
    504: b'Gateway Timeout',
    505: b'HTTP Version Not Supported',
    506: b'Variant Also Negotiates',
    507: b'Insufficient Storage',
    508: b'Loop Detected',
    510: b'Not Extended',
    511: b'Network Authentication Required'
}

def record_created_envelop(data, code=201):
    
    return jsonify({
        'data' : data,
        'code' : code,
        'message' : ALL_STATUS_CODES.get(code, 'Not foundd').decode(),
        'status' : 'success'
    })



def records_json_envelop(records, *, code=200):
    
    return jsonify({
        'data' : records,
        'code' : code,
        'message' : ALL_STATUS_CODES.get(code, 'Not found').decode(),
        'status' : 'success'

    })




def record_json_envelop(record, *, code=200):
    
    return jsonify({
        'data' : record,
        'code' : code,
        'message' : ALL_STATUS_CODES.get(code, 'Not found').decode(),
        'status': 'success'
    })

def record_updated_envelop(record, *, code=200):
    return jsonify({
        'data' : record,
        'code' : code,
        'message' : 'updated successfully',
        'status': 'success'
    })


def record_not_updated_env(message='',code=400):
    return jsonify({
        'data' : message,
        'code' : code,
        'message' : 'couldn\'t update',
        'status' : 'fail'
    })

def record_notfound_envelop(message=None, code=404):
    return jsonify({
        'data' : {},
        'code' : code,
        'message' : message if message else ALL_STATUS_CODES.get(code, 'Not found').decode(),
        'status': 'fail'
    })



def record_exists_envelop(message=None, code=409): 
    #409 = conflict
    return jsonify({
        'data' : {},
        'code' : code,
        'message' : message if message else 'Record already exists',
        'status' : 'fail'
    })



def bad_request_envelop(code=400):
    return jsonify({
        'data' : {},
        'code' : code,
        'message' : ALL_STATUS_CODES.get(code, 'Not found').decode(),
        'status': ' fail'
    })


def fatal_error_envelop(code=500):
    return jsonify({
        'data' : {},
        'code' : code, 
        'message' : ALL_STATUS_CODES.get(code, 'Not found').decode(),
        'status' : 'fail'
    })

def missing_keys_envelop(code=400):
    return jsonify(
        {
            'data' : {}, 
            'code' : code, 
            'message' : 'Missing keys', 
            'status' : 'fail'
        }
    )

def length_require_envelop(message=None, code=411):
    return jsonify(
        {
            'data' : {}, 
            'code' : code, 
            'message' : message if message else 'Not sufficient length of values',
            'status' : 'fail'
        }
    )