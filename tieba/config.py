
UA_WINDOWS = \
    'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:31.0) Gecko/20100101 Firefox/31.0'
UA_ANDROID = 'Mozilla/5.0 (Android; Mobile; rv:30.0) Gecko/30.0 Firefox/30.0'

HOST_TIEBA = 'tieba.baidu.com'

headers = {
    'User-Agent': UA_ANDROID,
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': HOST_TIEBA
}

# For return string mapping
dictionary = {
    '亲，你之前已经签过了': '你今天已經簽到了哦',
}
