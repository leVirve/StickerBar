import json
import requests

import config

HTTP_REQUEST = {
    'GET': requests.get,
    'POST': requests.post,
}

ENCODING = 'gbk'

__headers__ = dict()

def gen_headers(usercookie):
    global __headers__
    __headers__ = config.headers
    return update_headers(usercookie)

def update_headers(usercookie, host=config.headers['Host']):
    __headers__['Cookie'] = usercookie
    __headers__['Host'] = host
    return __headers__

def http_request(method, url, **kwargs):
    response = HTTP_REQUEST[method](url, headers=__headers__, allow_redirects=False, **kwargs)
    return to_json(response.text) or response

def to_json(data):
    try:
        data = json.loads(data, encoding=ENCODING)
    except:
        return None
    return data

def printf():
    # TO-DO: handle Console-Encode print()
    pass
