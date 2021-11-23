import networkx as nx
import numpy as np
import random
import matplotlib.pyplot as plt


class inf_network():
	def __init__(self, is_copy, path = None, NT_NAME = nx.barabasi_albert_graph, **kawgrs):
		self.num_nodes = None
		self.num_edges = None
		self.layer = None
		self.network = None
		self.path = path


		if(is_copy == False):
			self.network = NT_NAME(**kawgrs)
			#无论是否需要拷贝,节点属性是都要的
			self.num_nodes = nx.number_of_nodes(self.network)
			self.init()
			# nx.set_node_attributes(self.network, False, "INFECTED")#设置节点属性
			# nx.set_node_attributes(self.network, None, "INFECTED_TIME")#设置节点属性	
			for edge in self.network.edges:
				self.network.edges[edge]['weight'] = None#初始化权重
		else:
			self.copy_data(path)

	def set_random(self, fun, **kawgrs):
		return fun(**kawgrs)		


	def random_gen(self,mu = 0,sigma = 1):
		#生成符合分布的随机数
		val = random.gauss(mu, sigma)
		while( val <= 0 or val > 1):
			val = random.gauss(mu, sigma)
		return val

	def change_weight(self, fun, **kawgrs):
		#改变边的权重
		try:
			# print("Normal")
			for edge in self.network.edges:
				self.network.edges[edge]['weight'] = fun(**kawgrs)
		except:
			# print("random.random()")
			for edge in self.network.edges:
				self.network.edges[edge]['weight'] = fun()#主要针对没有参数的随机数,如random.random()
		return self

	def test(self, attr = 'weight'):
		# nx.draw(self.network)
		if(attr == 'weight'):
			print('weight:')
			for n, nbrs in self.network.adj.items():
				for nbr, eattr in nbrs.items():
					wt = eattr['weight']
					print("weight of {0} and {1} is {2}".format(n, nbr, wt))
			print('___________________________________________')
		if(attr == 'influence'):
			print('influence:')
			for n in self.network.nodes():
				print(self.network.nodes[n]['influence'])
			print('___________________________________________')

	def set_attr(self, attr, value = None):
		for nodes in self.network.nodes:
			self.network.nodes[nodes][attr] = value

	def init(self):
		#重置
		nx.set_node_attributes(self.network, None, 'influence')
		nx.set_node_attributes(self.network, False, "INFECTED")#设置节点属性
		nx.set_node_attributes(self.network, None, "INFECTED_TIME")#设置节点属性

	def copy_data(self, path):
		read = open(path, "rb")
		self.network = nx.read_multiline_adjlist(read, delimiter = ',', nodetype = int)
		read.close()
		self.num_nodes = nx.number_of_nodes(self.network)
		self.init()





if __name__ == '__main__':

	test_nw = inf_network(False, None, nx.barabasi_albert_graph, n = 50, m = 10)
	test_nw.test()
	test_nw.change_weight()
	test_nw.test()
