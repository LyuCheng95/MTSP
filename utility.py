import csv

# reads a CSV file and returns every line as a list
# e.g. for a CSV file with the following 2 lines:
#   apple, orange
#   banan, durian
# this function will return this list: [['apple', ' orange'], ['banana', ' durian']]
def list_reader(csv_file):
    the_list = []
    with open(csv_file, 'r') as csvfile:
        csv_reader = csv.reader(csvfile, delimiter = ',')
        for row in csv_reader:
            the_list.append(row)
    return the_list

# used to read parameter.csv. 
# returns [number_trucks, truck_speed, plane_speed]
def parameter_reader(csv_file):
	the_list = list_reader(csv_file)
	return int(the_list[0][0]), float(the_list[0][1]), float(the_list[0][2])


def legality_checking_airline_completeness(truck_paths):
	for path in truck_paths:
		current_path = "".join([x[0] for x in path])
		current_path = current_path.split("O")
		current_path = [len(x) for x in current_path]
		for length in current_path:
			if length % 2 == 1:
				print("airline incompleteness")
				exit()


def legality_checking_airline_capacity(truck_paths, airport_list):
	airport_dict = {}
	for item in airport_list:
		airport_dict[item[0]] = int(item[-1])

	for path in truck_paths:
		current_path = [x for x in path if x[0] ==  "A"]
		current_path = current_path[::2]
		for item in current_path:
			if item not in airport_dict:
				print("no such airport:", item)
				exit()
			elif airport_dict[item] == 0:
				print("run out of capacity", item)
				exit()
			else:
				airport_dict[item] = airport_dict[item] - 1

def checking_if_airports(truck_paths):
	for path in truck_paths:
		current_path = [x for x in path if x[0] ==  "A"]
		if len(current_path) > 0:
			return True
	return False

# checks that all orders have been fulfiled. prints out erroneous conditions
def checking_all_order(truck_paths, order_list):
	order_dict = {}
	for item in order_list:
		order_dict[item[0]] = 1

	for path in truck_paths:
		current_path = [x for x in path if x[0] ==  "O"]
		for item in current_path:
			if item not in order_dict:
				print("no such order", item) 
				exit()
			elif order_dict[item] == 0:
				print("this order has been delivered already", item)
				exit()
			else:
				order_dict[item] = order_dict[item] - 1

    # any undelivered orders?
	for item in order_dict:
		if order_dict[item] != 0:
			print(item, " not delivered")
			exit()

# checks truck paths. prints out erroneous conditions
def check_trucks(truck_paths, truck_number):
	if len(truck_paths) > truck_number:
		print("not enough trucks")
		exit()

	for path in truck_paths:
		if len(path) == 0:
			print("Warning: empty path should be excluded")

# calculates euclidian distance between two points (float)
def distance_calculation(location_A, location_B):
	return ((location_A[1] - location_B[1]) ** 2 + (location_A[2] - location_B[2]) ** 2) ** 0.5


def location_dict_generation(all_list):
	location_dict = {}
	for the_list in all_list:
		for item in the_list:
			location_dict[item[0]] = [item[0], float(item[1]), float(item[2])]
	return location_dict 

# used for computing quality score for Q1
def scoring_q1(truck_paths, location_dict):
	length_list = []
	for path in truck_paths:
		length_list.append(0)
		for e, order in enumerate(path):
			if e == 0:
				length_list[-1] += distance_calculation(location_dict[path[e]], [0, 0, 0])
			if e == len(path) - 1:
				length_list[-1] += distance_calculation(location_dict[path[e]], [0, 0, 0])
			else:
				length_list[-1] += distance_calculation(location_dict[path[e]], location_dict[path[e + 1]])
	print(length_list)
	return max(length_list)

# used for computing quality score for Q2
def scoring_q2(truck_paths, location_dict, truck_speed, plane_speed):
	cost_list = [] # list of time costs for each truck. Each element represents the cost for 1 truck
	for path in truck_paths:
		cost_list.append(0) # to be modified later
		for e, order in enumerate(path):
			take_plane = -1
			if e == 0:
				cost_list[-1] += (distance_calculation(location_dict[path[e]], [0, 0, 0]) / truck_speed)

			if e == len(path) - 1:
				cost_list[-1] += (distance_calculation(location_dict[path[e]], [0, 0, 0]) / truck_speed)
			else:
				if order[0] == "A": # take plane
					if take_plane == -1:
						cost_list[-1] += (distance_calculation(location_dict[path[e]], location_dict[path[e + 1]]) / plane_speed)
					else:
						cost_list[-1] += (distance_calculation(location_dict[path[e]], location_dict[path[e + 1]]) / truck_speed)

					take_plane *= -1

				if order[0] == "O": # drive to order 
					cost_list[-1] += (distance_calculation(location_dict[path[e]], location_dict[path[e + 1]]) / truck_speed)
	return max(cost_list)
