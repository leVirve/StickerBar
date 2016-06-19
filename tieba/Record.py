import os
import json
import logging
import datetime
import collections
from tieba.utils import to_json


FORMAT = '%(asctime)-15s %(clientip)s %(user)-8s %(message)s'
logging.basicConfig(format=FORMAT, filename='signs.log')
logger = logging.getLogger('tieba')


class Recorder:

    """ 紀錄成功貼吧
    """

    def __init__(self, filename='sign-succ.json'):
        self.filename = filename
        self.data = collections.defaultdict(list)
        self.load()

    def load(self):
        if not os.path.isfile(self.filename):
            return
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
        logger.warning('Signs successfully: %s', bar, extra={'user': user})
        self.data[user].append(bar)

    def dump(self):
        self.data['expiration'] = str(datetime.date.today())
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4, sort_keys=True)
