import numpy as np


from windfarm import Windfarm
from environment_data import Environment

class Windfarm_state():
	def __init__(self, environment, total_windfarm_num=200):
		self.environment = environment
		self.all_windfarm = [Windfarm(k, environment.wind_hist) \
							for k in range(total_windfarm_num)]
        
# 	# 総じて使われていないので削除。
# 	# また、wf.check_present_situationに引数stateは渡せないようにした。
# 	# これは、time_step関数内でwfの更新に、
# 	# ship_planから受け取ったわけではなくwindfarm内で用意された変数`state`を
# 	# 引数とするべきではなく（windfarmは受動的な設計）、
# 	# またship_planからstateを受け取ることもない
# 	#（ship_planの行動はwfにstateを渡すことで表現されるのではなく、
# 	# 船を出航することで表現されている）
# 	# ため。
# 	
# 	def check_need_inspection_all(self):
# 		return [wf.return_check_present_situation('inspection')[0] \
# 				for wf in self.all_windfarm]

# 	def check_need_repair_all(self):
# 		return [wf.return_check_present_situation('repair')[0] \
# 				for wf in self.all_windfarm]

# 	def check_progress_inspection_all(self):
# 		return [wf.return_check_present_situation('inspection')[1] \
# 				for wf in self.all_windfarm]

# 	def check_progress_repair_all(self):
# 		return [wf.return_check_present_situation('repair')[1] \
# 				for wf in self.all_windfarm]

	# ship_planで参照される。
	def check_need_inspection_all(self):
		return [wf.need_inspection for wf in self.all_windfarm]
    
	# ship_planで参照される。
	def check_need_repair_all(self):
		return [wf.need_repair for wf in self.all_windfarm]

	def check_time_from_last_inspection_all(self):
		return [wf.time_from_last_inspection for wf in self.all_windfarm]

	def check_there_is_ship_all(self):
		return [wf.there_is_ship for wf in self.all_windfarm]

	# 動ける風車の数を返す
	def total_not_driving_windfarm(self, windfarm):
		count_need_inspection = 0
		count_need_repair = 0
		for wi in windfarm:
			if wi.need_inspection:
				count_need_inspection += 1
			if wi.need_repair:
				count_need_repair += 1
		return count_need_inspection, count_need_repair

	def total_calc_generated_kwh(self):
		return sum([wf.generated_power for wf in self.all_windfarm]) * 36

	def time_step(self, t):
		for wf in self.all_windfarm:
			wf.check_present_situation(t, self.environment.can_work)
