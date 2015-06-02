import json
from datetime import date


class Recorder:
    """ 紀錄成功貼吧
    """
    def __init__(self, filename='sign-succ.json'):
        self.filename = filename
        self.data = self.load()

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                if data['expiration'] == str(date.today()):
                    return data
        except (ValueError, FileNotFoundError):
            pass
        return dict()

    def getlist(self, user):
        self.print_signed_bar(user)
        return self.data[user] if user in self.data else []

    def print_signed_bar(self, user):
        try:
            for bar in self.data[user]:
                print('%s@tieba %s 今日已簽到' % (user, bar))
        except Exception:
            return

    def dump(self, user, bar):
        try:
            self.data[user].append(bar)
        except KeyError:
            self.data[user] = [bar]

    def fin(self):
        self.data['expiration'] = str(date.today())
        with open(self.filename, 'w') as f:
            json.dump(self.data, f, indent=4, sort_keys=True)
