class Ships():
	def __init__(self, target_windfarm):
		# この船がどこの風車にいるか
		# 港に残り続けるなら -1
		self.target_windfarm = target_windfarm
		# 港にいるかどうか。target_windfarmがあっても夜寄港しているときに大事になる変数。
		self.stay_harbor = False
		# 何してるか。None or 'inspection' or 'repair'
		# 全体で何隻の船が点検にあたっているかをカウントする際に使う。
		self.task = None
