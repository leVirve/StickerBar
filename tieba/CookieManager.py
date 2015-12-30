import os.path
import pickle


class Cookie:

    """ cookie item that contains 'user' and 'cookie' pair
    """

    def __init__(self, user=None, bduss=None):
        self.user = user
        self.cookie = 'BDUSS=%s;' % bduss


class CookieJar():

    """ maintain the set of cookies for every users
    """

    def __init__(self, name='__Cookie'):
        self.filename = name + '.dat'
        self.data = self.load()

    def load(self):
        if os.path.isfile(self.filename):
            with open(self.filename, 'rb') as f:
                return pickle.load(f)
        return dict()

    def save(self):
        with open(self.filename, 'wb') as f:
            pickle.dump(self.data, f)

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
