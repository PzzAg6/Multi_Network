#用于保存每一步的感染数量
import csv

headers = ['TIME', 'NODE#', 'LAYER#']




def Detail_txt(TIME_LAYER_LIST,name):
	TIME = len(TIME_LAYER_LIST) - 1
	read = open(name + '.txt', 'w')
	TIME = 0

	for INF_DIC in TIME_LAYER_LIST:
		read.write(line + '\n')
		# SUM = 0
		read.write('TIME = {}\n'.format(TIME))
		ALL_NODE_SET = set()#避免重复

		
		for layers, node_list in INF_DIC.items():
			ALL_NODE_SET.update(set(node_list))
			Tol_node_list = len(node_list)
			# SUM += Tol_node_list
			str_node_list = [str(i) for i in node_list]
			str_node_list = ', '.join(str_node_list)
			LINE = 'LAYER {0}: {1}, TOTAL:{2}'.format(layers, str_node_list, str(Tol_node_list))
			read.write(LINE + '\n')
		read.write('TOTAL: {} \n'.format(str(len(ALL_NODE_SET))) )
		TIME += 1

def Detail_csv(TIME_LAYER_LIST, N_NODES, NUM_INFLUENCE, NUM_TIME, BETA, name):
	headers = ['TIME', 'NODE#', 'LAYER#']

	with open(name + '.csv', 'a', newline = '') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(['TOTAL NUM:', '{}/{}'.format(NUM_INFLUENCE, N_NODES), ''])
		writer.writerow(['SPREAD TIME', NUM_TIME, ''])
		writer.writerow(['BETA', BETA, ''])
		writer.writerow(headers) 

	TIME = len(TIME_LAYER_LIST) - 1
	
	TIME = 0



	for INF_DIC in TIME_LAYER_LIST:
		
		ALL_NODE_SET = set()
		Tol_node_list = 0

		for layers, node_list in INF_DIC.items():
			ALL_NODE_SET.update(set(node_list))
			Tol_node_list += len(node_list)
			ROW = list(zip([TIME] * len(node_list), [Node for Node in node_list], [layers] * len(node_list)))
			with open(name + '.csv', 'a', newline = '') as csvfile:
				writer = csv.writer(csvfile)
				for row in zip([TIME] * len(node_list), [Node for Node in node_list], [layers] * len(node_list)):
					writer.writerow(list(row))
		with open(name + '.csv', 'a', newline = '') as csvfile:
			writer = csv.writer(csvfile)	
			writer.writerow(['TOTAL:', '{}'.format(len(ALL_NODE_SET)), ''])
		TIME += 1


