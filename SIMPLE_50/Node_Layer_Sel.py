#根据要求返回节点以及所在层

#Node_Sel_Betw用复杂的方法
#Node_Sel_Neib则是用邻居个数计算
#方法自选
import time
import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import copy
import numpy as np
import time
import pickle
import os

def Node_Sel_Betw(MULTI_NETWORK, N_LAYERS, N_NODES, wei_dis_dict, RADIUS):


	All_Node_List = [0 for i in range(N_LAYERS * N_NODES)]#建立一个list存放介数中心性

		#对半遍历的话应该可以减少很多判断in的时间
	for node in range(N_LAYERS * N_NODES):
		for link, para in wei_dis_dict.items():
			if link[0] == link[1]:
				continue
			else:
				Path = para['Path'][1 : -1]
				if node in Path:
					All_Node_List[node] += 1
				else:
						continue

	All_Node_Betweeness = [node/((N_LAYERS * N_NODES) * (N_LAYERS * N_NODES - 1)) for node in All_Node_List]
	Layer_betweeness = [None for i in range(N_LAYERS)]
	for layer in range(N_LAYERS):
		Layer_betweeness[layer] = sum(All_Node_Betweeness[layer * N_NODES : (layer + 1) * N_NODES])

	Max_Layer = Layer_betweeness.index(max(Layer_betweeness))

	# print(Layer_betweeness)
	Max_Node_L_Star = [0 for i in range(N_NODES)]
	for node in range(N_NODES):
		K_L_Node = len(list(nx.all_neighbors(MULTI_NETWORK[Max_Layer].network, node)))
		for layer in range(N_LAYERS):
			#注意R_List里面是会包含本身的节点，需要删掉
			R_List = list(nx.bfs_tree(MULTI_NETWORK[layer].network, source = node, depth_limit = RADIUS))
			R_List.remove(node)
			# print(R_List)
			for R_Node in R_List:
				D_R = wei_dis_dict[(node, R_Node + layer * N_NODES)]['Wei']/wei_dis_dict[(node, R_Node + layer * N_NODES)]['Length']
				Max_Node_L_Star[node] += K_L_Node * len(list(nx.all_neighbors(MULTI_NETWORK[layer].network, node)))/ D_R

	Max_Node = Max_Node_L_Star.index(max(Max_Node_L_Star))

	return (Max_Node, Max_Layer)

def Node_Sel_Neib(MULTI_NETWORK, N_LAYERS, N_NODES, wei_dis_dict, RADIUS):


	#另一种计算layer betweeness的方法，先做一个表
	Layer_betweeness_dict = {u: [0 for i in range(N_NODES)] for u in range(N_LAYERS)}
	# for layer in range(N_LAYERS):
	# 	for node in range(N_NODES):

	# 		Layer_betweeness_dict[layer][node] = len(nx.bfs_tree(MULTI_NETWORK[layer].network, source = node, depth_limit = RADIUS)) - 1#减去root

	for Node in range(N_NODES):
		for Layer in range(N_LAYERS):
			for Next_Layer in range(N_LAYERS):
				if Next_Layer == Layer:
					Layer_betweeness_dict[Layer][Node] += len(nx.bfs_tree(MULTI_NETWORK[Next_Layer].network, source = Node, depth_limit = RADIUS)) - 1
				else:
					Layer_betweeness_dict[Layer][Node] += len(nx.bfs_tree(MULTI_NETWORK[Next_Layer].network, source = Node, depth_limit = RADIUS - 1)) - 1


	Layer_betweeness = [0 for i in range(N_LAYERS)]
	for layer in range(N_LAYERS):
		Layer_betweeness[layer] = sum(Layer_betweeness_dict[layer])

	#懒得写argmin了，先随便设定一个


	Max_Layer = Layer_betweeness.index(max(Layer_betweeness))


	Max_Node_L_Star = [0 for i in range(N_NODES)]
	for node in range(N_NODES):
		K_L_Node = len(list(nx.all_neighbors(MULTI_NETWORK[Max_Layer].network, node)))
		for layer in range(N_LAYERS):
			#注意R_List里面是会包含本身的节点，需要删掉
			R_List = list(nx.bfs_tree(MULTI_NETWORK[layer].network, source = node, depth_limit = RADIUS))
			R_List.remove(node)
			# print(R_List)
			for R_Node in R_List:
				D_R = wei_dis_dict[(node, R_Node + layer * N_NODES)]['Wei']/wei_dis_dict[(node, R_Node + layer * N_NODES)]['Length']
				Max_Node_L_Star[node] += K_L_Node * len(list(nx.all_neighbors(MULTI_NETWORK[layer].network, node)))/ D_R

	Max_Node = Max_Node_L_Star.index(max(Max_Node_L_Star))