import json
from datetime import date

class Recorder:
	""" 紀錄成功貼吧
	"""
	def __init__(self, filename='sign-succ.json'):
		self.data = dict()
		self.FILE_NAME = filename
		self.load()

	def load(self):
		try:
			with open(self.FILE_NAME, 'r') as f:
				data = json.load(f)
				if data['expiration'] == str(date.today()):
					self.data = data
		except (ValueError, FileNotFoundError) as e:
			pass

	def getlist(self, user):
		self.printSigned(user)	
		return self.data[user] if user in self.data else []

	def printSigned(self, user):
		for bar in self.data[user]:
			print('%s@tieba %s 今日已簽到' % (user, bar))

	def dump(self, user, bar):
		if not user in self.data:
			self.data[user] = list([bar])
		else:
			if bar in self.data[user]:
				return
			self.data[user].append(bar)

	def fin(self):
		self.data['expiration'] = str(date.today())
		with open(self.FILE_NAME, 'w') as f:
			json.dump(self.data, f, indent=4, sort_keys=True)
