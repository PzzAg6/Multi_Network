#Single_select
#将该文件放在需要运行的目录下方，可以输出指定的循环操作，生成结果
#2021.12.14
#可以多个节点同时传播，函数为MULTI_NETWORK_SPREAD_MN


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
import sys

sys.path.append("..")
from class_network_1 import inf_network
from Node_Layer_Sel import Node_Sel_Betw
from MULTI_SPREAD import MULTI_NETWORK_SPREAD_SN
#from MULTI_SPREAD import MULTI_NETWORK_SPREAD_MN
from Detail import Detail_csv
from Node_Layer_Sel import Betw_Layer#选层
from Node_Layer_Sel import Gravity_Node#选点


ROOT_NAME = os.getcwd()#不包含/

FATHER_ROOT_NAME, DOC_NAME = os.path.split(ROOT_NAME)
#FATHER_ROOT_NAME = '/Users/pangyusheng/Desktop/论文/NETWORKS/new mission/SIMPLE_50'
#DOC_NAME = 'SMALL_50_Given_0.6'

NETWORK_NAME = ROOT_NAME.split('/')[-1]

BETA = 0.5

SKIP_NAME = '__pycache__'

Given = 'Given'

REPEAT_TIME = 2

RADIUS = 2

Random = 'Random'

WEI_NAME = '_Wei_Btw_Layer.pkl'

SP_NAME = '_SP_Info.pkl'

COMPRESS_NAME = '_Compress_NT.nt'


MULTI_NETWORK = list()


NAME_NT = lambda x: x + '.nt'

detail = open(FATHER_ROOT_NAME + '/' + 'detail.txt', 'r')
details = detail.readlines()
detail.close()
value = details[0].replace('\n', '').split(' ')
value_2 = [int(nb) for nb in details[1].replace('\n', '').split()]
infm = zip(value, value_2)
N_NODES, N_LAYERS = value_2

for i in range(N_LAYERS):
	NETWORK = inf_network(True, path = FATHER_ROOT_NAME + '/' + NAME_NT(str(i)))
	NETWORK.layer = i
	MULTI_NETWORK.append(NETWORK)


Wei_Btw_Layer = list()
SP_Info = dict()

Wei_pkl_file = open(ROOT_NAME + '/' + DOC_NAME + WEI_NAME, 'rb')
Wei_Btw_Layer = pickle.load(Wei_pkl_file)
Wei_pkl_file.close()

SP_pkl_file = open(ROOT_NAME + '/' + DOC_NAME + SP_NAME, 'rb')
SP_Info = pickle.load(SP_pkl_file)
SP_pkl_file.close()

# Max_Node, Max_Layer = Node_Sel_Betw(MULTI_NETWORK, N_LAYERS, N_NODES, SP_Info, RADIUS)
Max_Layer = Betw_Layer(MULTI_NETWORK, N_NODES, N_LAYERS, SP_Info)
Max_Node = Gravity_Node(MULTI_NETWORK, SP_Info, Max_Layer, N_LAYERS, N_NODES, RADIUS)#注意带入Max_Layer

for i in range(REPEAT_TIME):
	print("Now excuting {} iteration".format(i + 1))
	NUM_INFLUENCE, NUM_TIME, TIME_LAYER_LIST = MULTI_NETWORK_SPREAD_SN(MULTI_NETWORK, N_LAYERS, Max_Node, Max_Layer, Wei_Btw_Layer, BETA)
	Detail_csv(TIME_LAYER_LIST, N_NODES * N_LAYERS, NUM_INFLUENCE, NUM_TIME, BETA, os.path.join(ROOT_NAME, DOC_NAME + time.strftime("_%Y_%m_%d_%H_%M_%S", time.localtime())) + '_{}'.format(i))
	print('Next...')



