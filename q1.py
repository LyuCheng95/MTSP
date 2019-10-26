import random
import math
import numpy as np
import matplotlib.pyplot as plt
# <Your Team ID>
# <Team members' names>

# replace the content of this function with your own algorithm


def schedule_q1(orders, number_trucks):
    order_dict = list_to_dict(orders)
    order_dict['O'] = [0, 0]
    distances = []
    sections = [[] for i in range(number_trucks)]
    edges_lists = []

    # divide orders by angle
    for order in orders:
        bearing = calculate_bearing((float(order[1]), float(order[2])))
        radian_gap = 2 * math.pi / number_trucks
        nth_division = int(math.ceil(bearing / radian_gap) - 1)
        sections[nth_division].append(order[0])

    for nodes in sections:
        nodes.insert(0, 'O')
        nodes.append('O')
        edges = compute_edges(nodes, order_dict)
        total_dist = 99999
        while True:
            new_total_dist = clear_crosses(nodes, edges, order_dict)
            if new_total_dist < total_dist:
                total_dist = new_total_dist
            elif total_dist == new_total_dist:
                break
        edges_lists.append(edges)
        distances.append(sum(edges))
        # nodes.pop(0)
        # nodes.pop()

    # optmization
    trucks = {i:[sections[i], edges_lists[i], distances[i], i] for i in range(len(sections))}
    busiest_truck = max(trucks.values(), key=lambda x: x[2])
    random_node = random.choice(busiest_truck[0])




    # ending up
    for nodes in sections:
        nodes.pop(0)
        nodes.pop()
    # print(distances)
    # print(sections)
    plot_diagram(order_dict, sections)

    return sections


def clear_crosses(nodes, edges, order_dict):
    for i in range(len(nodes)):
        for j in range(i+2, len(nodes)-1):
            alt_path_1 = calculate_distance(
                order_dict[nodes[i]], order_dict[nodes[j]])
            alt_path_2 = calculate_distance(
                order_dict[nodes[i+1]], order_dict[nodes[j+1]])
            alternative_path = alt_path_1 + alt_path_2
            if alternative_path < (edges[i] + edges[j]):
                nodes[i+1:j+1] = nodes[i+1:j+1][::-1]
                edges[i] = alt_path_1
                edges[j] = alt_path_2
                edges[i+1:j] = edges[i+1:j][::-1]
    return sum(edges)


def calculate_bearing(position):
    lat = math.radians(position[0])
    lon = math.radians(position[1])
    x = math.sin(lon)
    y = -1 * math.sin(lat) * math.cos(lon)
    bearing = math.atan2(x, y) + math.pi
    return bearing


def calculate_distance(start, end):
    return ((start[0]-end[0])**2 + (start[1]-end[1])**2)**0.5


def compute_edges(nodes, order_dict):
    edges = []
    for i, order_id in enumerate(nodes):
        if not i == (len(nodes) - 1):
            edges.append(calculate_distance(
                order_dict[order_id], order_dict[nodes[i+1]]))
    return edges

def plot_diagram(order_dict, truck_paths):
    truck_colors = [[random.uniform(0, 1)
                     for i in range(3)] for j in range(25)]
    for i, id_list in enumerate(truck_paths):
        plot_list = ['O']
        plot_list.extend(id_list)
        plot_list.append('O')
        color = truck_colors[i]
        for j in range(len(plot_list)-1):
            p1 = [float(order_dict[plot_list[j]][0]), float(order_dict[plot_list[j+1]][0])]
            p2 = [float(order_dict[plot_list[j]][1]), float(order_dict[plot_list[j+1]][1])]
            # plt.plot(p1[0], p1[1], 'o', color=color)
            # plt.plot(p2[0], p2[1], 'o', color=color)
            plt.plot(p1, p2, 'ro-', color=color)
    plt.plot(0, 0, 'o', zorder=10, clip_on=False)
    plt.show()

def list_to_dict(lst):
    info_dict = {}
    for item in lst:
        info_dict[item[0]] = [float(item[1]), float(item[2])]
    return info_dict
