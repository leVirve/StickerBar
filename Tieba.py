import re
import urllib
import hashlib
import requests
from collections import OrderedDict

from utils import http_request, gen_headers, update_headers

class Tieba():

    """ class `Tieba` contains user's name and corresponding infomation """

    def __init__(self, username, usercookie=None):
        """
            Initial username and cookies.
            :param usercookie: (Optional) 'BDUSS cookie' can be found from browsers
        """
        self.username = username
        self.cookies = usercookie

        self.headers = gen_headers(usercookie)
        
        self.BDUSS = None
        self.tbs = None

        self.LOGIN_MODE = False
        self.STATUS = ''

    def run(self):
        """ Main method entry:
                1. Check the cookie validity
                2. Get the followed tiebas
                3. Sign tiebas
        """
        if not self.checkCookie():
            return None
        if self.STATUS == 'Login Success':
            self.STATUS = 'Cookie Update'

        barlist = self.getBarList()

        for entry in barlist:
            try:
                self.sign(entry)
            except:
                print('%s@tieba: (Error) Sign %s Fail !' % (self.username, entry))

    def sign(self, barname):
        """

            Sign with barname
            1. Generate request package
            2. Parse response
            3. Display the result

        """

        url = 'http://tieba.baidu.com/mo/m?kw=' + urllib.parse.quote(barname)
        response = http_request('GET', url)
        addr = re.search(r'<a\shref="([^"]+)">签到', response.text)

        if not addr:
            print('%s@tieba %s 今日已簽到!' % (self.username, barname))
            return None

        url = 'http://c.tieba.baidu.com/c/c/forum/sign'

        fid = re.search(r'fid"\svalue="(\w+)', response.text).group(1)
        tbs = re.search(r'name="tbs" value="(.*?)"', response.text).group(1)
        
        data = (
            ('BDUSS', self.BDUSS),
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

        post_sign = ''
        for k, v in data.items():
            post_sign += k + '=' + v
        post_sign += 'tiebaclient!!!'

        data['sign'] = hashlib.md5(post_sign.encode('utf8')).hexdigest()

        response = http_request('POST', url, data=data)

        try:
            exp = response['user_info']['sign_bonus_point']
            print('%s@tieba %s 成功簽到, exp +%s' % (self.username, barname, exp))
            print(response, file=open('mobile_signin.json', 'a', encoding='gbk'))
        except:
            if self.alternative_sign(addr, barname):
                return
            print('%s@tieba %s 簽到失敗 >> %s' % (self.username, barname, response))

    def alternative_sign(self, addr, barname):
        addr = addr.group(1).replace('&amp;', '&')

        url =  'http://tieba.baidu.com' + addr
        response = http_request('POST', url)
        if response.ok:
            print('%s@tieba %s 手機成功簽到' % (self.username, barname))
            return True
        else:
            return False

    def getBarList(self):
        """ Get favorite tieba list """
        tiebalist = list()
        page = 1
        while True:
            url = 'http://tieba.baidu.com/f/like/mylike?pn=%d' % page
            response = http_request('GET', url)

            if not response:
                print('%s Find BarList Error' % self.username)
                return None

            bars = re.findall(r'href="\/f\?kw=([^"]+)', response.text)

            if len(bars):
                for entry in bars:
                    tmp = urllib.parse.unquote(entry, encoding='gbk')
                    tiebalist.append(tmp)
                page += 1
            else:
                break

        return tiebalist

    def checkCookie(self):
        """ Validate the user's cookie,
            and ensuring its login state
        """
        url = 'http://tieba.baidu.com/dc/common/tbs'
        response = http_request('GET', url)

        if response['is_login']:
            bduss = re.search(r"BDUSS=(.+);", self.cookies).group(1)
            self.tbs = response['tbs']
            self.BDUSS = bduss
            return True

        elif not self.LOGIN_MODE:
            self.LOGIN_MODE = True
            status = self.login()
            if status:
                self.STATUS = 'Login Success'
            else: 
                print('Login Fail')
                return False
            return True if self.checkCookie() else False

        else:
            print('%s Cookie Error' % self.username, response)
            return None

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
        self.headers = update_headers(None, host=host)
        response = http_request('POST', url, data=postdata)
        if 'BDUSS' in response.cookies:
            self.cookies = 'BDUSS=%s;' % response.cookies['BDUSS']
            self.headers = update_headers(self.cookies)

        return True if response.status_code == 302 else False
