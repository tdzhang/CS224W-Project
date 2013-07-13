#triangle finding in directed weigthed graph
import networkx as nx
import matplotlib . pyplot as plt
import numpy as np
import pickle 
import random
from functions import *



#read in the networks
read_file='soc-sign-epinions.txt'
G=nx.read_weighted_edgelist(read_file, comments='#', delimiter='\t', create_using=nx.DiGraph(), nodetype=int, encoding='utf-8')
UG=G.to_undirected()

#--------------------Sample 2and3 steps feature and save to file-------------------#
Sample_Number=100000;
sampled_edges=random.sample(G.edges(),Sample_Number);
outfile=open('sampleDandR100000with35f','w')
index_i=0
for (a,b) in sampled_edges:
	index_i=index_i+1
	if index_i%5==0:
		print("current percent",float(index_i)/Sample_Number)
	feature2=find_2step_feature(G,a,b) #forward 2 step feature
	feature3=find_3step_feature(G,a,b) #forward 3 step feature
	feature4=find_2step_feature(G,b,a) #backward 2 step feature
	feature5=find_3step_feature(G,b,a) #backward 3 step feature
	feature6=find_in_out_plus_minus_degree(G,a)
	feature7=find_in_out_plus_minus_degree(G,b)
	feature2.extend(feature3)
	feature2.extend(feature4)
	feature2.extend(feature5)
	feature2.extend(feature6)
	feature2.extend(feature7)
	feature2.extend([nx.clustering(UG,a),nx.clustering(UG,b)])
	for feature in feature2:
  		outfile.write("%s," %feature)
	flag=G[a][b]['weight']
	outfile.write("%s\n" %flag)
outfile.close()