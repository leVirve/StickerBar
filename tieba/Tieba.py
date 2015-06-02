import re
from tieba.utils import *
from tieba.Record import Recorder


class LoginException(Exception):
    pass


class SigninException(Exception):
    pass


class Tieba():
    """ class `Tieba` contains user's name and corresponding infomation
        """
    def __init__(self, username, usercookie=None):
        """ Initial username and cookies.
            :param usercookie: (Optional) 'BDUSS cookie' can be found from
                               browsers
        """
        self.username = username
        self.bduss = self.validated_cookie(usercookie)
        self.recorder = Recorder()

    def run(self):
        """ Main method entry:
                1. Get the tieba list
                2. Sign tiebas
        """
        list(map(self.sign, self.get_bars()))
        self.recorder.dump()

    def get_bars(self):
        """ Get favorite tieba list """
        tiebalist, page = list(), 0
        while True:
            page += 1
            url = 'http://tieba.baidu.com/f/like/mylike?pn=%d' % page
            response = http_request('GET', url)
            bars = re.findall(r'href="\/f\?kw=([^"]+)', response.text)
            tiebalist += [url_decode(bar) for bar in bars]
            if not bars:
                break
        self.recorder.print_signed_bars(self.username)
        return list_process(
            tiebalist,
            self.recorder.get_signed_bars(self.username))

    def validated_cookie(self, bduss_cookie):
        """ Validate the user's cookie,
            and ensuring its login state
        """
        url = 'http://tieba.baidu.com/dc/common/tbs'
        response = http_request('GET', url, headers=gen_headers(bduss_cookie))
        if response['is_login']:
            return re.search(r"BDUSS=(.+);", bduss_cookie).group(1)
        # while cookie is invalid, take login process to get new cookies
        return self.get_new_cookies()

    def get_new_cookies(self):
        """ Login & get the BDUSS cookie
        """
        url = 'http://wappass.baidu.com/passport/login'
        host = 'wappass.baidu.com'
        password = input('密碼: ')
        postdata = {
            'username': self.username,
            'password': password,
            'submit': "%E7%99%BB%E5%BD%95"
        }
        try:
            response = http_request('POST', url,
                                    headers=gen_headers(None, host=host),
                                    data=postdata)
            return response.cookies['BDUSS']
        except:
            raise LoginException('Cookie Error: 密碼錯誤或Tieba忙碌中，請重新登入')

    def sign(self, barname):
        """ Sign with barname """
        url = 'http://tieba.baidu.com/mo/m?kw=' + url_encode(barname)
        response = http_request('GET', url).text
        _re = lambda regex, s: re.search(regex, s).group(1)

        try:
            # get tokens
            addr = _re(r'<a\shref="([^"]+)">签到', response)
            fid = _re(r'fid"\svalue="(\w+)', response)
            tbs = _re(r'name="tbs" value="(.*?)"', response)
            try:
                url = 'http://c.tieba.baidu.com/c/c/forum/sign'
                response = http_request('POST', url,
                                        data=get_sign_data(
                                            self.bduss, fid, tbs, barname)
                                        )
                parsing_print(self.username, barname, response)
            except:
                self.alternative_sign(addr, barname)
            self.recorder.save(self.username, barname)
        except:
            print("%s 失敗" % barname)

    def alternative_sign(self, addr, barname):
        """ Sign with barname in mobile mode """
        url = 'http://tieba.baidu.com' + addr.replace('&amp;', '&')
        response = http_request('POST', url)  # Post?
        if response.ok:
            printf('%s@tieba %s 手機成功簽到' % (self.username, barname))
        raise SigninException('%s@%s 簽到失敗' % (self.username, barname))
