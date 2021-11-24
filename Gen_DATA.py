# coding=utf-8
#OUPUT:
# - 每一层网络（计算好权重）
# - 层间的权重
# - 压缩网络（计算好权重）
# - 节点之间的权重距离字典


import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import copy
import numpy as np
import time
import pickle
import os

from class_network_1 import inf_network
from Document_Save import Document_Save#保存




# from FUN_MULTI_NETWORK_SPREAD import MULTI_NETWORK_SPREAD #MULTI_NETWORK_SPREAD(MULTI_NETWORK, N_LAYERS, inf_index, BETA)
# from FUN_CAL_INFLUENCE import CAL_INFLUENCE #CAL_INFLUENCE(MULTI_NETWORK, N_NODES, N_EDGES, N_LAYERS, RADIUS)
# from FUN_CAL_EDGE import CAL_EDGE #CAL_EDGE(MULTI_NETWORK, N_NODES, N_EDGES, N_LAYERS)
# from FUN_RANK import RANK #RANK(N_NODES, data)

#更改path可以改变生成网络的目录,请在源文件的目录下先新建文件夹(假设是doc_name).
#然后此时path = './doc_name/'
#detail.txt包含网络的节点数,边的数量(和随机生成的网络有关), 网络层数的信息
#x.nt则记录每一层节点的不同节点间的权重
# def GENERATE_MUL_NETWORK(N_NODES, N_EDGES, N_LAYERS, path):
# 	read = open(path + 'detail.txt', 'w')
# 	read.write("#NODES #EDGES #LAYERS" + '\n')
# 	read.write("{0:^5d} {1:^5d} {2:^5d}".format(N_NODES, N_EDGES, N_LAYERS) + '\n')
# 	read.close()
	
# 	MULTI_NETWORK = list()
# 	ori_network = inf_network(N_NODES, N_EDGES)
# 	MULTI_NETWORK.append(ori_network)
# 	for i in range(N_LAYERS - 1):
# 		#两种方法
# 		#1 新生成节点数量相同，边不同的网络
# 		MULTI_NETWORK.append(inf_network(N_NODES, N_EDGES))
# 		#2 生成和初始网络数量相同，边相同，只有权重不同的网络
# 		# MULTI_NETWORK.append(copy.deepcopy(ori_network).change_weight())
# 	for i in range(N_LAYERS):
# 		MULTI_NETWORK[i].layer = i

# 	for NETWORK in MULTI_NETWORK:	
# 		read = open(path + '{}.nt'.format(NETWORK.layer), 'wb')
# 		nx.write_multiline_adjlist(NETWORK.network, read, delimiter = ',')
# 		read.close()

# 	return True






'''
	NT_DICT_2 = {'1': {'name':nx.barabasi_albert_graph, 'arg':{'n':100, 'm':5}}, 
	'2': {'name':nx.watts_strogatz_graph, 'arg':{'n':100, 'k':10, 'p':0.5}},
	'3': {'name':nx.binomial_graph, 'arg':{'n':100, 'p':0.1}}}

	RANDOM_DICT_2 = {'1': {'fun':random.uniform, 'arg':{'a':0, 'b':1}}, 
	'2': {'fun':random.random, 'arg':{'a':0}},
	'3': {'fun':random_gen, 'arg':{'mu':0, 'sigma':1}}}					
	
	NT_DICT_FINAL = {'1': {'name':nx.barabasi_albert_graph, 'arg':{'n':1000, 'm':5}}, 
	'2': {'name':nx.watts_strogatz_graph, 'arg':{'n':1000, 'k':10, 'p':0.1}},
	'3': {'name':nx.binomial_graph, 'arg':{'n':1000, 'p':0.1}}}

	S500 = {'1': {'name':nx.barabasi_albert_graph, 'arg':{'n':500, 'm':7}}}	

	NT_SMAL = {'1': {'name':nx.barabasi_albert_graph, 'arg':{'n':10, 'm':3}}}
	RANDOM_DICT_SMAL = {'1': {'fun':random.random, 'arg':{'a':0}}}	

	# N_NODES = 100#设置节点数
	# N_EDGES = 5#设置每个节点的连边数
	N_LAYERS = 3

	NT_LW_FINAL = {'1': {'name':nx.watts_strogatz_graph, 'arg':{'n':1000, 'k':10, 'p':0.1}}, 
	'2': {'name':nx.watts_strogatz_graph, 'arg':{'n':1000, 'k':10, 'p':0.1}},
	'3': {'name':nx.watts_strogatz_graph, 'arg':{'n':1000, 'k':10, 'p':0.1}},
	'4': {'name':nx.watts_strogatz_graph, 'arg':{'n':1000, 'k':10, 'p':0.1}},
	'5': {'name':nx.watts_strogatz_graph, 'arg':{'n':1000, 'k':10, 'p':0.1}}}

	RANDOM_DICT_LW = {'1': {'fun':random.random, 'arg':{'a':0}}, 
	'2': {'fun':random.random, 'arg':{'a':0}},
	'3': {'fun':random.random, 'arg':{'a':0}},
	'4': {'fun':random.random, 'arg':{'a':0}},
	'5': {'fun':random.random, 'arg':{'a':0}}}

	RANDOM_DICT_UNIFORM = {'1': {'fun':random.uniform, 'arg':{'a':0, 'b':0.5}}, 
	'2': {'fun':random.uniform, 'arg':{'a':0.25, 'b':0.75}},
	'3': {'fun':random.uniform, 'arg':{'a':0.5, 'b':1.0}}}
'''


def test_NT_weight(MULTI_NETWORK, N_NODES, N_LAYERS):
	for layer in range(N_LAYERS):
		print("Now in Layer No.{}:".format(layer))
		for edge in MULTI_NETWORK[layer].network.edges:
			print("The weight of edge ({},{}) is {}".format(edge[0], edge[1], MULTI_NETWORK[layer].network.edges[edge]['weight']))
		print('===============================================')	

def test_layer_weight(Layer_weight, N_LAYERS):
	for layer in range(N_LAYERS):
		for next_layer in range(layer, N_LAYERS):
			print("The weight betweent No.{} and No.{} is :{}".format(layer, next_layer, Layer_weight[layer][next_layer]))


def idx_decode(node_index, N_LAYERS, N_NODES):
	return (node_index / N_NODES, node_index % N_NODES) #(layer, index)

def max_path(path_list):
	pass
	#path_list = (path, weight)



def GENERATE_MUL_NETWORK(NETWORK_DICT, N_LAYERS):
	
	#不需要传入权重参数了.
	
	

	MULTI_NETWORK = list()
	for value in NETWORK_DICT.values():
		MULTI_NETWORK.append(inf_network(False, None, value['name'], **value['arg']))


	for i in range(N_LAYERS):
		MULTI_NETWORK[i].layer = i

	#计算权重	
	# for i in range(N_LAYERS):
	# 	MULTI_NETWORK[i].change_weight(RANDOM_DICT[str(i + 1)]['fun'], **RANDOM_DICT[str(i + 1)]['arg'])
	for layer in range(N_LAYERS):
		for edge in MULTI_NETWORK[layer].network.edges():
			s_vertex = edge[0]
			e_vertex = edge[1]
			common_nbh = set(nx.common_neighbors(MULTI_NETWORK[layer].network, s_vertex, e_vertex))
			
			nbh_s = set(nx.neighbors(MULTI_NETWORK[layer].network, s_vertex))
			nbh_e = set(nx.neighbors(MULTI_NETWORK[layer].network, e_vertex))
			all_nbh = nbh_s | nbh_e
			MULTI_NETWORK[layer].network.edges[edge]['weight'] = (len(common_nbh) + 1)/ len(all_nbh)

	# for NETWORK in MULTI_NETWORK:	
	# 	read = open(path + '{}.nt'.format(NETWORK.layer), 'wb')
	# 	nx.write_multiline_adjlist(NETWORK.network, read, delimiter = ',')
	# 	read.close()

	# read = open(path + 'detail.txt', 'w')
	# read.write("#NODES #LAYERS" + '\n')
	# read.write("{0:^5d} {1:^5d}".format(MULTI_NETWORK[0].num_nodes, N_LAYERS) + '\n')
	# read.close()

	return MULTI_NETWORK

def Layer_Weight_R(MULTI_NETWORK, N_LAYERS, Is_Fix = True, Given = 0.1):
	#R是随机生成
	#Is_Fix表示层间权重是全随机，还是用后面给定的列表全部相等
	wei_layer_R = [[None for i in range(N_LAYERS)] for j in range(N_LAYERS)]
	if not Is_Fix:
		for i in range(N_LAYERS):
			for j in range(i, N_LAYERS):
				if j == i:
					continue
				else:
					wei_layer_R[i][j] = random.random()
					wei_layer_R[j][i] = wei_layer_R[i][j]
	else:
		#用给定参数给每一层赋值
		for i in range(N_LAYERS):
			for j in range(i, N_LAYERS):
				if j == i:
					continue
				else:
					wei_layer_R[i][j] = Given
					wei_layer_R[j][i] = Given

	return wei_layer_R

def Layer_Weight_K(MULTI_NETWORK, N_LAYERS):
	#K是利用kernel计算
	#怎么算
	wei_layer_K = [[None for i in range(N_LAYERS)] for j in range(N_LAYERS)]
	pass

	return wei_layer_K

def Combine_NetW(MULTI_NETWORK, N_LAYERS, N_NODES, Layer_Weight):
	#合并多层网络，根据层间权重列表添加权重
	Fake_Mul_Ntw = copy.deepcopy(MULTI_NETWORK[0].network)
	for layer in range(1, N_LAYERS):
		Fake_Mul_Ntw.add_nodes_from(range(layer * N_NODES, (layer + 1) * N_NODES))

	#其它层的边和权重补全
	for layer in range(1, N_LAYERS):
		e = [(edge[0] + layer * N_NODES, edge[1] + layer * N_NODES, {'weight': MULTI_NETWORK[layer].network.edges[edge]['weight']}) for edge in MULTI_NETWORK[layer].network.edges()]
		Fake_Mul_Ntw.add_edges_from(e)

	#层与层之间的权重补全
	for layer in range(N_LAYERS):
		for next_layer in range(layer +1, N_LAYERS):
			e = [(node + layer * N_NODES, node + next_layer * N_NODES, {'weight': Layer_Weight[layer][next_layer]}) for node in range(N_NODES)]
			Fake_Mul_Ntw.add_edges_from(e)	

	return Fake_Mul_Ntw

def Weight_Dist_Path(Combine_Ntw, N_LAYERS, N_NODES):
	#保存两个节点之间物理最短路以及权重和最短路
	wei_dis_dict = {(u, v):{'Length': None, 'Wei': None, 'Path': None} for u in range(N_LAYERS * N_NODES) for v in range(N_LAYERS * N_NODES)}

	for u in range(N_LAYERS * N_NODES):
		for v in range(u + 1, N_LAYERS * N_NODES):
			wei_dis_dict[(u, v)]['Length'] = len(nx.shortest_path(Combine_Ntw, u, v)) - 1
			# path_wei_list = [(p, nx.path_weight(Fake_Mul_Ntw, p, 'weight')) for p in nx.all_shortest_paths(Fake_Mul_Ntw, source = u, target = v)]
			#用于构建path和对应weight的dict表，方便找到最大权重的同时把映射的路径找到（暂时, key = weight, value = path
			wei_path_dict = {nx.path_weight(Combine_Ntw, p, 'weight'): p for p in nx.all_shortest_paths(Combine_Ntw, source = u, target = v)}
			max_key_wei = max(wei_path_dict.keys())#权重最大的值
			wei_dis_dict[(u, v)]['Wei'] = max_key_wei
			wei_dis_dict[(u, v)]['Path'] = wei_path_dict[max_key_wei]#权重最大值作为key，返回的path

			wei_dis_dict[(v, u)]['Length'] = wei_dis_dict[(u, v)]['Length']
			wei_dis_dict[(v, u)]['Wei'] = wei_dis_dict[(u, v)]['Wei']
			wei_dis_dict[(v, u)]['Path'] = wei_dis_dict[(u, v)]['Path']

	end = time.process_time()
	return wei_dis_dict	


def Dict_Write(Dict, Path, Name):
	#就这么简单吗？
	f = open(Path + Name + '.pkl', 'w')
	pickle.dump(Dict, f)
	f.close()






if __name__ == '__main__':

	def random_gen(mu = 0,sigma = 1):
		#生成符合分布的随机数
		val = random.gauss(mu, sigma)
		while( val <= 0 or val > 1):
			val = random.gauss(mu, sigma)
		return val


	NT_DICT = {'1': {'name':nx.barabasi_albert_graph, 'arg':{'n':100, 'm':5}}, 
	'2': {'name':nx.watts_strogatz_graph, 'arg':{'n':100, 'k':10, 'p':0.5}},
	'3': {'name':nx.barabasi_albert_graph, 'arg':{'n':100, 'm':7}}}



	DOCUMENT_NAME = "SMALL_50" #根据网络结构自行定义，建议带上节点数，网络类型

	N_LAYERS = 3

	N_NODES = 100




	ROOT_NAME = os.getcwd()

	GIVEN_NAME = '_Given_'

	KERNEL_NAME = '_Kenel'

	RANDOM_NAME = '_Random'


	Given_Dict = [i/10 for i in range(1, 10, 1)]

	print("Now generate multi network...")
	MULTI_NETWORK = GENERATE_MUL_NETWORK(NT_DICT, N_LAYERS)
	print("Generating Done.")

	for NETWORK in MULTI_NETWORK:	
		read_nt = open(ROOT_NAME + '/' + '{}.nt'.format(NETWORK.layer), 'wb')
		nx.write_multiline_adjlist(NETWORK.network, read_nt, delimiter = ',')
		read_nt.close()	

	read = open(ROOT_NAME + '/' + 'detail.txt', 'w')
	read.write("#NODES #LAYERS" + '\n')
	read.write("{0:^5d} {1:^5d}".format(MULTI_NETWORK[0].num_nodes, N_LAYERS) + '\n')
	read.close()


	#{'0.1': 对应了一个列表}，到时候直接用.items()就可以直接遍历，然后一个个保存了
	Combine_Ntw_Given_Dict = {str(Given) : Layer_Weight_R(MULTI_NETWORK, N_LAYERS, True, Given) for Given in Given_Dict}
	#一个循环全部保存

	#Given save:
	print("Now Saving the multi-network that the weight between respective network is given...")
	for Given_Val, Layer_Wei in Combine_Ntw_Given_Dict.items():
		print("The given value now saving is :{}..".format(Given_Val))
		Combine_NT = Combine_NetW(MULTI_NETWORK, N_LAYERS, N_NODES, Layer_Wei)
		# Wei_Dis_Dict = Weight_Dist_Path(Combine_NT, N_LAYERS, N_NODES)

		start_wei = time.process_time()
		SP_Dic = Weight_Dist_Path(Combine_NT, N_LAYERS, N_NODES)
		end_wei = time.process_time()
		print("Time of calculation weight and shortest_path is: {}".format(end_wei - start_wei))

		start_save = time.process_time()
		Document_Save(ROOT_NAME, DOCUMENT_NAME + GIVEN_NAME + Given_Val, Layer_Wei, Combine_NT, SP_Dic)
		end_save = time.process_time()
		print("Time of domument saving is :{}".format(end_save - start_save))
		print("Done...")



	print("Now Saving the multi-network that the weight between respective network is random...")
	Combine_Ntw_Random = Combine_NetW(MULTI_NETWORK, N_LAYERS, N_NODES, Layer_Weight_R(MULTI_NETWORK, N_LAYERS, False, 0))
	Document_Save(ROOT_NAME, DOCUMENT_NAME + RANDOM_NAME, Layer_Wei, Combine_NT, SP_Dic)
	print("Done...")


	# Combine_Ntw_Kernel = None#持续难产中

	#不模块了


	



