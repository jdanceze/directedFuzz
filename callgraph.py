import pydot
import pyparsing
import json
import argparse
import collections
import functools
import networkx as nx
import glob


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


G = nx.DiGraph(nx.drawing.nx_pydot.read_dot("./cg/TensorListScatter.dot"))
print(G)
# for n in find_nodes ("scalar"):
#     print(n)
#     print(G.nodes[n].get('label', ''))

print(find_out_edges_dest_label("Node1", G))

for dest_label in find_out_edges_dest_label("Node1", G):
  print(dest_label)

#get graph name
print("++++++++++++++")
print(G.graph.get('name', ''))


callgraphs = glob.glob("./cg/*.dot")
print(callgraphs)
# G4 = nx.DiGraph()
# for dot in callgraphs:
#   G4.update(nx.DiGraph(nx.drawing.nx_pydot.read_dot(dot)))
# nx.drawing.nx_pydot.write_dot(G4, "./cg_out/TensorListScatter3.dot")

# #create a new graph
# G2 = nx.DiGraph()
# first_node = "Node1"

# for dest_label in find_out_edges_dest_label(first_node, G):
#   new_dest_label = '"' + dest_label + '"'
#   G2.add_edge(get_node_label(first_node), new_dest_label)
#   for dot in callgraphs:
#     G3 = nx.DiGraph(nx.drawing.nx_pydot.read_dot(dot))
#     if dest_label in G3.graph.get('name', ''):
#       print(G3.graph.get('name', ''))
#       for dest_label2 in find_out_edges_dest_label(first_node, G3):
#         new_dest_label2 = '"' + dest_label2 + '"'
#         G2.add_edge(new_dest_label, new_dest_label2)

#nx.drawing.nx_pydot.write_dot(G2, "./cg_out/TensorListScatter2.dot")   
      
#recursive function to add nodes and edges to graph
GN = nx.DiGraph()
count = 0
def add_nodes_edges (node, GT):
  for dest_label in find_out_edges_dest_label(node, GT):
    new_dest_label = '"' + dest_label + '"'
    GN.add_edge(get_node_label(node, GT), new_dest_label)
    for dot in callgraphs:
      GD = nx.DiGraph(nx.drawing.nx_pydot.read_dot(dot))
      if dest_label in GD.graph.get('name', ''):
        print(GD.graph.get('name', ''))
        add_nodes_edges(node, GD)
  nx.drawing.nx_pydot.write_dot(GN, "./cg_out/TensorListScatter2.dot")

add_nodes_edges("Node1", G)

