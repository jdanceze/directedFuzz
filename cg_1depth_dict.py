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

target_namespace = "tensorflow::Tensor::scalar"
    
with open('./temp/callgraphs_dict.json') as json_file:
  callgraphs = json.load(json_file)


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

#find parent node
def find_parent_node (node, graph):
  return [e[0] for e in graph.in_edges(node)]

#find parent node and keep only the label
def find_parent_node_label (node):
  return [G.nodes[e[0]].get('label', '') for e in G.in_edges(node)]

#recursive function to find the origin node of a node
def find_origin_node (node):
  parent = find_parent_node(node)
  if parent:
    return find_origin_node(parent[0])
  else:
    return node
  
#recursive function to find the origin node of a node and keep only the label
def find_origin_node_label (node, graph):
  parent = find_parent_node(node, graph)
  if parent:
    return find_origin_node_label(parent[0], graph)
  else:
    return graph.nodes[node].get('label', '')

#find parent node from label
def find_parent_node_from_label (label):
  return [e[0] for e in G.in_edges(label)]

#find all incoming edges for node and keep only the destination node label
def find_in_edges_dest_label (node, graph):
  lable = [graph.nodes[e[0]].get('label', '') for e in graph.in_edges(node)]
  lable = [x.replace('"', '') for x in lable]
  return lable

#find all incoming edges for label and keep only the destination node label
def find_in_edges_dest_label_from_label (label, graph):
  lable = [graph.nodes[e[0]].get('label', '') for e in graph.in_edges(label)]
  lable = [x.replace('"', '') for x in lable]
  return lable

#find all out going edges for node
def find_out_edges (node):
  return [e for e in G.out_edges(node)]

#find all out going edges for node and keep only the destination node
def find_out_edges_dest (node):
  return [e[1] for e in G.out_edges(node)]

#find all out going edges for node and keep only the destination node label
def find_out_edges_dest_label (node, graph):
  lable = [graph.nodes[e[1]].get('label', '') for e in graph.out_edges(node)]
  lable = [x.replace('"', '') for x in lable]
  return lable

#return node label
def get_node_label (node, graph):
  label = graph.nodes[node].get('label', '')
  #label = label.replace('"', '')
  return label

#get node from label
def get_node_from_label (label, graph):
  node = [n for n, d in graph.nodes(data=True) if label in d.get('label', '')]
  return node


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

def process_out_node(path):
  print("path: ",path)
  G = nx.DiGraph(nx.drawing.nx_pydot.read_dot(path))
  # if target_namespace in find_out_edges_dest_label("Node1", G):
  #   return get_node_label("Node1", G)
  #get key from value callgraphs dict
  if path not in callgraphs.values():
    print("path not in callgraphs.values()")
    return None
  return list(callgraphs.keys())[list(callgraphs.values()).index(path)], find_out_edges_dest_label("Node1", G)
  
  # node = get_node_from_label(target_namespace, G)
  # if len(node) != 0:
      
        
  #   # if G.graph.get('name', '') == target_namespace:
  #   #   continue
  #   print("node: ", node)
  #   print("original node label: ",find_origin_node_label(node, G))
  #   return find_origin_node_label(node, G)


#recursive function to add nodes and edges to graph

def add_nodes_edges(node, GT, name):
  count = 0
  for dest_label in find_out_edges_dest_label(node, GT):
    new_dest_label = '"' + dest_label + '"'
    if get_node_label(node, GT) == new_dest_label and count == 0:
      GN.add_edge(get_node_label(node, GT), new_dest_label)
      count+=1
    else:
      GN.add_edge(get_node_label(node, GT), new_dest_label)
      #id dest_label contain backslash then remove it
      if '\\' in dest_label:
        dest_label = dest_label.replace('\\', '')

      if dest_label in callgraphs:
        dot = callgraphs[dest_label]
        GD = nx.DiGraph(nx.drawing.nx_pydot.read_dot(dot))
        print("Joining: ", GD.graph.get('name', ''))
        add_nodes_edges(node, GD, name)
  nx.drawing.nx_pydot.write_dot(GN, "./temp/cg_out/" + name + ".dot")
  #nx.drawing.nx_pydot.write_dot(GN, "./cg_out/cg.dot")


def get_target_namespace(target_path):
  with open(target_path) as f:
    return f.readline()

  

if __name__ == '__main__':
    
    start_time = time.time()
    keep_namespace = set()
    
    #interface_namespace_paths = [v for k, v in callgraphs.items() if "Compute" in k]
    #interface_namespace_paths = [v for k, v in callgraphs.items() if "Compute" not in k and k!=target_namespace ]
    interface_namespace_paths = [v for k, v in callgraphs.items()]
    #interface_namespace_paths = ["/Users/jdanceze/Desktop/hub/tf_callgraph/classtensorflow_1_1Tensor_af36b0667149599e4b47d8207330c5a59_cgraph.dot","/Users/jdanceze/Desktop/hub/tf_callgraph/classtensorflow_1_1Tensor_ae0135f94822a26ad9fee6f261db8b500_cgraph.dot","/Users/jdanceze/Desktop/hub/tf_callgraph/classtensorflow_1_1TensorMapStackKeys_ae344130a499966328fecce5a7ac22de8_cgraph.dot","/Users/jdanceze/Desktop/hub/tf_callgraph/c_2c__api_8cc_a21dbe3606686b4489d7af8bfca76856d_cgraph.dot", "/Users/jdanceze/Desktop/hub/tf_callgraph/classtensorflow_1_1tpu_1_1TpuCompileSucceededAssertOp_ac6fea6228d5aa735108bbf0cf5628e30_cgraph.dot"]

    #print("Interface Namespace Paths: ", interface_namespace_paths)

    # for path in interface_namespace_paths:
    #   G = nx.DiGraph(nx.drawing.nx_pydot.read_dot(path))
    #   #G = nx.DiGraph(nx.drawing.nx_pydot.read_dot(interface_namespace_paths[0]))
    #   print("path: ",path)
    #   node = get_node_from_label(target_namespace, G)
    #   if len(node) == 0:
    #     continue
      
    #   if G.graph.get('name', '') == target_namespace:
    #     continue
    #   print("node: ", node)
    #   print("original node label: ",find_origin_node_label(node))
    #   keep_namespace.add(find_origin_node_label(node))
    #   print(keep_namespace)


    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        result = [x for x in executor.map(process_out_node, interface_namespace_paths) if x!=None]

    depth_1_dict = dict(result)

    with open('./temp/depth_1_dict.json', 'w') as fp:
        json.dump(depth_1_dict, fp)

    end_time = time.time()
    print("time: ", end_time - start_time)
    # #write keep_namespace to file
    # with open('./temp/keep_namespace.txt', 'w') as f:
    #   #f.write(str(keep_namespace))
    #   f.write(str(result))

