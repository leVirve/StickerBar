import json
import collections
import datetime


class Recorder:
    """ 紀錄成功貼吧
    """
    def __init__(self, filename='sign-succ.json'):
        self.filename = filename
        self.data = collections.defaultdict(list)
        self.load()

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                raw = json.load(f)
                if raw.get('expiration', '') == str(datetime.date.today()):
                    self.data.update(raw)
        except:
            pass

    def get_signed_list(self, user):
        self.print_signed_bar(user)
        return self.data[user]

    def print_signed_bar(self, user):
        for bar in self.data[user]:
            print('%s@tieba %s 今日已簽到' % (user, bar))

    def save(self, user, bar):
        self.data[user].append(bar)

    def dump(self):
        self.data['expiration'] = str(datetime.date.today())
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4, sort_keys=True)


if __name__ == '__main__':
    r = Recorder(filename='test.json')
    r.print_signed_bar('Soreqq')
