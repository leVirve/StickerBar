import re

from utils import *

class Tieba():
    """ class `Tieba` contains user's name and corresponding infomation 
        """
    def __init__(self, username, usercookie=None):
        """ Initial username and cookies.
            :param usercookie: (Optional) 'BDUSS cookie' can be found from browsers
        """
        self.username = username
        self.cookies = usercookie
        self.bduss = None
        self.STATUS = ''

    def run(self):
        """ Main method entry:
                1. Check the cookie validity
                2. Get the tieba list
                3. Sign tiebas
        """
        try:
            self.checkCookie()
        except ValueError:
            if self.login():
                self.STATUS = 'Cookie Updated'
            else:
                printf('%s@tieba Cookie Error: 密碼錯誤或請重新登入' % self.username)

        for entry in self.getBarList():
            try:
                self.sign(entry)
            except:
                printf('%s@tieba: (Error) Sign %s Fail !' % (self.username, entry))

        return self.STATUS

    def checkCookie(self):
        """ Validate the user's cookie,
            and ensuring its login state
        """
        url = 'http://tieba.baidu.com/dc/common/tbs'
        response = http_request('GET', url, headers=gen_headers(self.cookies))

        if response['is_login']:
            self.bduss = re.search(r"BDUSS=(.+);", self.cookies).group(1)
            return True
        raise ValueError

    def getBarList(self):
        """ Get favorite tieba list """
        tiebalist = list()
        page = 0
        while True:
            page += 1
            url = 'http://tieba.baidu.com/f/like/mylike?pn=%d' % page
            response = http_request('GET', url)
            bars = re.findall(r'href="\/f\?kw=([^"]+)', response.text)
            if not bars:
                return tiebalist
            tiebalist += [url_decode(bar) for bar in bars]

    def login(self):
        """ Login to the server
            Get the BDUSS cookie
        """
        url = 'http://wappass.baidu.com/passport/login'
        host = 'wappass.baidu.com'

        password = input('密碼: ')
        postdata = {
            'username': self.username,
            'password': password,
            'submit': "%E7%99%BB%E5%BD%95"
        }
        response = http_request('POST', url, 
            headers=gen_headers(None, host=host), data=postdata)
        if 'BDUSS' in response.cookies:
            self.cookies = 'BDUSS=%s;' % response.cookies['BDUSS']
            self.checkCookie()
        return True if response.status_code == 302 else False

    def sign(self, barname):
        """ Sign with barname """

        url = 'http://tieba.baidu.com/mo/m?kw=' + url_decode(barname)
        response = http_request('GET', url)

        addr = re.search(r'<a\shref="([^"]+)">签到', response.text)
        if not addr:
            printf('%s@tieba %s 今日已簽到!' % (self.username, barname))
            return

        fid = re.search(r'fid"\svalue="(\w+)', response.text).group(1)
        tbs = re.search(r'name="tbs" value="(.*?)"', response.text).group(1)
        url = 'http://c.tieba.baidu.com/c/c/forum/sign'
        response = http_request('POST', url, data=get_sign_data(self.bduss, fid, tbs, barname))

        try:
            parsing_print(username, barname, response)
        except:
            if self.alternative_sign(addr.group(1), barname):
                return
            printf('%s@tieba %s 簽到失敗 >> %s' % (self.username, barname, response))

    def alternative_sign(self, addr, barname):
        url =  'http://tieba.baidu.com' + addr.replace('&amp;', '&')
        response = http_request('POST', url)

        if response.ok:
            printf('%s@tieba %s 手機成功簽到' % (self.username, barname))
            return True
        return False
