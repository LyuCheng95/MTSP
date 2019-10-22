from utility import *
from q1 import schedule_q1
# import numpy as np
# import matplotlib.pyplot as plt

def legality_checking(truck_paths, order_list, number_trucks):
	check_trucks(truck_paths, number_trucks)
	checking_all_order(truck_paths, order_list)
	if checking_if_airports(truck_paths):
		print("no airport in q1")
		exit()

# def plot_orders(orders):
# 	x = [float(order[1]) for order in orders]
# 	y = [float(order[2]) for order in orders]
# 	print(x)
# 	print(y)
# 	plt.plot(x, y, 'o', zorder=10, clip_on=False)
# 	plt.xlim(min(x), max(x))
# 	plt.ylim(min(y), max(y))
# 	plt.show()

# replace these parameters with different csv file locations
order_csv = "./dataset/1/orders.csv"
parameter_csv = "./dataset/1/parameters.csv"

number_trucks, truck_speed, plane_speed = parameter_reader(parameter_csv)
orders = list_reader(order_csv)

# plot_orders(orders)
location_dict = location_dict_generation([orders])

truck_paths = schedule_q1(orders, number_trucks)  # call your function

legality_checking(truck_paths, orders, number_trucks)
print("Score for q1 is:", scoring_q1(truck_paths, location_dict)) # print your score






