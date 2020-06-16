import networkx as nx
from networkx.exception import NetworkXError
from networkx.utils import not_implemented_for
import json
from networkx.readwrite import json_graph
import numpy as np
import sys
import random
from random import shuffle
import os

WALK_LEN=5
N_WALKS=50

def gen_setcover_inst(total_nodes,fract):
    frac_primal = fract
    p = 0.009

    print('-----','total_nodes = ',total_nodes)
    print('-----','frac_primal = ',frac_primal)

    cur_n = total_nodes
    num_primal = int(cur_n * frac_primal)
    num_dual = cur_n - num_primal

    a = range(num_primal)
    b = range(num_primal, num_dual + num_primal)

    g = nx.Graph()
    g.add_nodes_from(a, bipartite=0)
    g.add_nodes_from(b, bipartite=1)

    colHasOneBool = [0]*num_primal



    overlap_3_highest_degree_node_ids =[0,1,2]
    overlap_dual_nodes = [1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    overlap_dual_nodes= [ x+ num_primal for x in overlap_dual_nodes]

    for i in overlap_3_highest_degree_node_ids:
        for j in overlap_dual_nodes:
            g.add_edge(i,j)
            colHasOneBool[i] = 1




    pass

    for i in range(num_primal,num_primal+num_dual):
        # guarantee that each element is in at least 2 sets, based on http://link.springer.com/chapter/10.1007%2FBFb0120886#page-1
        # k1 = np.random.randint(num_primal)
        # g.add_edge(k1, i + num_primal)
        # while(1):
        #     k2 = np.random.randint(num_primal)
        #
        #     if( k2 not in overlap_3_highest_degree_node_ids and g.degree()[k2] < len(overlap_dual_nodes) -4):
        #         g.add_edge(k2, i + num_primal)
        #         break

        #

        if i in overlap_dual_nodes:
            continue

        for j in range(num_primal):
        #    if j == k1 or j == k2:
         #       continue

            if( j in overlap_3_highest_degree_node_ids):
                continue
            r = np.random.rand()
            if r < p and g.degree()[j] < len(overlap_dual_nodes)-3:
                g.add_edge(j, i)
                colHasOneBool[j] = 1

    # guarantee that each set has at least 1 element, based on http://link.springer.com/chapter/10.1007%2FBFb0120886#page-1
    for j in range(num_primal):
        if colHasOneBool[j] == 0:
            randrow = np.random.randint(num_dual-len(overlap_dual_nodes))
            g.add_edge(j, randrow + num_primal+len(overlap_dual_nodes))

   # for j in [0,1,2]:



    return g



@not_implemented_for('multigraph')
def divrank(G, alpha=0.25, d=0.85, personalization=None,
            max_iter=1000, tol=1.0e-6, nstart=None, weight='weight',
            dangling=None):
    '''
    Returns the DivRank (Diverse Rank) of the nodes in the graph.
    This code is based on networkx.pagerank.

    Args: (diff from pagerank)
      alpha: controls strength of self-link [0.0-1.0]
      d: the damping factor

    Reference:
      Qiaozhu Mei and Jian Guo and Dragomir Radev,
      DivRank: the Interplay of Prestige and Diversity in Information Networks,
      http://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.174.7982
    '''

    if len(G) == 0:
        return {}

    if not G.is_directed():
        D = G.to_directed()
    else:
        D = G

    # Create a copy in (right) stochastic form
    W = nx.stochastic_graph(D, weight=weight)
    N = W.number_of_nodes()

    # self-link (DivRank)
    for n in W.nodes_iter():
        for n_ in W.nodes_iter():
            if n != n_ :
                if n_ in W[n]:
                    W[n][n_][weight] *= alpha
            else:
                if n_ not in W[n]:
                    W.add_edge(n, n_)
                W[n][n_][weight] = 1.0 - alpha

    # Choose fixed starting vector if not given
    if nstart is None:
        x = dict.fromkeys(W, 1.0 / N)
    else:
        # Normalized nstart vector
        s = float(sum(nstart.values()))
        x = dict((k, v / s) for k, v in nstart.items())

    if personalization is None:
        # Assign uniform personalization vector if not given
        p = dict.fromkeys(W, 1.0 / N)
    else:
        missing = set(G) - set(personalization)
        if missing:
            raise NetworkXError('Personalization dictionary '
                                'must have a value for every node. '
                                'Missing nodes %s' % missing)
        s = float(sum(personalization.values()))
        p = dict((k, v / s) for k, v in personalization.items())

    if dangling is None:
        # Use personalization vector if dangling vector not specified
        dangling_weights = p
    else:
        missing = set(G) - set(dangling)
        if missing:
            raise NetworkXError('Dangling node dictionary '
                                'must have a value for every node. '
                                'Missing nodes %s' % missing)
        s = float(sum(dangling.values()))
        dangling_weights = dict((k, v/s) for k, v in dangling.items())
    dangling_nodes = [n for n in W if W.out_degree(n, weight=weight) == 0.0]

    # power iteration: make up to max_iter iterations
    for _ in range(max_iter):
        xlast = x
        x = dict.fromkeys(xlast.keys(), 0)
        danglesum = d * sum(xlast[n] for n in dangling_nodes)
        for n in x:
            D_t = sum(W[n][nbr][weight] * xlast[nbr] for nbr in W[n])
            for nbr in W[n]:
                #x[nbr] += d * xlast[n] * W[n][nbr][weight]
                x[nbr] += (
                    d * (W[n][nbr][weight] * xlast[nbr] / D_t) * xlast[n]
                )
            x[n] += danglesum * dangling_weights[n] + (1.0 - d) * p[n]

        # check convergence, l1 norm
        err = sum([abs(x[n] - xlast[n]) for n in x])
        if err < N*tol:
            return x
    raise NetworkXError('divrank: power iteration failed to converge '
                        'in %d iterations.' % max_iter)


def divrank_scipy(G, alpha=0.25, d=0.85, personalization=None,
                  max_iter=100, tol=1.0e-6, nstart=None, weight='weight',
                  dangling=None):
    '''
    Returns the DivRank (Diverse Rank) of the nodes in the graph.
    This code is based on networkx.pagerank_scipy
    '''
    import scipy.sparse

    N = len(G)
    if N == 0:
        return {}

    nodelist = G.nodes()
    M = nx.to_scipy_sparse_matrix(G, nodelist=nodelist, weight=weight,
                                  dtype=float)
    S = scipy.array(M.sum(axis=1)).flatten()
    S[S != 0] = 1.0 / S[S != 0]
    Q = scipy.sparse.spdiags(S.T, 0, *M.shape, format='csr')
    M = Q * M

    # self-link (DivRank)
    M = scipy.sparse.lil_matrix(M)
    M.setdiag(0.0)
    M = alpha * M
    M.setdiag(1.0 - alpha)
    #print M.sum(axis=1)

    # initial vector
    x = scipy.repeat(1.0 / N, N)

    # Personalization vector
    if personalization is None:
        p = scipy.repeat(1.0 / N, N)
    else:
        missing = set(nodelist) - set(personalization)
        if missing:
            raise NetworkXError('Personalization vector dictionary '
                                'must have a value for every node. '
                                'Missing nodes %s' % missing)
        p = scipy.array([personalization[n] for n in nodelist],
                        dtype=float)
        p = p / p.sum()

    # Dangling nodes
    if dangling is None:
        dangling_weights = p
    else:
        missing = set(nodelist) - set(dangling)


        if missing:
            raise NetworkXError('Dangling node dictionary '
                                'must have a value for every node. '
                                'Missing nodes %s' % missing)
        # Convert the dangling dictionary into an array in nodelist order
        dangling_weights = scipy.array([dangling[n] for n in nodelist],
                                       dtype=float)
        dangling_weights /= dangling_weights.sum()
    is_dangling = scipy.where(S == 0)[0]

    # power iteration: make up to max_iter iterations
    for _ in range(max_iter):
        xlast = x
        D_t =  M * x
        x = (
            d * (x / D_t * M * x + sum(x[is_dangling]) * dangling_weights)
            + (1.0 - d) * p
        )
        # check convergence, l1 norm
        err = scipy.absolute(x - xlast).sum()
        if err < N * tol:
            return dict(zip(nodelist, map(float, x)))

    raise NetworkXError('divrank_scipy: power iteration failed to converge '
                        'in %d iterations.' % max_iter)



def run_random_walks(G, nodes, num_walks=N_WALKS):
    pairs = []
    for count, node in enumerate(nodes):
        if G.degree(node) == 0:
            continue
        for i in range(num_walks):
            curr_node = node
            for j in range(WALK_LEN):
                next_node = random.choice(G.neighbors(curr_node))
                # self co-occurrences are useless
                if curr_node != node:
                    pairs.append((node,curr_node))
                curr_node = next_node
        if count % 1000 == 0:
            print("Done walks for", count, "nodes")
    return pairs

def genNewGraph(graph_id, total_nodes, frac_primal, num_k):
	dir_name = "./GraphSAGE-master/graph_data/" + "graph" + str(graph_id) + "/"
	if not os.path.exists(os.path.dirname(dir_name)):
		os.makedirs(dir_name)
	graph_name = dir_name + "graph" + str(graph_id)
	# UG = nx.gnm_random_graph(total_nodes, edges_per_node)
	UG = gen_setcover_inst(total_nodes,frac_primal)

	# page_rank = nx.pagerank(UG)
	# div_rank = divrank(UG)

	degree_of_nodes = UG.degree()

	all_nodes = nx.nodes(UG)

	features = []

	sum_degree = 0

	for node_i in all_nodes:
		features.append([])
		sum_degree = sum_degree + degree_of_nodes[node_i]

	for node_i in all_nodes:
		# features[node_i].append(page_rank[node_i])
		# features[node_i].append(div_rank[node_i])
		norm_value = degree_of_nodes[node_i]*1.0/sum_degree
		features[node_i].append(norm_value)


	validation_set = (0.95*total_nodes)
	test_set = (0.98*total_nodes)
	random_list = [i for i in range(total_nodes)]
	shuffle(random_list)

	for node in range(0,total_nodes):
		if node<validation_set:
			UG.node[random_list[node]]['val'] = False
			UG.node[random_list[node]]['test'] = False
		elif node<test_set:
			UG.node[random_list[node]]['val'] = True
			UG.node[random_list[node]]['test'] = False
		else:
			UG.node[random_list[node]]['val'] = False
			UG.node[random_list[node]]['test'] = True

	nx.set_edge_attributes(UG, 'test_removed', False)
	nx.set_edge_attributes(UG, 'train_removed', False)

	json_graph_name = graph_name + "-G.json"
	json_id_map_name = graph_name + "-id_map.json"
	feats_file_name = graph_name + "-feats.npy"

	np.save(feats_file_name,features)
	data = json_graph.node_link_data(UG)
	graphjson = json.dumps(data)
	f1=open(json_graph_name, 'w')
	f1.write(graphjson)
	f1.close()

	id_map = {}

	for node in range(0,total_nodes):
		id_map[str(node)] = node

	iddata = json.dumps(id_map)
	f2=open(json_id_map_name, 'w')
	f2.write(iddata)
	f2.close()

	nodes = [n for n in UG.nodes() if not UG.node[n]["val"] and not UG.node[n]["test"]]
	G = UG#.subgraph(nodes)

#	pairs = run_random_walks(G, nodes)

	#out_file = graph_name + "-walks.txt"

	#with open(out_file, "w") as fp:
	#	fp.write("\n".join([str(p[0]) + "\t" + str(p[1]) for p in pairs]))

	class_map_file = graph_name + "-class_map.json"

	class_map = {}

	os.chdir("./greedy_baseline")

	graph_file_name = "." + json_graph_name

	command = "sh ./find_greedy.sh " + graph_file_name + " " + str(num_k)

	os.system(command)


	solution_file_name = graph_file_name + ".greedySol"

	# solution_file_name = "./greedy_baseline/solution_greedy.txt"  

	solution_file = open(solution_file_name,"r")
	os.chdir("../")
	greedy_nodes = solution_file.readlines()
	temp_selected_nodes = greedy_nodes[0].strip().split(' ')
	
	os.chdir("./random_baseline")

	graph_file_name = "." + json_graph_name

	command = "sh ./find_random.sh " + graph_file_name + " " + str(num_k)

	os.system(command)
	os.chdir("../")

	os.chdir("./top-k_baseline")

	graph_file_name = "." + json_graph_name

	command = "sh ./find_top-k.sh " + graph_file_name + " " + str(num_k)

	os.system(command)
	os.chdir("../")

	for node in range(0,total_nodes):
		class_map[str(node)] = [float(temp_selected_nodes[node])]

	classdata = json.dumps(class_map)
	f2=open(class_map_file, 'w')
	f2.write(classdata)
	f2.close()