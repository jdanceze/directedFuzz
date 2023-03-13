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

def get_target_namespace(target_path):
  with open(target_path) as f:
    return f.readline()

if __name__ == '__main__':
    
    
    SOURCE = "tensorflow::UnsortedSegmentJoinOp::Compute"
    #SOURCE = get_target_namespace("./temp/target_kernel_class.txt")
    TARGET = "tensorflow::TensorShapeBase::AddDim"
    CG = "./temp/cg_out/" + SOURCE + ".dot"
    #targets = ["tensorflow::anonymous_namespace\{py_func::cc\}::MakeArgTuple"]
    print ("Calculating distance..")

    G = nx.DiGraph(nx.drawing.nx_pydot.read_dot(CG))

    shortest_path = nx.dijkstra_path(G, SOURCE, TARGET)
    print("Shortest Path: ", shortest_path)
    print("Shortest Path Length: ", nx.dijkstra_path_length(G, SOURCE, TARGET))
    #write to file
    with open("./temp/shortest_path.txt", "w") as f:
        f.write(str(shortest_path))