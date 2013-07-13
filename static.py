#triangle finding in directed weigthed graph
import networkx as nx
import matplotlib . pyplot as plt
import numpy as np
import pickle
from functions import *



#read in the networks
#read_file='soc-sign-epinions.txt'
read_file='soc-sign-Slashdot090221.txt'
G=nx.read_weighted_edgelist(read_file, comments='#', delimiter='\t', create_using=nx.DiGraph(), nodetype=int, encoding='utf-8')

total_nodes=G.number_of_nodes()
print('total_nodes=',total_nodes)
total_edges=G.number_of_edges()
print('total_edges=',total_edges)

posi=0
naga=0
for (a,b) in G.edges():
	if G[a][b]['weight']==1:
		posi=posi+1
	else:
		naga=naga+1
print('positive_edge=',posi)
print('ratio=',float(posi)/total_edges)
print('nagative_edge=',naga)
print('ratio=',float(naga)/total_edges)

print('SCC=',len(nx.strongly_connected_components(G)[0]))
print('WCC=',len(nx.weakly_connected_components(G)[0]))


NDG=G.to_undirected();
print('average_clustering=',nx.average_clustering(NDG))
print('transitivity=',nx.transitivity(NDG)) 
