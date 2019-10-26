import random
import numpy as np
# import matplotlib.pyplot as plt
import math
# <Your Team ID>
# <Team members' names>

# replace the content of this function with your own algorithm

def schedule_q1(orders, number_trucks):
	spatial_index_dimention = [10,10]
	no_of_trails = 200
	orders_dict = list_to_dict(orders)
	orders_spatial_index, xmin, ymin, xgap, ygap = build_spatial_index(orders, orders_dict, spatial_index_dimention)

	# plot_index = [j for sub in orders_spatial_index for j in sub] 
	# plot_diagram(orders, plot_index)

	## random select
	best_score = 99999
	truck_paths = []
	for run in range(no_of_trails):
		print('runing...', run)
		starting_orders = list(map(lambda x: x[0], random.sample(orders, number_trucks)))
		status = initializeStatus(orders_dict, number_trucks, starting_orders)
		# while(len(status['allocated'].keys()) != len(orders)):

		## 1st run, by index
		for i, row in enumerate(orders_spatial_index):
			for j, curr_orders in enumerate(row):
				if not curr_orders:
					continue
				checking_orders = load_checking_orders(i, j, orders_spatial_index)
				checking_orders = [order for order in checking_orders if order in status['allocated'].keys()]
				if not checking_orders:
					continue
				for order_id in curr_orders:
					if order_id in status['allocated'].keys():
						continue
					close_sequence = compute_close_sequence(order_id, checking_orders, orders_dict)
					handle_one_order(order_id, close_sequence, status, orders_dict)

		## handle remainings, by order, local reign
		remaining_copy = [o for o in list(status['remaining_orders'])]
		for order_id in remaining_copy:
			position = orders_dict[order_id]
			i, j = find_order_from_index(position, xmin, ymin, xgap, ygap)
			checking_orders = load_checking_orders(i, j, orders_spatial_index)	
			checking_orders = [order for order in checking_orders if order in status['allocated'].keys()]
			if not checking_orders:
				print('!!! why got such strange order !!!')
				continue
			handle_one_order(order_id, checking_orders, status, orders_dict)
		
		## fit the strange orders into near trucks, brutal force 
		remaining_copy = [o for o in list(status['remaining_orders'])]
		if remaining_copy:
			for order_id in remaining_copy:
				close_sequence = compute_close_sequence(order_id, list(orders_dict.keys()), orders_dict)
				close_sequence = [o for o in close_sequence if o not in remaining_copy]
				handle_one_order(order_id, close_sequence, status, orders_dict)
		if status['longest_dist'] < best_score:
			truck_paths= list(map(lambda x: x['path'], status['truck_status']))

	## optmizing  
	distances = list(map(lambda x: sum(x['distances']), status['truck_status']))
	sorted_distances = sorted(distances)
	print(sorted_distances)
	# plot_diagram(orders, truck_paths)
	return truck_paths

def find_order_from_index(position, xmin, ymin, xgap, ygap):
	i = math.floor((position[0] - xmin - 0.00000001) / xgap)
	j = math.floor((position[1] - ymin - 0.00000001) / ygap)
	return [i, j]

def compute_close_sequence(order_id, checking_orders, order_dict):
	sorting_orders = checking_orders[:]
	sorting_orders.sort(key=lambda x: calculate_distance(order_dict[order_id], order_dict[x]))
	return sorting_orders

def load_checking_orders(row, col, spatial_index):
	'''
	find surrounding blocks
	'''
	checking_orders = spatial_index[row][col][:]
	if row != 0:
		checking_orders.extend(spatial_index[row-1][col][:])
		if col != 0:
			checking_orders.extend(spatial_index[row-1][col-1][:])
		if col != len(spatial_index[0])-1:
			checking_orders.extend(spatial_index[row-1][col+1][:])
	if row != len(spatial_index)-1:
		checking_orders.extend(spatial_index[row+1][col][:])
		if col != 0:
			checking_orders.extend(spatial_index[row+1][col-1][:])
		if col != len(spatial_index[0])-1:
			checking_orders.extend(spatial_index[row+1][col+1][:])
	if col != 0:
		checking_orders.extend(spatial_index[row][col-1][:])
	if col != len(spatial_index[0])-1:
		checking_orders.extend(spatial_index[row][col+1][:])
	return checking_orders

def build_spatial_index(orders, orders_dict, dimention):
	ids = list(orders_dict.keys())
	indexed_list = [[[] for j in range(dimention[1])] for i in range(dimention[0])]
	xmin = min([float(order[1]) for order in orders])
	xmax = max([float(order[1]) for order in orders])
	ymin = min([float(order[2]) for order in orders])
	ymax = max([float(order[2]) for order in orders])
	xgap = (xmax-xmin)/dimention[0]
	ygap = (ymax-ymin)/dimention[1]
	for ix, x_lower in enumerate(np.arange(xmin, xmax, xgap)):
		x_upper = x_lower + xgap
		for iy, y_lower in enumerate(np.arange(ymin, ymax, ygap)):
			y_upper = y_lower + ygap
			for order_id in ids[:]:
				if orders_dict[order_id][0] < x_upper and orders_dict[order_id][0] >= x_lower:
					if orders_dict[order_id][1] < y_upper and orders_dict[order_id][1] >= y_lower:
						indexed_list[ix][iy].append(order_id)
						ids.remove(order_id)
	return [indexed_list, xmin, ymin, xgap, ygap]

def handle_one_order(order_id, close_sequence, status, orders_dict):
	lowest_total_dist = 999
	best_truck_index = 0
	best_insert_position = 0
	insert_dist_1 = 0
	insert_dist_2 = 0
	best_total_dist = 0
	for allocated_order_id in close_sequence:
		truck_status = status['truck_status'][status['allocated'][allocated_order_id]] 
		dist_changed, insert_position, dist_1, dist_2= compute_dist_changed(truck_status['path'], truck_status['distances'], order_id, allocated_order_id, orders_dict)
		total_dist = sum(truck_status['distances']) + dist_changed
		if total_dist < lowest_total_dist:
			lowest_total_dist = total_dist
			best_truck_index = status['allocated'][allocated_order_id] 
			best_insert_position = insert_position
			insert_dist_1 = dist_1
			insert_dist_2 = dist_2
			best_total_dist = total_dist
	add_order_to_truck(order_id, status, best_truck_index, best_insert_position, insert_dist_1, insert_dist_2, best_total_dist)

def add_order_to_truck(order_id, status, truck_index, insert_position, dist_1, dist_2, total_dist):
	status['truck_status'][truck_index]['path'].insert(insert_position, order_id)
	status['truck_status'][truck_index]['distances'].pop(insert_position)
	status['truck_status'][truck_index]['distances'].insert(insert_position,dist_1)
	status['truck_status'][truck_index]['distances'].insert(insert_position+1,dist_2)
	status['allocated'][order_id] = truck_index 
	if status['longest_dist'] < total_dist:
		status['longest_dist'] = total_dist
	status['remaining_orders'].remove(order_id)

def compute_dist_changed(path, distances, order_id, allocated_order, orders_dict):
	position = orders_dict[order_id]	
	## decide adding to which side
	index = path.index(allocated_order)
	primary_dist = calculate_distance(orders_dict[allocated_order], position)
	left_secondary_dist = 0
	right_secondary_dist = 0
	left_dist = -distances[index] + primary_dist
	right_dist = -distances[-index - 1] + calculate_distance(orders_dict[allocated_order], position)
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
		return [left_dist, index, left_secondary_dist, primary_dist]
	else:
		return [right_dist, index+1, primary_dist, right_secondary_dist]

def initializeStatus(orders_dict, number_trucks, starting_orders):
	truck_status = []
	longest_dist = 0
	allocated = {order: i for i, order in enumerate(starting_orders)}
	remaining_orders = {x for x in orders_dict.keys() if x not in starting_orders}
	for i in range(number_trucks):
		path = [starting_orders[i]]
		distances = [calculate_distance([0,0], orders_dict[starting_orders[i]])]*2
		sum_dist = sum(distances)	
		if sum_dist > longest_dist:
			longest_dist = sum_dist
		truck_status.append({'path':path, 'distances': distances})
	return  {'truck_status':truck_status, 'longest_dist':longest_dist, 'allocated': allocated, 'remaining_orders': remaining_orders}

def calculate_distance(start, end):
	return ((start[0]-end[0])**2 + (start[1]-end[1])**2)**0.5

# def plot_diagram(orders, truck_paths): 
# 	order_dict = list_to_dict(orders)
# 	truck_colors = [[random.uniform(0,1) for i in range(3)] for j in range(len(truck_paths))]
# 	for i, id_list in enumerate(truck_paths):
# 		color = truck_colors[i]
# 		for id in id_list:
# 			plt.plot(float(order_dict[id][0]), float(order_dict[id][1]), 'o', color=color, zorder=10, clip_on=False)
# 	plt.plot(0, 0, 'o', zorder=10, clip_on=False)
# 	plt.show()

def list_to_dict(lst):
	info_dict = {}
	for item in lst:
		info_dict[item[0]]=[float(item[1]), float(item[2])]
	return info_dict 