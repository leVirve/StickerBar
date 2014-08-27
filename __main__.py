"""

    貼吧模擬手機端自動簽到

    Author: Salas

    Create: 2014/08/08

"""

from Tieba import Tieba
from CookieManager import Cookie, CookieJar

def start(user, cookie, cookieJar):
    tieba = Tieba(user, cookie)
    tieba.run()
    # TO-DO: re-try failed tieba
    # tieba.status()

    if tieba.STATUS == 'Cookie Updated':
        print('%s@tieba Cookie in database updated!' % user)
        cookieJar.add(Cookie(user, tieba.cookies))

def main():
    cookieJar = CookieJar()
    for user, cookie in cookieJar.getItems():
        start(user, cookie, cookieJar)

    if not cookieJar.data:
        user = input('New 貼吧使用者: ')
        start(user, '', cookieJar)

if __name__ == '__main__':
    main()
