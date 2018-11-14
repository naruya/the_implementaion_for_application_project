import argparse
import numpy as np
import matplotlib.pyplot as plt
import sys
from tqdm import tqdm

from environment_data import Environment
from windfarm_state import Windfarm_state
from ship_plan import Ship_plan

def arg_parse():
	parser = argparse.ArgumentParser()
	parser.add_argument('-n', '--total_number_of_ships',
						type=int, default=6)
	parser.add_argument('-t', '--total_step_by_three_hour',
						type=int, default=int(20*365*(24/3)))
	args = parser.parse_args()
	return args

def main():
	args = arg_parse()

	wind_hist = np.load("data/wind_hist.npy")
	can_work = np.load("data/can_work.npy")
	broken_program = np.load("data/broken_program.npy")

	print("read environment ...")
	environment = Environment(data=(wind_hist, can_work, broken_program))
    
	print("construct windfarm_state ...")
	windfarm_state = Windfarm_state(environment)
    
	print("construct ship_plan ...")
	ship_plan = Ship_plan(args.total_number_of_ships, environment, windfarm_state)
    
	plot_array = np.zeros([200, \
						   args.total_step_by_three_hour])
    
	need_inspection_list = []
	need_repair_list = []
	total_generated_power = []

	for t in tqdm(range(args.total_step_by_three_hour)):
        
		ship_plan.time_step(t)
		windfarm_state.time_step(t)
		plot_array[:, t] = [wf.generating_power for wf in \
							windfarm_state.all_windfarm]

		need_inspection_list.append(sum(windfarm_state.check_need_inspection_all()))
		need_repair_list.append(sum(windfarm_state.check_need_repair_all()))
		total_generated_power.append(windfarm_state.total_calc_generated_kwh())

	print("total_calc_generated_kwh: {:,}".format(windfarm_state.total_calc_generated_kwh()))
	print("total_driving_cost: {:,}".format(ship_plan.total_driving_cost))
	print("repayment cost: {:,}".format(400000000 * args.total_number_of_ships))
	print("total_profit: {:,}".format(windfarm_state.total_calc_generated_kwh() -
						  ship_plan.total_driving_cost - 400000000 *
						  args.total_number_of_ships))

	plt.figure()
	plt.imshow(plot_array[:, 0:1 * 1000])
	plt.savefig("1.png")
	plt.show()
	plt.figure()
	plt.imshow(plot_array[:, 1000:2000])
	plt.savefig("2.png")
	plt.show()
	plt.figure()
	plt.imshow(plot_array[:, -1000:])
	plt.savefig("3.png")
	plt.show()


	plt.figure(figsize=(20, 5))
	plt.plot(np.arange(args.total_step_by_three_hour), need_inspection_list, c="r", label="need_inspection")
	plt.plot(np.arange(args.total_step_by_three_hour), need_repair_list, c="g", label="need_repair")
	plt.legend()
	plt.savefig("data/not_driving_windfarm.png")
	plt.figure(figsize=(20, 5))
	plt.plot(np.arange(args.total_step_by_three_hour), total_generated_power)
	plt.savefig("data/total_generated_power.png")



if __name__ == "__main__":
	sys.exit(main())
