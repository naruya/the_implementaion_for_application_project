import numpy as np

class Windfarm():
	def __init__(self, k, wind_state):
		self.k = k
		self.prob_occur_broken = 0.2/365/(24/3)
		self.wind_state = wind_state
		self.need_repair = False
		self.need_inspection = False
		self.progress_repair_time = 0
		self.progress_inspection_time = 0
		self.time_from_last_inspection = 0

		self.generated_power = 0
		self.generating_power = 0 # plotに使う
		self.there_is_ship = False

	# kWh
	def generate_power(self, t):
		self.generating_power = 0
		if self.need_inspection == False and self.need_repair == False:
			if self.wind_state[t] == 1:
				self.generating_power = 6 * 1900 # 1.9MWh = 1900kWh
			elif self.wind_state[t] == 2 | self.wind_state[t] == 3:
				self.generating_power = 6 * 5000 # 5.0MWh = 5000kWh
		self.generated_power += self.generating_power

	def broken_occasionally(self):
		if not self.need_repair: # 修理中には壊れないよね！
			broken = np.random.choice([0,1], p=[1-self.prob_occur_broken, \
									            self.prob_occur_broken])
			if broken == 1:
				self.need_repair = True
# 				print("broken, windfarm.k=={}".format(self.k))

	def check_need_inspection(self):
		if self.time_from_last_inspection == 4320:
			self.need_inspection = True
			self.progress_inspection_time = 0
		self.time_from_last_inspection += 3

	def make_progress(self, t, tenken):
		# 進捗を生む＆点検や修理が終わったら処理
		# TODO
		# 点検と修理の両方が必要な場合、
		# どちらから始めてもかかる時間は同じなので、とりあえず点検から始める、でよい？
		if self.need_inspection: # repairの進捗は産まない！
			self.progress_inspection_time += self.there_is_ship * tenken[t] * 3
			if self.progress_inspection_time == 36:
				self.need_inspection = False
				self.time_from_last_inspection = 0
				self.progress_inspection_time = 0
				self.there_is_ship = False
		elif self.need_repair:
			self.progress_repair_time += self.there_is_ship * tenken[t] * 3
			if self.progress_repair_time == 120:
				self.need_repair = False
				self.progress_repair_time = 0
				self.there_is_ship = False
                
	# 各タイムステップで呼ばれる関数
	def check_present_situation(self, t, tenken):
		# 点検が必要になったり修理が必要になったりしてないか
		self.broken_occasionally()
		self.check_need_inspection()
		self.make_progress(t, tenken)
		self.generate_power(t)
