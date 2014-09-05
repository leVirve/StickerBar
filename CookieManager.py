import os
import pickle

class Cookie:
    """ cookie item that contains 'user' and 'cookie' pair
        """
    def __init__(self, user=None, cookie=None):
        self.user = user
        self.cookie = cookie

class CookieJar():
    """ maintain the set of cookies for every users
        """
    def __init__(self, name='__Cookie'):
        self.filename = name + '.dat'
        self.data = dict()

        self.load()

    def load(self):
        try:
            f = open(self.filename, 'rb')
            self.data = pickle.load(f)
        except FileNotFoundError as e:
            f = open(self.filename, 'x')
        except EOFError as e:
            pass
        finally:
            if f is not None:
                f.close()

    def save(self):
        try:
            f = open(self.filename, 'wb')
            pickle.dump(self.data, f)
        except pickle.PicklingError as e:
            raise e
        finally:
            if f is not None:
                f.close()

    def add(self, item):
        self.data[item.user] = item.cookie
        self.save()

    def handle(self, item):
        if self.data[item.user] != item.cookie:
            self.add(item)

    def getItems(self):
        return self.data.items()

    def status(self):
        for k, v in self.getItems():
            print(k, v)
