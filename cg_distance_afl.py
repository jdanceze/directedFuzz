import argparse
import collections
import functools
import networkx as nx


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
  return name

# Find the graph node for a name
@memoize
def find_nodes (name):
    n_name = node_name (name)
    #print(n_name)
    #get node id
    return [n for n, d in G.nodes(data=True) if n_name == n]

def distance (name):
  distance = -1
  for n in find_nodes (name):
    #print("node: ", n)
    d = 0.0
    i = 0
    for t in targets:
        #print("t: ", t)
        try:
            shortest = nx.dijkstra_path_length(G, n, t)
            print("n>>> " + n + " t>>> " + t)
            print("shortest: ", shortest)
            d += 1.0 / (1.0 + shortest)
            #d += 1.0 / (shortest)
            i += 1
            print("d: ", d)
        except nx.NetworkXNoPath:
            pass

    if d != 0 and (distance == -1 or distance > i / d) :
        distance = (i / d) - 1
        print("distance: ", distance)

  if distance != -1:
    out.write (name)
    out.write (",")
    out.write (str (distance))
    out.write ("\n")
    #return d

def get_target_namespace(target_path):
  with open(target_path) as f:
    return f.readline()

if __name__ == '__main__':
    
    
    SOURCE = "tensorflow::TensorListScatter::Compute"
    #SOURCE = get_target_namespace("./temp/target_kernel_class.txt")
    #TARGET = "tensorflow::Variant::get"
    #CG = "./temp/cg_out/" + SOURCE + ".dot"
    CG = "./cg_out/cg_out_TensorListScatter.dot"
    targets = ["tensorflow::Tensor::CheckIsAlignedAndSingleElement"]
    print ("Calculating distance..")

    G = nx.DiGraph(nx.drawing.nx_pydot.read_dot(CG))
    #print(distance("tensorflow::TensorListScatter::Compute"))
    
    # with open("./distance/distance_Scatter.txt", "w") as out:
    #     distance("tensorflow::TensorListScatter::Compute")

    with open("./distance/distance.txt", "w") as out:
        for n in G.nodes:
            distance(n)


    # print("Shortest Path: ", nx.dijkstra_path(G, SOURCE, TARGET))
    # print("Shortest Path Length: ", nx.dijkstra_path_length(G, SOURCE, TARGET))