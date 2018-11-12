import numpy as np

from ships import Ships

class Ship_plan():
	def __init__(self, total_number_of_ships, environment, windfarm_state):
		self.total_number_of_ships = total_number_of_ships
		self.all_ships = [Ships() for s in range(total_number_of_ships)]
		self.environment = environment
		self.windfarm_state = windfarm_state
		self.total_driving_cost = 0
		self.driving_cost_per_three_hour = 125000

	def time_step(self, t):
		for ship in self.all_ships:
            
			# 次のwindfarmに出動させる # TODO この関数名内容と合ってない。next action的な内容だと思う。
			self.ship_should_leave_current_windfarm(ship, t)
		self.calc_driving_cost()

    # 毎時間, 沖合に出ている船の数分の運転費を計算する
	def calc_driving_cost(self):
		# 港に残っていない船の数
		number_of_driving_ships = sum([not sh.stay_harbor for sh in self.all_ships])
		# 港に残っていない船の数 × 1stepあたりの運転費
		self.total_driving_cost += number_of_driving_ships * \
									self.driving_cost_per_three_hour

	def ship_should_leave_current_windfarm(self, ship, t):
		# 担当する風車の点検or修理が終わったらorニート
		# TODO 点検中に故障してた場合
		if ship.task == None or \
		(ship.task=='inspection' and not self.windfarm_state.all_windfarm[ship.target_windfarm].need_inspection) or \
		(ship.task=='repair' and not self.windfarm_state.all_windfarm[ship.target_windfarm].need_repair):
			next_windfarm, task = self.select_next_windfarm()
			ship.target_windfarm = next_windfarm
			ship.task = task

		# 担当する風車の点検がまだ終わっていない
# 		else: # TODO elseじゃなくね？
			# TODO next_windfarmが決まった後の昼夜判定
			# TODO 午前3時の時点で出航してほしい。
			# まだ元の風車の点検が終わっていない
			# 夜かどうか
		if not ship.task == None:
			ship.stay_harbor = self.check_night(t)
		else:
			ship.stay_harbor = True

	def select_next_windfarm(self):

# 		戦略1: すべての船が常に点検をする。
# 		tmp = np.argmax(self.windfarm_state.time_from_last_inspection_all())
# 		next_windfarm = self.windfarm_state.all_windfarm[tmp]
# 		next_windfarm.there_is_ship = True
# 		next_windfarm.time_from_last_inspection = 0
# 		next_windfarm.need_inspection = True # 強制的にneed_inspectionだったことにする
# 		task = 'inspection'
# 		return tmp, task

		need_repair_all = np.array(self.windfarm_state.check_need_repair_all())
		there_is_ship_all = np.array(self.windfarm_state.check_there_is_ship_all())
		time_from_last_inspection_all = np.array(self.windfarm_state.check_time_from_last_inspection_all())

		# 戦略2: 戦略1をベースに、
		# 壊れた発電機があるときにはp=1の確率で修理に向かうが
		# その他は常に点検に当てる。        
		# 壊れていてかつ修理船がまだ来ていない発電機が全くない場合
# 		if sum(need_repair_all & ~there_is_ship_all) < 1:
# 			# 船がいるところは time_from_last_inspection を0として扱う
# 			tmp = np.argmax(time_from_last_inspection_all * ~there_is_ship_all) # ~で¬の意
# 			next_windfarm = self.windfarm_state.all_windfarm[tmp]
# 			next_windfarm.there_is_ship = True
# 			next_windfarm.need_inspection = True # 強制的にneed_inspectionだったことにする
# 			task = 'inspection'
# 		# 壊れていてかつ修理船がまだ来ていない発電機がある場合
# 		else:
# 			tmp = np.argmax(need_repair_all & ~there_is_ship_all) # ~で¬の意
# 			next_windfarm = self.windfarm_state.all_windfarm[tmp]
# 			next_windfarm.there_is_ship = True
# 			task = 'repair'
# 			print("repair, windfarm.k=={}".format(tmp))

		# 戦略3: 
		# p を「壊れてる発電機の数」と「sum(time_from_last_inspection_all)」に応じて決める
		# それっぽい値で割って、正規化している
		w_repair = sum(need_repair_all & ~there_is_ship_all)/5 # max5かなっていう # どれだけ故障を許容するかが鍵？
		w_inspection = np.mean(time_from_last_inspection_all)/2160 # max2160かなっていう
		p_repair = w_repair / (w_repair + w_inspection + 1e-12)
		print("{:.2%}, {:.2%}, {:.2%}".format(w_repair, w_inspection, p_repair))
		# 修理するゼ
		if np.random.rand() < p_repair:
			print("repair")
			tmp = np.argmax(need_repair_all & ~there_is_ship_all) # ~で¬の意
			next_windfarm = self.windfarm_state.all_windfarm[tmp]
			next_windfarm.there_is_ship = True
			task = 'repair'
		# 点検するゼ
		else:
			print("inspection")
			# 船がいるところは time_from_last_inspection を0として扱う
			tmp = np.argmax(time_from_last_inspection_all * ~there_is_ship_all) # ~で¬の意
			next_windfarm = self.windfarm_state.all_windfarm[tmp]
			next_windfarm.there_is_ship = True
			next_windfarm.need_inspection = True # 強制的にneed_inspectionだったことにする
			task = 'inspection'
            
		return tmp, task

	# environment.day = 1ならば昼, 0ならば夜
	# 夜ならばTrueが返る.
	def check_night(self, t):
		return self.environment.day[t] == 0