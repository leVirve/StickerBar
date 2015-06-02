import os
import json
import datetime
import collections


class Recorder:
    """ 紀錄成功貼吧
    """
    def __init__(self, filename='sign-succ.json'):
        self.filename = filename
        self.data = collections.defaultdict(list)
        if os.path.isfile(self.filename):
            self.load()

    def clean_json(self, raw):
        try:
            return json.load(raw)
        except:
            return dict()

    def load(self):
        with open(self.filename, 'r') as f:
            raw = self.clean_json(f)
            if raw.get('expiration', '') == str(datetime.date.today()):
                self.data.update(raw)

    def get_signed_bars(self, user):
        return self.data[user]

    def print_signed_bars(self, user):
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
