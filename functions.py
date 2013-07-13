#triangle finding in directed weigthed graph
import networkx as nx
import matplotlib . pyplot as plt
import numpy as np

#-----------------------------predefined function----------------------------#
#find the in nodes of the network
def find_in_nodes(G,node):
	edges=G.in_edges(node)
	in_nodes=[edges[i][0] for i in range(G.in_degree(node))]
	return in_nodes

#return a set:find all the in nodes for a given nodes array(exclude the input nodes)
def find_in_nodeset_ofComponents(G,nodes):
	in_nodes=[]
	for node in nodes:
		in_nodes.extend(find_in_nodes(G,node))
	in_set=set(in_nodes)
	node_set=set(nodes)
	return in_set-node_set

#find the out nodes of the network
def find_out_nodes(G,node):
	edges=G.out_edges(node)
	out_nodes=[edges[i][1] for i in range(G.out_degree(node))]
	return out_nodes

#return a set:find all the out nodes for a given nodes array(exclude the input nodes)
def find_out_nodeset_ofComponents(G,nodes):
	out_nodes=[]
	for node in nodes:
		out_nodes.extend(find_out_nodes(G,node))
	out_set=set(out_nodes)
	node_set=set(nodes)
	return out_set-node_set

#return (balance_number,total_number) for a certain node in G that chained for 3 steps
def step3_balance_number(G,node):
	right=0
	wrong=0
	total=0
	cate_num=dict() #the number 16 cases
	ins=find_in_nodes(G,node)
	outs=find_out_nodes(G,node)
	sub_nodes=ins+outs
	subG=nx.subgraph(G,sub_nodes)
	for in_node in ins:
		c_outs=find_in_nodes(subG,in_node)
		for out_node in c_outs:
			if out_node in outs:
				total=total+1
				#node-->out_node-->mid_node-->in_node-->node
				flag1=(G[node][out_node]['weight']==-1)
				flag2=(G[out_node][in_node]['weight']==-1)
				flag3=(G[in_node][node]['weight']==-1)
				key=str(1000+flag1*100+flag2*10+flag3)
				
				if cate_num.has_key(key):
					cate_num[key]=cate_num[key]+1
				else:
					cate_num[key]=1

				if((flag1+flag2+flag3)%2==0):
					right=right+1
				else:
					wrong=wrong+1
	return (right,total,cate_num)

#return (balance_number,total_number,cate_num) for a certain node in G that chained for 4 steps
def step4_balance_number(G,node):
	right=0
	wrong=0
	total=0
	cate_num=dict() #the number 16 cases
	ins=find_in_nodes(G,node)
	inset=set(ins)
	outs=find_out_nodes(G,node)
	outset=set(outs)
	mid1=find_in_nodeset_ofComponents(G,ins)
	mid2=find_out_nodeset_ofComponents(G,outs)
	midset=mid1&mid2 #this is the intermediate sets of ins and outs
	midarray=[x for x in midset]

	for mid_node in midarray:
		tmp=find_in_nodes(G,mid_node)
		mid_outs=list(set(tmp)&outset)
		tmp=find_out_nodes(G,mid_node)
		mid_ins=list(set(tmp)&inset)
		for in_node in mid_ins:
			for out_node in mid_outs:
				total=total+1
				#node-->out_node-->mid_node-->in_node-->node
				flag1=(G[node][out_node]['weight']==-1)
				flag2=(G[out_node][mid_node]['weight']==-1)
				flag3=(G[mid_node][in_node]['weight']==-1)
				flag4=(G[in_node][node]['weight']==-1)
				key=str(10000+flag1*1000+flag2*100+flag3*10+flag4)
				
				if cate_num.has_key(key):
					cate_num[key]=cate_num[key]+1
				else:
					cate_num[key]=1

				if((flag1+flag2+flag3+flag4)%2==0):
					right=right+1
				else:
					wrong=wrong+1

	return (right,total,cate_num)

#return (balance_number,total_number,cate_num) for a certain node in G that chained for 4 steps
def step4_propagation_number(G,node):
	right=0
	wrong=0
	total=0
	cate_num=dict() #the number 16 cases

	step1=find_out_nodes(G,node)
	step1_set=set(step1)
	step2_set=find_out_nodeset_ofComponents(G,step1)
	step2=list(step2_set)
	step3_set=find_out_nodeset_ofComponents(G,list(step2_set))
	step3_set=step3_set&step1_set
	step3=list(step3_set)
	
	for step2_node in step2:
		tmp=find_in_nodes(G,step2_node)
		s1=list(set(tmp)&step1_set)
		tmp=find_out_nodes(G,step2_node)
		s3=list(set(tmp)&step1_set)
		for in_node in s1:
			for out_node in s3:
				if out_node==in_node:
					continue
				total=total+1
				#node-->out_node  node-->in-->step2-->out
				flag1=(G[node][in_node]['weight']==-1)
				flag2=(G[in_node][step2_node]['weight']==-1)
				flag3=(G[step2_node][out_node]['weight']==-1)
				flag4=(G[node][out_node]['weight']==-1)
				key=str(10000+flag1*1000+flag2*100+flag3*10+flag4)
				
				if cate_num.has_key(key):
					cate_num[key]=cate_num[key]+1
				else:
					cate_num[key]=1

				if((flag1+flag2+flag3+flag4)%2==0):
					right=right+1
				else:
					wrong=wrong+1

	return (right,total,cate_num)

#return the 2 step feature of a edge a->b find a->mid->b
def find_2step_feature(G,a,b):
	cate_num=dict()
	ins=find_in_nodes(G,b)
	outs=find_out_nodes(G,a)
	mid=set(ins)&set(outs)  #get the intermediate point
	for mid_node in mid:
		#a-->mid_node-->b
		flag1=(G[a][mid_node]['weight']==-1)
		flag2=(G[mid_node][b]['weight']==-1)
		key=str(100+flag1*10+flag2*1)
		
		if cate_num.has_key(key):
			cate_num[key]=cate_num[key]+1
		else:
			cate_num[key]=1
	result=[];
	keys=['100','101','111','110'] #++ +- -- -+
	for key in keys:
		if cate_num.has_key(key):
			result.append(cate_num[key])
		else:
			result.append(0)
	return result

#return the 3 step feature of a edge a->b find a->mid1->mid2->b
def find_3step_feature(G,a,b):
	cate_num=dict()
	ins=find_in_nodes(G,b)
	outs=find_out_nodes(G,a)
	ins_t=set(ins)-set(outs)-set([a])
	outs_t=set(outs)-set(ins)-set([b])
	oouts=find_out_nodeset_ofComponents(G,outs_t)
	iins=find_in_nodeset_ofComponents(G,ins_t)
	oouts=oouts&ins_t
	iins=iins&outs_t

	for s2_node in iins:
		tmp=find_out_nodes(G,s2_node)
		tmp1=set(tmp)&oouts
		for s3_node in tmp1:
			#node-->out_node  node-->in-->step2-->out
			flag1=(G[a][s2_node]['weight']==-1)
			flag2=(G[s2_node][s3_node]['weight']==-1)
			flag3=(G[s3_node][b]['weight']==-1)
			key=str(1000+flag1*100+flag2*10+flag3)
			
			if cate_num.has_key(key):
				cate_num[key]=cate_num[key]+1
			else:
				cate_num[key]=1

	result=[];
	keys=['1000','1001','1010','1100','1011','1101','1110','1111'] #+++ ++- +-+ -++ +-- -+- --+ ---
	for key in keys:
		if cate_num.has_key(key):
			result.append(cate_num[key])
		else:
			result.append(0)
	return result

#reture the in+ in- out+ out-
def find_in_out_plus_minus_degree(G,node):
	in_nodes=find_in_nodes(G,node)
	out_nodes=find_out_nodes(G,node)
	inp=0
	inm=0
	outp=0
	outm=0
	for in_node in in_nodes:
		if G[in_node][node]['weight']==1:
			inp=inp+1
		else:
			inm=inm+1
	for out_node in out_nodes:
		if G[node][out_node]['weight']==1:
			outp=outp+1
		else:
			outm=outm+1
	return [inp,inm,outp,outm]

#reture the in+ in- out+ out-
def find_in_plus_minus_degree_with_pagerank(G,node,pagerank):
	in_nodes=find_in_nodes(G,node)
	inp=0
	inm=0
	for in_node in in_nodes:
		if G[in_node][node]['weight']==1:
			inp=inp+pagerank[in_node]
		else:
			inm=inm+pagerank[in_node]
	return [inp,inm]

def find_in_plus_minus_degree_with_pagerank_except(G,node,pagerank,ex_node):
	in_nodes=find_in_nodes(G,node)
	ins=set(in_nodes)-set([ex_node])
	inp=0
	inm=0
	for in_node in list(ins):
		if G[in_node][node]['weight']==1:
			inp=inp+pagerank[in_node]
		else:
			inm=inm+pagerank[in_node]
	return [inp,inm]


