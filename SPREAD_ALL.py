#READ_DATA
#读取每一个目录的文件，进行传播，局限性是不能单独看具体的
#可能还需要一个更具体的Singe来对每一个再跑……

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


from class_network_1 import inf_network
from Document_Save import Document_Save
from Node_Layer_Sel import Node_Sel_Betw
from MULTI_SPREAD import MULTI_NETWORK_SPREAD_SN
from Detail import Detail_csv
from Node_Layer_Sel import Betw_Layer#选层
from Node_Layer_Sel import Gravity_Node#选点


ROOT_NAME = os.getcwd()#不包含/

NETWORK_NAME = os.path.split(ROOT_NAME)[1]#SMALL_50_Given_0.6

# NETWORK_NAME = ROOT_NAME.split('/')[-1]

BETA = 0.5

SKIP_NAME = '__pycache__'

Given = 'Given'

RADIUS = 2

Random = 'Random'

WEI_NAME = 'Wei_Btw_Layer.pkl'

SP_NAME = 'SP_Info.pkl'

COMPRESS_NAME = 'Compress_NT.nt'





MULTI_NETWORK = list()


NAME_NT = lambda x: x + '.nt'

detail = open(ROOT_NAME + '/' + 'detail.txt', 'r')
details = detail.readlines()
detail.close()
value = details[0].replace('\n', '').split(' ')
value_2 = [int(nb) for nb in details[1].replace('\n', '').split()]
infm = zip(value, value_2)
N_NODES, N_LAYERS = value_2

for i in range(N_LAYERS):
	NETWORK = inf_network(True, path = ROOT_NAME + '/' + NAME_NT(str(i)))
	NETWORK.layer = i
	MULTI_NETWORK.append(NETWORK)

for root, dirs, files in os.walk(os.getcwd()):
	#root:/Users/pangyusheng/Desktop/论文/NETWORKS/new mission/SIMPLE_50/SMALL_50_Given_0.3
	if '__pycache__' in dirs:
		dirs.remove('__pycache__')
	if len(dirs) == 0:
		#表明是子目录
		print("Now in the network: {}".format(root.split('/')[-1]))
		Wei_Btw_Layer = list()
		SP_Info = dict()
		for name in files:
			if name.endswith(WEI_NAME):
				pkl_file = open(os.path.join(root, name), 'rb')
				Wei_Btw_Layer = pickle.load(pkl_file)
				pkl_file.close()
			elif name.endswith(SP_NAME):
				pkl_file = open(os.path.join(root, name), 'rb')
				SP_Info = pickle.load(pkl_file)
				pkl_file.close()
		# Max_Node, Max_Layer = Node_Sel_Betw(MULTI_NETWORK, N_LAYERS, N_NODES, SP_Info, RADIUS)
		Max_Layer = Betw_Layer(MULTI_NETWORK, N_NODES, N_LAYERS, SP_Info)
		Max_Node = Gravity_Node(MULTI_NETWORK, SP_Info, Max_Layer, N_LAYERS, N_NODES, RADIUS)#注意带入Max_Layer

		NUM_INFLUENCE, NUM_TIME, TIME_LAYER_LIST = MULTI_NETWORK_SPREAD_SN(MULTI_NETWORK, N_LAYERS, Max_Node, Max_Layer, Wei_Btw_Layer, BETA)
		DOC_Pre = os.path.split(root)[1]#获取文件名开头
		Detail_csv(TIME_LAYER_LIST, N_NODES * N_LAYERS, NUM_INFLUENCE, NUM_TIME, BETA,os.path.join(root, DOC_Pre + time.strftime("_%Y_%m_%d_%H_%M_%S", time.localtime())))
		print('Next...')

print("End.")












