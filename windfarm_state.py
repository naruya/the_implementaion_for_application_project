import numpy as np

from windfarm import Windfarm

class Windfarm_state():
	def __init__(self, environment, total_windfarm_num=200):
		self.environment = environment
		self.all_windfarm = [Windfarm(k, environment.wind_hist, environment.broken_program[k]) \
							for k in range(total_windfarm_num)]
        
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
    
	def total_calc_generated_kwh(self): # TODO: 円じゃね？
		return sum([wf.generated_power for wf in self.all_windfarm]) * 36

	def time_step(self, t):
		for wf in self.all_windfarm:
			wf.check_present_situation(t, self.environment.can_work)
