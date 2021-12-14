import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import copy
import math

from class_network_1 import inf_network

#SN = 'Single Node'单个节点的扩散
#2021.11.18
#MN = 'Multiple Node'多个节点同时扩散
#2021.12.14



#单个节点传播
def MULTI_NETWORK_SPREAD_SN(MULTI_NETWORK, N_LAYERS, inf_index, L_Layer, C_Layer, BETA):

	TIME = 0#设置时间
	for NETWORK in MULTI_NETWORK:
		NETWORK.init()#由于这里是shallow copy,上一次迭代修改的TIME会对当前迭代产生影响,故需要重置
		

	MULTI_NETWORK[L_Layer].network.nodes[inf_index]["INFECTED"] = True
	MULTI_NETWORK[L_Layer].network.nodes[inf_index]["INFECTED_TIME"] = TIME

	INFECTED_LIST = list()
	INFECTED_LIST.append((L_Layer, inf_index))

	Cur_TESTED_UNINFECTED_NODE = [set() for i in range(N_LAYERS)]
	Cur_INFECTED_LIST = set()	

	TIME_LAYER_LIST = []#for statistics
	LAYER_DICT = {}.fromkeys([i for i in range(N_LAYERS)])#for statistics
	for i in range(N_LAYERS):
		LAYER_DICT[i] = list()
	TIME_LAYER_LIST.append(copy.deepcopy(LAYER_DICT))#for statistics

	TIME_LAYER_LIST[TIME][L_Layer].append(inf_index)
	while(len(INFECTED_LIST)):
		Layer, init = INFECTED_LIST.pop(0)
		if TIME == MULTI_NETWORK[Layer].network.nodes[init]['INFECTED_TIME']:
			
			Cur_TESTED_UNINFECTED_NODE = [set() for i in range(N_LAYERS)]#因为可能重复计算，需要将用过的un_node放进这个set()里面
			# for node in Cur_INFECTED_LIST:
			# 	for NETWORK in MULTI_NETWORK:#找到未被感染的那一层
			# 		if NETWORK.network.nodes[node]["INFECTED"] == True:
			# 			continue
			# 		else:
			# 			NETWORK.network.nodes[node]["INFECTED"] = True
			# 			NETWORK.network.nodes[node]["INFECTED_TIME"] = TIME
			# 			INFECTED_LIST.append((NETWORK.layer, node))
						#2021.10.25这个地方需要改掉，因为层与层之间也是独立的了，修改一下，大概就是不用append了，到时候在底下再加一个层关系的感染即可
						# print("Node {} at layer#{} is infected by itself".format(node, NETWORK.layer))

			Cur_INFECTED_LIST = set()
			# print('===========================================')
			# print("TIME is {}".format(TIME))
			TIME += 1
			TIME_LAYER_LIST.append(copy.deepcopy(LAYER_DICT))#for statistics
			
		print("Starting node {0} in layer#{1}".format(init, Layer))
		uninfected_nbr_init = [(Layer, node) for node in nx.neighbors(MULTI_NETWORK[Layer].network, init) \
			if (MULTI_NETWORK[Layer].network.nodes[node]["INFECTED"] == False) and (node not in Cur_TESTED_UNINFECTED_NODE[Layer])]

		#补上层间节点，同一个的	
		layer_nbr_init = [(layer_, init) for layer_ in range(N_LAYERS) \
			if (MULTI_NETWORK[layer_].network.nodes[init]["INFECTED"] == False and (init not in Cur_TESTED_UNINFECTED_NODE[layer_]))]

		uninfected_nbr_init += layer_nbr_init#产生新的未感染邻居

		if len(uninfected_nbr_init) == 0:
			continue
		else:
			for un_node in uninfected_nbr_init:
				Cur_TESTED_UNINFECTED_NODE[un_node[0]].update([un_node[1]])
				Is_Infected = False

				#用所有层的周围节点，综合考虑
				INFECTED_Prb = 1
				#这里也许要改2021.10.26
				
				#从层邻居被感染节点 + 同节点不同层感染节点
				inf_nbr_node = [(un_node[0], node) for node in nx.neighbors(MULTI_NETWORK[un_node[0]].network, un_node[1]) \
				if (MULTI_NETWORK[un_node[0]].network.nodes[node]["INFECTED"] == True and MULTI_NETWORK[un_node[0]].network.nodes[node]["INFECTED_TIME"] == TIME - 1)]\
					+ [(layer_, un_node[1]) for layer_ in range(N_LAYERS) \
					if (MULTI_NETWORK[layer_].network.nodes[un_node[1]]["INFECTED"] == True and MULTI_NETWORK[layer_].network.nodes[un_node[1]]["INFECTED_TIME"] == TIME - 1) and (layer_ != un_node[0])]

				#需要判断是同一层还是不同层
				for layer_,inf_node in inf_nbr_node:
					if layer_ == un_node[0]:
						INFECTED_Prb *= ((1 - BETA)**MULTI_NETWORK[layer_].network.edges[inf_node, un_node[1]]['weight'] )
					else:
						INFECTED_Prb *= math.exp(C_Layer[un_node[0]][layer_])/(1 + math.exp(C_Layer[un_node[0]][layer_]))
				INFECTED_Prb = 1 - INFECTED_Prb
				# print("Probability of NODE {0} is {1}".format(un_node[1], INFECTED_Prb))
				if INFECTED_Prb > random.random():
					Is_Infected = True
				if Is_Infected:
					Cur_INFECTED_LIST.update([un_node])
					TIME_LAYER_LIST[TIME][un_node[0]].append(un_node[1])#for statistics
					MULTI_NETWORK[un_node[0]].network.nodes[un_node[1]]["INFECTED"] = Is_Infected
					MULTI_NETWORK[un_node[0]].network.nodes[un_node[1]]["INFECTED_TIME"] = TIME
					INFECTED_LIST.append((un_node))
					# print("Node{0} in layer#{1} is infected!".format(un_node[1], un_node[0]))
				else:
					continue

	
	infected_NUM = 0
	for Layer_ in range(N_LAYERS):
		for node in MULTI_NETWORK[Layer_].network.nodes:
			if MULTI_NETWORK[Layer_].network.nodes[node]["INFECTED"]:
				infected_NUM += 1

				
	return infected_NUM, TIME, TIME_LAYER_LIST



#多个节点作为初始
def MULTI_NETWORK_SPREAD_MN(MULTI_NETWORK, N_LAYERS, inf_index, L_Layer, C_Layer, BETA):

	TIME = 0#设置时间
	for NETWORK in MULTI_NETWORK:
		NETWORK.init()#由于这里是shallow copy,上一次迭代修改的TIME会对当前迭代产生影响,故需要重置
		
	for Node in inf_index:	
		MULTI_NETWORK[L_Layer].network.nodes[Node]["INFECTED"] = True
		MULTI_NETWORK[L_Layer].network.nodes[Node]["INFECTED_TIME"] = TIME

	INFECTED_LIST = list()
	for Node in inf_index:
		INFECTED_LIST.append((L_Layer, Node))

	Cur_TESTED_UNINFECTED_NODE = [set() for i in range(N_LAYERS)]
	Cur_INFECTED_LIST = set()	

	TIME_LAYER_LIST = []#for statistics
	LAYER_DICT = {}.fromkeys([i for i in range(N_LAYERS)])#for statistics
	for i in range(N_LAYERS):
		LAYER_DICT[i] = list()
	TIME_LAYER_LIST.append(copy.deepcopy(LAYER_DICT))#for statistics

	for Node in inf_index:
		TIME_LAYER_LIST[TIME][L_Layer].append(Node)

	while(len(INFECTED_LIST)):
		Layer, init = INFECTED_LIST.pop(0)
		if TIME == MULTI_NETWORK[Layer].network.nodes[init]['INFECTED_TIME']:
			
			Cur_TESTED_UNINFECTED_NODE = [set() for i in range(N_LAYERS)]#因为可能重复计算，需要将用过的un_node放进这个set()里面
			# for node in Cur_INFECTED_LIST:
			# 	for NETWORK in MULTI_NETWORK:#找到未被感染的那一层
			# 		if NETWORK.network.nodes[node]["INFECTED"] == True:
			# 			continue
			# 		else:
			# 			NETWORK.network.nodes[node]["INFECTED"] = True
			# 			NETWORK.network.nodes[node]["INFECTED_TIME"] = TIME
			# 			INFECTED_LIST.append((NETWORK.layer, node))
						#2021.10.25这个地方需要改掉，因为层与层之间也是独立的了，修改一下，大概就是不用append了，到时候在底下再加一个层关系的感染即可
						# print("Node {} at layer#{} is infected by itself".format(node, NETWORK.layer))

			Cur_INFECTED_LIST = set()
			# print('===========================================')
			# print("TIME is {}".format(TIME))
			TIME += 1
			TIME_LAYER_LIST.append(copy.deepcopy(LAYER_DICT))#for statistics
			
		print("Starting node {0} in layer#{1}".format(init, Layer))
		uninfected_nbr_init = [(Layer, node) for node in nx.neighbors(MULTI_NETWORK[Layer].network, init) \
			if (MULTI_NETWORK[Layer].network.nodes[node]["INFECTED"] == False) and (node not in Cur_TESTED_UNINFECTED_NODE[Layer])]

		#补上层间节点，同一个的	
		layer_nbr_init = [(layer_, init) for layer_ in range(N_LAYERS) \
			if (MULTI_NETWORK[layer_].network.nodes[init]["INFECTED"] == False and (init not in Cur_TESTED_UNINFECTED_NODE[layer_]))]

		uninfected_nbr_init += layer_nbr_init#产生新的未感染邻居

		if len(uninfected_nbr_init) == 0:
			continue
		else:
			for un_node in uninfected_nbr_init:
				Cur_TESTED_UNINFECTED_NODE[un_node[0]].update([un_node[1]])
				Is_Infected = False

				#用所有层的周围节点，综合考虑
				INFECTED_Prb = 1
				#这里也许要改2021.10.26
				
				#从层邻居被感染节点 + 同节点不同层感染节点
				inf_nbr_node = [(un_node[0], node) for node in nx.neighbors(MULTI_NETWORK[un_node[0]].network, un_node[1]) \
				if (MULTI_NETWORK[un_node[0]].network.nodes[node]["INFECTED"] == True and MULTI_NETWORK[un_node[0]].network.nodes[node]["INFECTED_TIME"] == TIME - 1)]\
					+ [(layer_, un_node[1]) for layer_ in range(N_LAYERS) \
					if (MULTI_NETWORK[layer_].network.nodes[un_node[1]]["INFECTED"] == True and MULTI_NETWORK[layer_].network.nodes[un_node[1]]["INFECTED_TIME"] == TIME - 1) and (layer_ != un_node[0])]

				#需要判断是同一层还是不同层
				for layer_,inf_node in inf_nbr_node:
					if layer_ == un_node[0]:
						INFECTED_Prb *= ((1 - BETA)**MULTI_NETWORK[layer_].network.edges[inf_node, un_node[1]]['weight'] )
					else:
						INFECTED_Prb *= math.exp(C_Layer[un_node[0]][layer_])/(1 + math.exp(C_Layer[un_node[0]][layer_]))
				INFECTED_Prb = 1 - INFECTED_Prb
				# print("Probability of NODE {0} is {1}".format(un_node[1], INFECTED_Prb))
				if INFECTED_Prb > random.random():
					Is_Infected = True
				if Is_Infected:
					Cur_INFECTED_LIST.update([un_node])
					TIME_LAYER_LIST[TIME][un_node[0]].append(un_node[1])#for statistics
					MULTI_NETWORK[un_node[0]].network.nodes[un_node[1]]["INFECTED"] = Is_Infected
					MULTI_NETWORK[un_node[0]].network.nodes[un_node[1]]["INFECTED_TIME"] = TIME
					INFECTED_LIST.append((un_node))
					# print("Node{0} in layer#{1} is infected!".format(un_node[1], un_node[0]))
				else:
					continue

	
	infected_NUM = 0
	for Layer_ in range(N_LAYERS):
		for node in MULTI_NETWORK[Layer_].network.nodes:
			if MULTI_NETWORK[Layer_].network.nodes[node]["INFECTED"]:
				infected_NUM += 1

				
	return infected_NUM, TIME, TIME_LAYER_LIST
