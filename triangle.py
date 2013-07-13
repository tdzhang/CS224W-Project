#triangle finding in directed weigthed graph
import networkx as nx
import matplotlib . pyplot as plt
import numpy as np
import pickle 
import random
from functions import *



#read in the networks
#read_file='soc-sign-Slashdot090221.txt'
read_file='soc-sign-epinions.txt'
G=nx.read_weighted_edgelist(read_file, comments='#', delimiter='\t', create_using=nx.DiGraph(), nodetype=int, encoding='utf-8')
UG=G.to_undirected()

#--------------------Sample 2and3 steps feature and save to file-------------------#
G_temp=G.copy()
for (node_a,node_b) in G.edges():
		if G_temp[node_a][node_b]['weight']==-1:
			G_temp.remove_edge(node_a,node_b)
			G_temp.add_edge(node_b,node_a)
			G_temp[node_b][node_a]['weight']=1

page_rank=nx.pagerank(G_temp,max_iter=300,tol=1e-08)

#存一下pagerank
pickle.dump( page_rank, open( "page_rank_1e8.p", "wb" ) )

#--------------------Sample 2and3 steps feature and save to file-------------------#
Sample_Number=100000;
sampled_edges=random.sample(G.edges(),Sample_Number);
outfile=open('featuresWithStatus.txt','w')
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
	feature8=find_in_plus_minus_degree_with_pagerank(G,a,page_rank)
	feature9=find_in_plus_minus_degree_with_pagerank_except(G,b,page_rank,a)
	feature2.extend(feature3)
	feature2.extend(feature4)
	feature2.extend(feature5)
	feature2.extend(feature6)
	feature2.extend(feature7)
	feature2.extend([nx.clustering(UG,a),nx.clustering(UG,b)])
	feature2.extend([page_rank[a],page_rank[b]])
	feature2.extend(feature8)
	feature2.extend(feature9)
	for feature in feature2:	
  		outfile.write("%s," %feature)
	flag=G[a][b]['weight']
	outfile.write("%s," %flag)
	outfile.write("(%s," %a)
	outfile.write("%s)\n" %b)
outfile.close()

#-----------------------------propagation for 4 steps----------------------------#
right=0
total=0
index_i=0
index_t=G.number_of_nodes()
cate_num=dict();

#the accurate list for nodes with more than one traid
accurate_list=[]
for x in G.nodes():
	index_i=index_i+1
	if index_i%5==0:
		print("current percent",float(index_i)/index_t)
	(t_r,t_t,t_c)=step4_propagation_number(G,x)
	right=right+t_r
	total=total+t_t
	for key in t_c:
		if cate_num.has_key(key):
			cate_num[key]=cate_num[key]+t_c[key]
		else:
			cate_num[key]=t_c[key]
	if t_t!=0:
		accurate_list.append(float(t_r)/t_t)
#save/read the data
#pickle.dump((cate_num,accurate_list,right,total), open( "prop_step4.p", "wb" ))
#(cate_num,accurate_list,right,total)=pickle.load(open( "prop_step4.p", "rb" ))

#-----------------------------chain for 4 steps----------------------------#
right=0
total=0
index_i=0
index_t=G.number_of_nodes()
cate_num=dict();

#the accurate list for nodes with more than one traid
accurate_list=[]
for x in G.nodes():
	index_i=index_i+1
	if index_i%5==0:
		print("current percent",float(index_i)/index_t)
	(t_r,t_t,t_c)=step4_balance_number(G,x)
	right=right+t_r
	total=total+t_t
	for key in t_c:
		if cate_num.has_key(key):
			cate_num[key]=cate_num[key]+t_c[key]
		else:
			cate_num[key]=t_c[key]
	if t_t!=0:
		accurate_list.append(float(t_r)/t_t)
#save/read the data
#pickle.dump((cate_num,accurate_list,right,total), open( "step4.p", "wb" ) )
#(cate_num,accurate_list,right,total)=pickle.load(open( "step4.p", "rb" ))



	


#-----------------------------chain for 3 step(triangle)----------------------------#
right=0
total=0
index_i=0
index_t=G.number_of_nodes()
cate_num=dict();

#the accurate list for nodes with more than one traid
accurate_list=[]
for x in G.nodes():
	index_i=index_i+1
	if index_i%50==0:
		print("current percent",float(index_i)/index_t)
	(t_r,t_t,t_c)=step3_balance_number(G,x)
	right=right+t_r
	total=total+t_t
	for key in t_c:
		if cate_num.has_key(key):
			cate_num[key]=cate_num[key]+t_c[key]
		else:
			cate_num[key]=t_c[key]
	if t_t!=0:
		accurate_list.append(float(t_r)/t_t)
	
#accuracy
print("accuracy percent",float(right)/total)

#pickle.dump((cate_num,accurate_list,right,total), open( "step3.p", "wb" ) )
#(cate_num,accurate_list,right,total)=pickle.load(open( "step3.p", "rb" ))

#histgram
n, bins, patches=plt.hist(accurate_list, bins=np.linspace(0,1,30),normed=1, facecolor='b', alpha=0.75)
#plt.xscale('log')
#plt.yscale('log')
plt.title('histogram of directed balance traid')
plt.ylabel('number of nodes')
plt.xlabel('accuracy')
plt.grid(True)
plt.show()






