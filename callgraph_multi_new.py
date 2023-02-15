import pydot
import pyparsing
import json
import argparse
import collections
import functools
import networkx as nx
import glob
import glob
import numpy as np
import concurrent.futures
import time


class memoize:
  # From https://github.com/S2E/s2e-env/blob/master/s2e_env/utils/memoize.py

  def __init__(self, func):
    self._func = func
    self._cache = {}

  def __call__(self, *args):
    if not isinstance(args, collections.abc.Hashable):
      return self._func(args)

    if args in self._cache:
      return self._cache[args]

    value = self._func(*args)
    self._cache[args] = value
    return value

  def __repr__(self):
    # Return the function's docstring
    return self._func.__doc__

  def __get__(self, obj, objtype):
    # Support instance methods
    return functools.partial(self.__call__, obj)


# Get graph node name
def node_name (name):
  #print("\"{name}\"")
  #return "\"{%s}\"" % name
  return name



# Find the graph node for a name
@memoize
def find_nodes (name):
  n_name = node_name (name)
  return [n for n, d in G.nodes(data=True) if n_name in d.get('label', '')]

#find all edges for node
def find_edges (node):
  return [e for e in G.edges if node in e]

#find all out going edges for node
def find_out_edges (node):
  return [e for e in G.out_edges(node)]

#find all out going edges for node
#keep only the destination node
def find_out_edges_dest (node):
  return [e[1] for e in G.out_edges(node)]

#find all out going edges for node
#keep only the destination node label
def find_out_edges_dest_label (node, graph):
  #remove quotes
  lable = [graph.nodes[e[1]].get('label', '') for e in graph.out_edges(node)]
  lable = [x.replace('"', '') for x in lable]
  return lable

#return node label
def get_node_label (node, graph):
  label = graph.nodes[node].get('label', '')
  #remove quotes
  #label = label.replace('"', '')
  return label


# for n in find_nodes ("scalar"):
#     print(n)
#     print(G.nodes[n].get('label', ''))

# print(find_out_edges_dest_label("Node1", G))

# for dest_label in find_out_edges_dest_label("Node1", G):
#   print(dest_label)


#callgraphs = glob.glob("./cg/*.dot")
#callgraphs = glob.glob("/Users/jdanceze/Desktop/hub/tf_callgraph/*.dot")
#print(callgraphs)


def process_dot(dot):
    graph_name = nx.drawing.nx_pydot.read_dot(dot).graph.get('name', '')
    print("Add to dict: ",graph_name)
    return graph_name, dot

#recursive function to add nodes and edges to graph

def add_nodes_edges(node, GT):
  count = 0
  for dest_label in find_out_edges_dest_label(node, GT):
    new_dest_label = '"' + dest_label + '"'
    if get_node_label(node, GT) == new_dest_label and count == 0:
      GN.add_edge(get_node_label(node, GT), new_dest_label)
      count+=1
    else:
      GN.add_edge(get_node_label(node, GT), new_dest_label)

      if dest_label in callgraphs:
        dot = callgraphs[dest_label]
        GD = nx.DiGraph(nx.drawing.nx_pydot.read_dot(dot))
        print("Joining: ", GD.graph.get('name', ''))
        add_nodes_edges(node, GD)
  nx.drawing.nx_pydot.write_dot(GN, "./cg_out/cg_out_CompositeTensorVariantToComponents.dot")
  #nx.drawing.nx_pydot.write_dot(GN, "./cg_out/cg.dot")


if __name__ == '__main__':
    
    G = nx.DiGraph(nx.drawing.nx_pydot.read_dot("./cg/CompositeTensorVariantToComponents.dot"))
    #print(G)
    #get graph name
    print("++++++++++++++")
    print(G.graph.get('Reading Graph name', ''))

    GN = nx.DiGraph()
    #get start time
    start_time = time.time()
    
    # callgraphs = glob.glob("/Users/jdanceze/Desktop/hub/tf_callgraph/*.dot")
    # #callgraphs = glob.glob("./cg/*.dot")
    # num_processes = 8

    # with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
    #     result = [x for x in executor.map(process_dot, callgraphs)]
    
    # callgraphs = dict(result)
    # #save dict to json file
    # with open('./merged_cg/merged_callgraphs.json', 'w') as fp:
    #     json.dump(callgraphs, fp)
    # add_nodes_edges("Node1", G)

    #read dict from json file
    with open('./merged_cg/merged_callgraphs.json') as json_file:
        callgraphs = json.load(json_file)
    add_nodes_edges("Node1", G)

    end_time = time.time()
    print("time: ", end_time - start_time)
    #print(callgraphs)

