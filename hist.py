#statistic finding
import networkx as nx
import matplotlib . pyplot as plt
import numpy as np
import numpy
from plfit_py import plfit



#read in the networks
#read_file='soc-sign-epinions.txt'
read_file='soc-sign-Slashdot090221.txt'
G=nx.read_weighted_edgelist(read_file, comments='#', delimiter='\t', create_using=nx.DiGraph(), nodetype=int, encoding='utf-8')

d=nx.degree(G)
#D=sorted(d.items(),key=lambda x:x[1], reverse=True)
#d_sorted=[D1[i][0] for i in range(len(d1))]
x=[d[key] for key in d]
MyPL=plfit(x)
MyPL.plfit()

#xmin alpha 1, 1.6005149337157845

#loglog show
plt.figure(1)
plt.hist(x,bins=10**np.linspace(0,4,1000))
plt.xscale('log')
plt.yscale('log')
plt.title('loglog histgram of degree')
plt.ylabel('number of nodes')
plt.xlabel('degree')
plt.show()



