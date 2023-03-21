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
    return self._func.__doc__

  def __get__(self, obj, objtype):
    return functools.partial(self.__call__, obj)

def process_dot(dot):
    graph_name = nx.drawing.nx_pydot.read_dot(dot).graph.get('name', '')
    print("Add to dict: ",graph_name)
    return graph_name, dot



if __name__ == '__main__':
    
    print("Adding graph name and file name to dict")
    print("++++++++++++++")

    GN = nx.DiGraph()
    start_time = time.time()
    
    callgraphs = glob.glob("/Users/jdanceze/Desktop/hub/tf_callgraph/*.dot")
    #callgraphs = glob.glob("./cg/*.dot")
    num_processes = 8

    with concurrent.futures.ProcessPoolExecutor(max_workers=num_processes) as executor:
        result = [x for x in executor.map(process_dot, callgraphs)]
    
    callgraphs = dict(result)

    with open('./temp/callgraphs_dict.json', 'w') as fp:
        json.dump(callgraphs, fp)

    end_time = time.time()
    print("time: ", end_time - start_time)


