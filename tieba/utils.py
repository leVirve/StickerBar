import json
import urllib
import hashlib
from collections import OrderedDict

import tieba.config as config

try:
    import requests
except ImportError as e:
    print(('本專案相依於 Python Package: `Requests`\n'))
    raise e

HTTP_REQUEST = {
    'GET': requests.get,
    'POST': requests.post,
}

ENCODING = 'gbk'
DATA_ENCODING = 'utf8'
ALTER_ENCODING = 'cp950'


def gen_headers(usercookie, host=config.HOST_TIEBA):
    data = {
        'Cookie': usercookie,
        'Host': host
    }
    config.headers.update(data)
    return config.headers


def get_sign_data(bduss, fid, tbs, barname):
    """ Magic poat data !!! """
    data = (
        ('BDUSS', bduss),
        ('_client_id', '04-00-DA-69-15-00-73-97-08-00-02-00-06-00-3C-43-01-00-34-F4-22-00-BC-35-19-01-5E-46'),
        ('_client_type', '4)'),
        ('_client_version', '1.2.1.17'),
        ('_phone_imei', '641b43b58d21b7a5814e1fd41b08e2a5'),
        ('fid', fid),
        ('kw', barname),
        ('net_type', '3'),
        ('tbs', tbs),
    )
    data = OrderedDict(data)

    signature = ''
    for k, v in data.items():
        signature += (k + '=' + v)
    signature += 'tiebaclient!!!'
    data['sign'] = hashlib.md5(signature.encode(DATA_ENCODING)).hexdigest()
    return data


def get_unsigned_bars(todo_list, success_list):
    return list(set(todo_list) - set(success_list))


def http_request(method, url, headers=config.headers, **kwargs):
    response = HTTP_REQUEST[method](
        url, headers=headers, allow_redirects=False, **kwargs)
    return to_json(response.text) or response


def to_json(data, encode=''):
    try:
        data = json.loads(data, encoding=ENCODING or encode)
    except:
        return dict()
    return data


def url_decode(text):
    return urllib.parse.unquote(text, encoding=ENCODING)


def url_encode(text):
    return urllib.parse.quote(text)


def parsing_print(username, barname, data):
    rank = data['user_info']['user_sign_rank']
    exp = data['user_info']['sign_bonus_point']
    total = data['user_info']['total_sign_num']
    conti = data['user_info']['cont_sign_num']
    miss = data['user_info']['miss_sign_num']
    printf('%s@tieba %s 成功簽到, exp +%s, 本吧第%s個簽到: 連續簽到%s天/累計簽到%s天 - 本月漏簽%s天'
            % (username, barname, exp, rank, conti, total, miss))


def printf(output):
    try:
        print(output)
    except UnicodeEncodeError:
        print(output.encode(ALTER_ENCODING, 'replace')
                    .decode(ALTER_ENCODING, 'replace'), '(請使用能正常顯示UTF8的終端介面)')
