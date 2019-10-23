import random
import numpy as np
import matplotlib.pyplot as plt
# <Your Team ID>
# <Team members' names>

# replace the content of this function with your own algorithm

def schedule_q1(orders, number_trucks):
	orders_dict = list_to_dict(orders)

	## random select
	starting_orders = list(map(lambda x: x[0], random.sample(orders, number_trucks)))
	status = initializeStatus(orders_dict, number_trucks, starting_orders)
	remaining_orders = [x for x in list(map(lambda x: x[0], orders)) if x not in [starting_orders]]

	handle_one_order(remaining_orders, status, orders_dict)
	print(status)

	## 
	truck_paths= list(map(lambda x: x['path'], status['truck_status']))
	plot_diagram(orders, truck_paths)
	# print(truck_paths)
	return truck_paths

def handle_one_order(remaining_orders, status, orders_dict):
	order_id = remaining_orders.pop(0)
	for truck_info in status['truck_status']:
		dist_change = add_order_to_truck(truck_info['path'], truck_info['distances'], order_id, orders_dict)
		print(dist_change)

	
def add_order_to_truck(path, distances, id, orders_dict):
	position = orders_dict[id]	

	## find closet order
	shortest_dist = 9999
	cloest_order = ''
	for order in path:
		distance = calculate_distance(position, orders_dict[order])
		if distance < shortest_dist:
			shortest_dist = distance
			cloest_order = order

	## decide adding to which side
	index = path.index(order)
	primary_dist = calculate_distance(orders_dict[cloest_order], position)
	left_secondary_dist = 0
	right_secondary_dist = 0
	left_dist = -distances[index] + primary_dist
	right_dist = -distances[-index - 1] + calculate_distance(orders_dict[cloest_order], position)
	if index == 0 or index == len(path) - 1:
		left_secondary_dist = calculate_distance([0,0], position)
		right_secondary_dist = calculate_distance([0,0], position)
		left_dist += left_secondary_dist
		right_dist += right_secondary_dist
	else:
		left_secondary_dist = calculate_distance(orders_dict[path[index-1]], position)
		right_secondary_dist = calculate_distance(orders_dict[path[index+1]], position)
		left_dist += left_secondary_dist
		right_dist += right_secondary_dist
	if left_dist < right_dist:
		path.insert(index, id)
		distances.pop(index)
		distances.insert(index,left_secondary_dist)
		distances.insert(index+1,primary_dist)
		return left_dist
	else:
		path.insert(index+1, id)
		distances.pop(index+1)
		distances.insert(index+1,primary_dist)
		distances.insert(index+2,right_secondary_dist)
		return right_dist


def initializeStatus(orders_dict, number_trucks, starting_orders):
	status = {}
	truck_status = []
	longest_dist = 0
	for i in range(number_trucks):
		path = [starting_orders[i]]
		distances = [calculate_distance([0,0], orders_dict[starting_orders[i]])]*2
		sum_dist = sum(distances)	
		if sum_dist > longest_dist:
			longest_dist = sum_dist
		truck_status.append({'path':path, 'distances': distances})
	return  {'truck_status':truck_status, 'longest_dist':longest_dist}

def calculate_distance(start, end):
	return ((start[0]-end[0])**2 + (start[1]-end[1])**2)**0.5

def plot_diagram(orders, truck_paths):
	order_dict = list_to_dict(orders)
	truck_colors = [[random.uniform(0,1) for i in range(3)] for j in range(25)]
	xmin = min([float(order[1]) for order in orders])
	xmax = max([float(order[1]) for order in orders])
	ymin = min([float(order[2]) for order in orders])
	ymax = max([float(order[2]) for order in orders])
	for i, id_list in enumerate(truck_paths):
		color = truck_colors[i]
		for id in id_list:
			plt.plot(float(order_dict[id][0]), float(order_dict[id][1]), 'o', color=color, zorder=10, clip_on=False)
	plt.plot(0, 0, 'o', zorder=10, clip_on=False)
	
	plt.show()


def list_to_dict(lst):
	info_dict = {}
	for item in lst:
		info_dict[item[0]]=[float(item[1]), float(item[2])]
	return info_dict 