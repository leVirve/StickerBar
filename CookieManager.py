import os
import pickle

class Cookie:
    """ cookie item that contains 'user' and 'cookie' pair
    """
    def __init__(self, user=None, bduss=None):
        self.user = user
        self.cookies = 'BDUSS=%s;' % bduss

class CookieJar():
    """ maintain the set of cookies for every users
    """
    def __init__(self, name='__Cookie'):
        self.filename = name + '.dat'
        self.data = self.load()

    def load(self):
        try:
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        except:
            return dict()

    def save(self):
        try:
            with open(self.filename, 'wb') as f:
                pickle.dump(self.data, f)
        except Exception as e:
            raise e

    def update(self, item):
        self.data[item.user] = item.cookie
        self.save()

    def handle(self, item):
        if self.data[item.user] != item.cookie:
            self.update(item)

    def getItems(self):
        return self.data.items()

    def status(self):
        for k, v in self.getItems():
            print(k, v)
