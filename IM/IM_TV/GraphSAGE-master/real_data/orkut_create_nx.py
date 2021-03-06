#
import networkx as nx
import json
from networkx.readwrite import json_graph
import sys
import numpy as np
from random import sample

dataset="orkut/"
model='TV'
dataset=dataset+ model
train_or_test= "test"

input_file_path =dataset+'/'+"/"+train_or_test+"/sorted_edges.txt"
#input_file_path =dataset+"/"+train_or_test+"/edges.txt"

id_map ={}
json_id_map_name =dataset +'/' + train_or_test+"/large_graph"+"-id_map.json"

G = nx.DiGraph(name=dataset)

node_dic = {}
count = 0
print("json file name ", json_id_map_name)

set_processed = set()
input_file_name = input_file_path
print("input file of edges ", input_file_name
      )
file = open(input_file_name, 'r')

print (len(set_processed))
print(input_file_name)
# lines = 2000
counter = 0
while True:
    counter+=1

    if counter %100 ==0:
        print ("completed ", counter , " lines")
       # break
    # for line in file_handle.readline():
    line = file.readline()
    if len(line)<3:
        break

    edges = line.strip()
    # if len(edges)==0:
    # continue
    edge = edges.split()
    # print(edge)
    source = int(edge[0].rstrip('\x00'))
    target = int(edge[1].rstrip('\x00'))
    weight = float(edge[2].rstrip('\x00'))
   # weight_list = [0.1,0.01,0.001]

#	if (source ==target):
#		continue

    # if source not in node_dic:
    #     node_dic[source] = count
    #     count = count + 1
    #
    # if target not in node_dic:
    #     node_dic[target] = count
    #     count = count + 1

    id_map[source] = source
    id_map[target] =target

    #check_string = str(node_dic[source])+ ' '+str(node_dic[target])
    #if check_string in set_processed:
#		print (check_string)
    #	continue
    #set_processed.add(check_string)

    #inf_prob = 0.1  # float(edge[2].rstrip('\x00'))
  #  weight = sample(weight_list,1)[0]
   # file_write.write( str(node_dic[source]) + ' ' + str(node_dic[target]) +' ' + str(weight)+'\n')
    #id_map[str(node_dic[source])] = node_dic[source]
    #id_map[str(node_dic[target])] = node_dic[target]

 #   G.add_edge(node_dic[source], node_dic[target], weight =weight)

  #  weight = sample(weight_list,1)[0]
  #  file_write.write( str(node_dic[target]) + ' ' + str(node_dic[source]) +' ' + str(weight)+'\n')
    #id_map[str(node_dic[source])] = node_dic[source]
    #id_map[str(node_dic[target])] = node_dic[target]

    G.add_edge(target, source, weight =weight)


print(count)
# print(len(edges_dict))

#   print(n1,n2)
# pass


data1 = json_graph.node_link_data(G)
s1 = json.dumps(data1)
print("dumping to ", dataset +'/' + train_or_test+"/large_graph-G.json")

file1 = open(dataset +'/' + train_or_test+"/large_graph-G.json","w")

file1.write(s1)
file1.close()

#print >>file1, s1
#ith open("train/large_graph-G.json") as f:
#	js_graph = json.load(f)

#H = json_graph.node_link_graph(js_graph)


iddata = json.dumps(id_map)
f2 = open(json_id_map_name, 'w')
f2.write(iddata)
f2.close()
print(json_id_map_name)
#
# # degree_of_nodes = G.out_degree(weight='weight')
#
# all_nodes=nx.nodes(G_sub)
# total_nodes=len(all_nodes)
# print("total nodes", total_nodes)
# features=[]
# # weight_list = [0.1,0.01,0.001]
#
# #   sum_degree = 0
# sum_weight_out=0.0
# #
# # for node_i in all_nodes:
# #     features.append([])
# #  #   sum_degree = sum_degree + degree_of_nodes[node_i]
# #     # sum_weight_in = sum_weight_in + node_weights_incoming[node_i]
# #     sum_weight_out = sum_weight_out + degree_of_nodes[node_i]
# #
# #
# # # print("sum in sum out", sum_weight_in, sum_weight_out)
# # print("sum out",  sum_weight_out)
# #
# # for node_i in all_nodes:
# #     # features[node_i].append(page_rank[node_i])
# #     # features[node_i].append(div_rank[node_i])
# #  #   norm_value = degree_of_nodes[node_i]*1.0/sum_degree
# #
# #     norm_value_out = degree_of_nodes[node_i]*1.0/sum_weight_out
# #     # norm_value_in = node_weights_incoming[node_i]*1.0/sum_weight_in
# #
# # #     features[node_i].append(norm_value)
# #     features[node_i].append(norm_value_out)
# #     # features[node_i].append(norm_value_in)
# #
# # print('Length of the features = ',len(features),total_nodes)
# # #
# #

attribute_file_name=dataset +'/' + train_or_test+'/'  + 'attribute.txt'
print("attribute ", attribute_file_name)
attribute_file = open(attribute_file_name,'w')
attribute_file.write(str(len(G)) +"   " +str(G.number_of_edges()))
#np.save(feats_file_name, features)



#
#
#
#
#
#
#
#
#




