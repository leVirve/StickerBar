"""

    貼吧模擬手機端自動簽到

    Author: Salas

    Create: 2014/08/08

"""

from Tieba import Tieba
from CookieManager import Cookie, CookieJar

'''
    :NEW_USER: If you want to add more users, turn this to `True`
'''
NEW_USER = False


def start(user, cookie):
    print('hello, %s' % user)
    tieba = Tieba(user, cookie)
    tieba.run()
    return Cookie(user, tieba.bduss)


def main():
    cookieJar = CookieJar()
    if NEW_USER or not cookieJar.data:
        user = input('新增貼吧使用者: ')
        cookieJar.update(Cookie(user, ''))

    for user, cookie in cookieJar.getItems():
        cookieJar.handle(start(user, cookie))

if __name__ == '__main__':
    main()
