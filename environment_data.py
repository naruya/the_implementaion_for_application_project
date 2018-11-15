import pandas as pd
import numpy as np

class Environment():
	def __init__(self, data=None, csv_path="data/fukushima_wind.csv"):

		self.day = np.array([1, 1, 1, 1, 0, 0, 0, 0] * 365 * 20)
# 		self.wind_hist, self.can_work, self.broken_program = data

		if data == None:
			wind = self._read_wind_data_from_csv(csv_path)
			wind_power_rank = self._calc_wind_power_rank(wind)
			markov_array = self._make_markov_array(wind_power_rank)
			self.wind_hist = self._make_wind_histgram(markov_array)
			self.can_work = self._calc_time_to_work(self.wind_hist)
		else:
			NotImplementedError
        
	def _read_wind_data_from_csv(self, csv_path):
		df = pd.read_csv(csv_path)[2:]
		wind_over_10_meter = np.power(np.sum(np.power(df, 2), 1), 0.5)
# 		wind_over_15_meter = (15. / 10.) ** (1.0 / 7.0) * wind_over_ten_meter # 150
		return wind_over_10_meter
 
	def _calc_wind_power_rank(self, wind):
		wind_power_rank = np.where(wind>16.98, 4, np.where(wind>10.0, 3, \
						  np.where(wind>8.15, 2, np.where(wind>2.72, 1, 0))))
		return wind_power_rank

	def _make_markov_array(self, wind_power_rank):
		markov_array = np.zeros([5, 5])
		pre_rank = wind_power_rank[0]
		for t in range(1, len(wind_power_rank)):
			temp_rank = wind_power_rank[t]
			markov_array[pre_rank, temp_rank] += 1
			pre_rank = temp_rank
		markov_array = markov_array / np.sum(markov_array, 1).reshape(-1, 1)
		return markov_array

	def _make_wind_histgram(self, markov_array):
		hist = [0, 0]
		for t in range(20 * 365 * 4 - 1):
			pre = hist[-1]
			tmp = np.random.choice(np.arange(5), p=markov_array[pre])
			hist.extend([tmp, tmp])
		wind_hist = np.array(hist)
		return wind_hist

	def _calc_time_to_work(self, wind_hist):
		nice_weather = np.where(wind_hist >= 3, 0, 1)
		return nice_weather & self.day

