import os
import json
import datetime
import collections
from tieba.utils import to_json


class Recorder:
    """ 紀錄成功貼吧
    """
    def __init__(self, filename='sign-succ.json'):
        self.filename = filename
        self.data = collections.defaultdict(list)
        if os.path.isfile(self.filename):
            self.load()

    def load(self):
        with open(self.filename, 'r') as f:
            raw = to_json(f)
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
