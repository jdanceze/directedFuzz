import json
import collections
import functools
import networkx as nx
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


@memoize
def find_out_edges_dest_label (node, graph):
  lable = [graph.nodes[e[1]].get('label', '') for e in graph.out_edges(node)]
  lable = [x.replace('"', '') for x in lable]
  return lable

def process_out_node(path):
  print("path: ",path)
  G = nx.DiGraph(nx.drawing.nx_pydot.read_dot(path))
  if path not in callgraphs.values():
    print("path not in callgraphs.values()")
    return None
  return list(callgraphs.keys())[list(callgraphs.values()).index(path)], find_out_edges_dest_label("Node1", G)
  

if __name__ == '__main__':
    
    start_time = time.time()
    keep_namespace = set()
    
    interface_namespace_paths = [v for k, v in callgraphs.items()]


    with concurrent.futures.ProcessPoolExecutor(max_workers=8) as executor:
        result = [x for x in executor.map(process_out_node, interface_namespace_paths) if x!=None]

    depth_1_dict = dict(result)

    with open('./temp/depth_1_dict.json', 'w') as fp:
        json.dump(depth_1_dict, fp)

    end_time = time.time()
    print("time: ", end_time - start_time)

