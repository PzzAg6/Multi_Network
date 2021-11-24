#在根目录下创建文件夹，然后保存文件
# coding=utf-8
import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt
import copy
import numpy as np
import time
from class_network_1 import inf_network
import os
import pickle
import 


def Document_Save(Root_Name, Doc_Name, Layer_Wei, Compress_NT, SP_Dic):
	#Doc_Name前面不用带/
	#Layer_Wei:层间的权重
	#Compress_NT:压缩网络的内容
	#SP_Dic:最短路径权重信息
	LW = 'Wei_Btw_Layer'
	Com_NT = 'Compress_NT'
	SP_Name = 'SP_Info'	


	New_Root = Root_Name + '/' + Doc_Name

	try:
		os.mkdir(New_Root)
	except FileExistsError:
		pass


	#压缩网络保存
	Com_write = open(New_Root + '/' + '{}.nt'.format(Doc_Name + '_' + Com_NT), 'wb')
	nx.write_multiline_adjlist(Compress_NT, Com_write, delimiter = ',')
	Com_write.close()

	#层间权重保存
	#觉得应该再保存一个可以查看的.csv
	np.save(New_Root + '/' + '{}.npy'.format(Doc_Name + '_' + LW), Layer_Wei)


	#最短路信息保存	
	#觉得应该再保存一个可以查看的.csv
	np.save(New_Root + '/' + '{}.npy'.format(Doc_Name + '_' + SP_Name), SP_Dic)

	return True



