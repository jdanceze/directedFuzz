import networkx as nx
import glob
import os

#callgraphs = glob.glob("./cg/*.dot")
callgraphs = glob.glob("/Users/jdanceze/Desktop/hub/tf_callgraph/*.dot")

for cg in callgraphs:
  G = nx.DiGraph(nx.drawing.nx_pydot.read_dot(cg))
  #if G.graph.get('name', '') == "TEST":
  if "TEST" in G.graph.get('name', ''):
    print("delete graph: " + cg)
    os.remove(cg)

