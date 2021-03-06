#根据要求返回节点以及所在层

#Node_Sel_Betw用复杂的方法
#Node_Sel_Neib则是用邻居个数计算
#R_LAYER_R_NODE 随机层，随机节点
#R_LAYER_Degr_NODE 随机层，根据度选取节点
#R_LAYER_Neigh_NODE 随机层， 根据邻居数选取节点



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


def Output_Betw(MULTI_NETWORK, N_LAYERS, N_NODES, wei_dis_dict):
	#输出每一层的betweeness的值
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

	return Layer_betweeness

def Output_Neigh(MULTI_NETWORK, N_LAYERS, N_NODES, RADIUS):
	#输出每一层neighborhood的值
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

	return Layer_betweeness	



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

	return (Max_Node, Max_Layer)


def R_LAYER_R_NODE(N_LAYERS, N_NODES):
	return (random.randint(0, N_NODES - 1), random.randint(0, N_LAYERS - 1))

def R_LAYER_Degr_NODE(MULTI_NETWORK, N_LAYERS, N_NODES):
	CHOSEN_LAYER = random.randint(0, N_LAYERS - 1)

	EDGE_LIST = [0] * N_NODES
	for NETWORK in MULTI_NETWORK:
		for node, nbrs in NETWORK.network.adj.items():
			EDGE_LIST[node] += len(list(nbrs))

	MAX_NODE_INDEX = 0
	MAX_Val = 0
	#找有最大度的节点
	for i in range(N_NODES):
		if EDGE_LIST[i] >= EDGE_LIST[MAX_NODE_INDEX]:
			MAX_NODE_INDEX = i
			MAX_Val = EDGE_LIST[i]
		else:
			continue
	return (MAX_NODE_INDEX, CHOSEN_LAYER)		

def R_LAYER_Neigh_NODE(MULTI_NETWORK, N_LAYERS, N_NODES):
	CHOSEN_LAYER = random.randint(0, N_LAYERS - 1)


	NODE_NBRS = [set() for i in range(N_NODES)]
	N_N = []
	for NETWORK in MULTI_NETWORK:
		for node, nbrs in NETWORK.network.adj.items():
			NODE_NBRS[node] = (NODE_NBRS[node] | set(nbrs))	
	N_N = [len(NODE_NBRS[i]) for i in range(len(NODE_NBRS))]


	MAX_NODE_INDEX = 0
	MAX_Val = 0
	#找有最大邻居数的节点
	for i in range(N_NODES):
		if N_N[i] >= N_N[MAX_NODE_INDEX]:
			MAX_NODE_INDEX = i
			MAX_Val = N_N[i]
		else:
			continue
	return (MAX_NODE_INDEX, CHOSEN_LAYER)	

def Betw_LAYER_R_NODE(MULTI_NETWORK, N_LAYERS, N_NODES, wei_dis_dict, RADIUS):
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

	Max_Node = random.randint(0, N_LAYERS - 1)

	return (Max_Node, Max_Layer)

def Betw_LAYER_Degr_NODE(MULTI_NETWORK, N_LAYERS, N_NODES, wei_dis_dict, RADIUS):
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

	EDGE_LIST = [0] * N_NODES
	for NETWORK in MULTI_NETWORK:
		for node, nbrs in NETWORK.network.adj.items():
			EDGE_LIST[node] += len(list(nbrs))

	MAX_NODE_INDEX = 0
	MAX_Val = 0
	#找有最大度的节点
	for i in range(N_NODES):
		if EDGE_LIST[i] >= EDGE_LIST[MAX_NODE_INDEX]:
			MAX_NODE_INDEX = i
			MAX_Val = EDGE_LIST[i]
		else:
			continue

	return (MAX_NODE_INDEX, Max_Layer)		

def Betw_LAYER_Neigh_NODE(MULTI_NETWORK, N_LAYERS, N_NODES, wei_dis_dict, RADIUS):
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

	NODE_NBRS = [set() for i in range(N_NODES)]
	N_N = []
	for NETWORK in MULTI_NETWORK:
		for node, nbrs in NETWORK.network.adj.items():
			NODE_NBRS[node] = (NODE_NBRS[node] | set(nbrs))	
	N_N = [len(NODE_NBRS[i]) for i in range(len(NODE_NBRS))]


	MAX_NODE_INDEX = 0
	MAX_Val = 0
	#找有最大邻居数的节点
	for i in range(N_NODES):
		if N_N[i] >= N_N[MAX_NODE_INDEX]:
			MAX_NODE_INDEX = i
			MAX_Val = N_N[i]
		else:
			continue		

	return (MAX_NODE_INDEX, Max_Layer)		


def Neib_LAYER_R_NODE(MULTI_NETWORK, N_LAYERS, N_NODES, wei_dis_dict, RADIUS):
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

	Max_Node = random.randint(0, N_LAYERS - 1)

	return (Max_Node, Max_Layer)


def Neib_LAYER_Degr_NODE(MULTI_NETWORK, N_LAYERS, N_NODES, wei_dis_dict, RADIUS):
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

	EDGE_LIST = [0] * N_NODES
	for NETWORK in MULTI_NETWORK:
		for node, nbrs in NETWORK.network.adj.items():
			EDGE_LIST[node] += len(list(nbrs))

	MAX_NODE_INDEX = 0
	MAX_Val = 0
	#找有最大度的节点
	for i in range(N_NODES):
		if EDGE_LIST[i] >= EDGE_LIST[MAX_NODE_INDEX]:
			MAX_NODE_INDEX = i
			MAX_Val = EDGE_LIST[i]
		else:
			continue

	return (MAX_NODE_INDEX, Max_Layer)		
	

def Neib_LAYER_Neigh_NODE(MULTI_NETWORK, N_LAYERS, N_NODES, wei_dis_dict, RADIUS):
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

	NODE_NBRS = [set() for i in range(N_NODES)]
	N_N = []
	for NETWORK in MULTI_NETWORK:
		for node, nbrs in NETWORK.network.adj.items():
			NODE_NBRS[node] = (NODE_NBRS[node] | set(nbrs))	
	N_N = [len(NODE_NBRS[i]) for i in range(len(NODE_NBRS))]


	MAX_NODE_INDEX = 0
	MAX_Val = 0
	#找有最大邻居数的节点
	for i in range(N_NODES):
		if N_N[i] >= N_N[MAX_NODE_INDEX]:
			MAX_NODE_INDEX = i
			MAX_Val = N_N[i]
		else:
			continue		

	return (MAX_NODE_INDEX, Max_Layer)		



#Pick Layer
def Betw_Layer(MULTI_NETWORK, N_NODES, N_LAYERS, wei_dis_dict):

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

	return Max_Layer

def R_Layer(N_LAYERS):
	CHOSEN_LAYER = random.randint(0, N_LAYERS - 1)
	return CHOSEN_LAYER

def Nei_Layer(MULTI_NETWORK, N_LAYERS, N_NODES, wei_dis_dict, RADIUS):

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

	return Max_Layer


#Pick Node

#随机
def R_Node(N_NODES, Top = 1):
	Random_List = [i for i in range(N_NODES)]
	return random.sample(Random_List, Top)



#邻居数
def Neigh_Node(MULTI_NETWORK, N_LAYERS, N_NODES, Top = 1):
	#选取排名的前Top个节点
	NODE_NBRS = [set() for i in range(N_NODES)]
	N_N = []
	for NETWORK in MULTI_NETWORK:
		for node, nbrs in NETWORK.network.adj.items():
			NODE_NBRS[node] = (NODE_NBRS[node] | set(nbrs))	
	N_N = [len(NODE_NBRS[i]) for i in range(len(NODE_NBRS))]

	NODE_DATA_LIST = [(i, N_N[i]) for i in range(N_NODES)]#建立一个节点编号和其数值对应的list
	NODE_DATA_LIST.sort(key = lambda x: x[1], reverse = True)#根据N_N排序，由大到小，其实也没多大必要，只要Top，如果慢的话就改一下吧，数量不多的话O(n)即可

	Rank_List = []
	for pick in range(Top):
		Rank_List.append(NODE_DATA_LIST[pick][0])#append编号

	return Rank_List
	


#度
def Degr_Node(MULTI_NETWORK, N_LAYERS, N_NODES, Top = 1):
	#选取排名的前Top个节点
	EDGE_LIST = [0] * N_NODES
	for NETWORK in MULTI_NETWORK:
		for node, nbrs in NETWORK.network.adj.items():
			EDGE_LIST[node] += len(list(nbrs))


	NODE_DATA_LIST = [(i, EDGE_LIST[i]) for i in range(N_NODES)]#建立一个节点编号和其数值对应的list
	NODE_DATA_LIST.sort(key = lambda x: x[1], reverse = True)#根据N_N排序，由大到小，其实也没多大必要，只要Top，如果慢的话就改一下吧，数量不多的话O(n)即可

	Rank_List = []
	for pick in range(Top):
		Rank_List.append(NODE_DATA_LIST[pick][0])#append编号

	return Rank_List

#引力模型
def Gravity_Node(MULTI_NETWORK, wei_dis_dict, Pick_Layer, N_LAYERS, N_NODES, RADIUS, Top = 1):
	#选取排名的前Top个节点
	Max_Node_L_Star = [0 for i in range(N_NODES)]
	for node in range(N_NODES):
		K_L_Node = len(list(nx.all_neighbors(MULTI_NETWORK[Pick_Layer].network, node)))
		for layer in range(N_LAYERS):
			#注意R_List里面是会包含本身的节点，需要删掉
			R_List = list(nx.bfs_tree(MULTI_NETWORK[layer].network, source = node, depth_limit = RADIUS))
			R_List.remove(node)
			# print(R_List)
			for R_Node in R_List:
				D_R = wei_dis_dict[(node, R_Node + layer * N_NODES)]['Wei']/wei_dis_dict[(node, R_Node + layer * N_NODES)]['Length']
				Max_Node_L_Star[node] += K_L_Node * len(list(nx.all_neighbors(MULTI_NETWORK[layer].network, node)))/ D_R

	Max_Node = Max_Node_L_Star.index(max(Max_Node_L_Star))

	NODE_DATA_LIST = [(i, Max_Node_L_Star[i]) for i in range(N_NODES)]#建立一个节点编号和其数值对应的list
	NODE_DATA_LIST.sort(key = lambda x: x[1], reverse = True)#根据N_N排序，由大到小，其实也没多大必要，只要Top，如果慢的话就改一下吧，数量不多的话O(n)即可

	Rank_List = []
	for pick in range(Top):
		Rank_List.append(NODE_DATA_LIST[pick][0])#append编号

	return Rank_List	


