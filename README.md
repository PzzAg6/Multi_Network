# Multi_Network
多层网络的节点，层选取，以及网络传播等



# 2021.11.23  

由于`pickle`实在太慢了，所以决定把`Document_save.py`中的保存，以及相应文件的读取改为用numpy进行存储和读写。

# 2021.11.24  

在`Gen_Data.py`中删除一行多余的最短路径代码，节省一半的计算时间  

# 2021.11.26  

由于之前在函数里面选层和选种是一起的，所以需要多个排列组合，现在把两个步骤拆开，自行选择选层选种策略

# 2021.11.28  

计算最短路径的权重和时，涉及到从一层到另一层到时候，权重由c改为1 - c  

# 2021.12.2  

之前保存层间权重是随机的网络出现了问题，保存的部分用的是Given的值，大无语了，重新修改了。

# 2021.12.9  

增加一个能够查看每一层betweeness和neighborhood的文件`Output_Betw_Neigh.py`，导出csv，方便看出规律。并在`Node_Layer_Sel.py`中加入对应的函数

# 2021.12.14

修改`MULTI_SPREAD.py`，增加函数`MULTI_NETWORK_SPREAD_MN`可以多节点传播
修改了`sel`里面的函数，可以根据参数，按照排名选取多个节点。

# 2021.12.16  

原本的`For_One_Network.py`生成的`.csv`是每次循环生成一个文件，为了使统计更简便，改为放进一个文件中，并统计了平均传播节点数量
