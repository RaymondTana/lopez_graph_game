# lopez_graph_game
Computing Lopez type and $*$-type for Lopez graph games.

## Tool Introduction
This tool helps to compute the Lopez types of various graphs of relatively small size.

### (Optimized) Graph Class
The basic constructor for a `Graph` object works as follows: `class Class.Graph(g: int[[]], n: int, e: int)`, with parameters
- `g` (`int[[]]`) _optional_: default `None`: specified index matrix for a graph. If `g` is specified, then `self.n` is computed from `g`,
- `n` (`int`) _optional_: default `1`: specified number of vertices in the graph,
- `e` (`int`) _optional_: default `None`: specified number of edges to randomly add into the graph,

where `Class` comes from either class `Graph` or `Optimized_Graph`. 

The `Graph` class is a bare-bones version of the Lopez type calculator. For larger graphs, it may be more convenient to take advantage of pre-computed minors. The `Optimized_Graph` class was designed to make use of these pre-computed minors and store them for later use. The database has default directory `typed.txt`, and stores a representative of each pre-computed isomorphism class, where we judge isomorphism by permuting vertices and checking for graph-equivalence.

### Graph Wrappers
There are a few predefined `Graph` constructor wrappers:
- `Path(n: int)`: produce a path graph on $n$ vertices,
- `Complete(n: int)`: produce a complete graph on $n$ vertices,
- `Cycle(n: int)`: produce a cyclic graph on $n$ vertices.

There are also two pre-defined graphs: 
- `V1 = Graph(g = [[0]])`: the graph on 1 vertex with 0 edges,
- `P2 = Graph(g = [[0, 1], [1, 0]])`: the graph on 2 vertices with 1 edge.

### Computing Types
Given an instance `G` of the `Graph` (or `Optimized_Graph`) class, one may compute its Lopez types (type and $*$-type) by calling `G.types()` (where `True` encodes I and `False` encodes II), which outputs a dictionary `{'type': bool, 'stype': bool}`. One may specify which type to output by either reading the corresponding key from `G.types()` or by calling the method `G.type()` or `G.stype()`.

### Visualizing Graphs
Whether `G` is an instance of the `Graph` class or `Optimized_Graph` class, one may visualize `G` by either calling `print(G)` to see its index matrix representation or `G.visualize()` to get a `matplot.pyplot` output illustrating the graph. 

## Mathematical Setting
A _Lopez graph game_ is a game held between two players on a given, undirected graph $G = (V, E)$. Players alternate making moves on $G$ and its resulting subgraphs until a winner is determined. A _move_ is defined as a player removing either:
- A single vertex $v \in V$ (and all edges $e \in E$ with $v \in e$), or
- Two adjacent vertices $u, v$ (and all edges $e \in E$ with $u \in e \lor v \in e$).
- The resulting $G' = (V', E')$ is the subgraph of $G$ on which the next player must play.
- In the _normal version_ of the Lopez graph game, the last player to remove a vertex wins.
- In the _adjoint version_ (or $*$ version) of the Lopez graph game, the last player to remove a vertex loses. 
- In the normal (or adjoint) version, 
  - if Player I can guarantee a win no matter Player II's responses, we say that the graph $G$ on which they started play has _Lopez type I_ (or _Lopez_ $\ast$_-type I_$^{*}$, resp.). 
  - Otherwise, we say that $G$ has _Lopez type II_ (or _Lopez_ $\ast$_-type II_$^{*}$, resp.). 

## Dependencies
In order to make use of the `Graph` and `Optimized_Graph` classes, make sure your machine has access to a recent version of Python 3.0 as well as the following Python dependencies:
- `numpy`,
- `random`,
- `itertools`,
- `matplotlib.pyplot`,
- `networkx`.

## Future Directions
- Separate methods for _sparse_ index matrices (i.e., graphs with very few edges compared to the number of vertices)
- Further optimize type computations,
- Switch to modal form,
- More graph wrappers.
