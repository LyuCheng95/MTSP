import random
import numpy as np
import matplotlib.pyplot as plt
# <Your Team ID>
# <Team members' names>

# replace the content of this function with your own algorithm

def schedule_q1(orders, number_trucks):
	truck_colors = [[random.uniform(0,1) for i in range(3)] for j in range(25)]
	truck_paths = [[orders[random.randint(0, len(orders)-1)][0]] for i in range(25)]
	plot_diagram(orders, truck_paths)
	truck_paths.append([x[0] for x in orders])
	plt.show()
	return truck_paths

def plot_diagram(orders, truck_paths):
	xmin = min([float(order[1]) for order in orders])
	xmax = max([float(order[1]) for order in orders])
	ymin = min([float(order[2]) for order in orders])
	ymax = max([float(order[2]) for order in orders])
	for id in truck_paths:


	plt.plot(x, y, 'o', zorder=10, clip_on=False)
	plt.plot(0, 0, 'o', zorder=10, clip_on=False)


