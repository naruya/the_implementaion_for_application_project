class Ships():
	def __init__(self):
		# この船がどこの風車にいるか
		# 港に残り続けるなら -1
		self.target_windfarm = -1
		# 港にいるかどうか。target_windfarmがあっても夜寄港しているときに大事になる変数。
		self.stay_harbor = False
		# 何してるか。None or 'inspection' or 'repair'
		# 全体で何隻の船が点検にあたっているかをカウントする際に使う。
		self.task = None
