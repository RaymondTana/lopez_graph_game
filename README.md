# lopez_graph_game
Computing Lopez Type and *-Type for his Graph Games.

## Tool Introduction
This tool helps to compute the Lopez types of various graphs of relatively small size. The basic constructor for a `Graph` object works as follows: `class Graph.Graph(g: int[[]], n: int, e: int)`, with parameters
This tool helps to compute the Lopez types of various graphs of relatively small size. 

### Graph Class
The basic constructor for a `Graph` object works as follows: `class Graph.Graph(g: int[[]], n: int, e: int)`, with parameters
- `g` (`int[[]]`) _optional_: default `None`: specified index matrix for a graph. If `g` is specified, then `self.n` is computed from `g`.
- `n` (`int`) _optional_: default `1`: specified number of vertices in the graph
- `e` (`int`) _optional_: default `None`: specified number of edges to randomly add into the graph.
### Graph Wrappers
There are a few predefined `Graph` constructor wrappers:
- `Path(n: int)`: produce a path graph on $n$ vertices,
- `Complete(n: int)`: produce a complete graph on $n$ vertices,
- `Cycle(n: int)`: produce a cyclic graph on $n$ vertices.
There are also two pre-defined graphs: 
- `V1 = Graph(g = [[0]])`: the graph on 1 vertex with 0 edges,
- `P2 = Graph(g = [[0, 1], [1, 0]])`: the graph on 2 vertices with 1 edge.
### Computing Types
Given an instance `G` of the `Graph` class, one may compute its Lopez type by calling `G.type()` (with the encoding that `True` signifies Lopez type I, and `False` signifies Lopez type II). Similarly, one may compute the Lopez $\*$-type of `G` by calling `G.stype()` (with similar encoding).
## Mathematical Setting
A _Lopez graph game_ is a game held between two players on a given, undirected graph $G = (V, E)$. Players alternate making moves on $G$ and its resulting subgraphs until a winner is determined. A _move_ is defined as a player removing either:
- A single vertex $v \in V$ (and all edges $e \in E$ with $v \in e$), or
- Two adjacent vertices $u, v$ (and all edges $e \in E$ with $u \in e \lor v \in e$).
The resulting $G' = (V', E')$ is the subgraph of $G$ on which the next player must play.
In the *normal version* of the Lopez graph game, the last player to remove a vertex wins.
In the *adjoint version* (or $\*$ version) of the Lopez graph game, the last player to remove a vertex loses. 
In the normal (or adjoint) version, if Player I can guarantee a win no matter Player II's responses, we say that the graph $G$ on which they started play has *Lopez type I* (or *Lopez* $\*$*-type I*$^{\*}$, resp.). Otherwise, we say that $G$ has *Lopez type II* (or *Lopez* $\*$*-type II*$^{\*}$, resp.). 
## Dependencies
In order to make use of the `Graph` class, make sure your machine has access to a recent version of Python as well as the following Python dependencies:
- `numpy`,
- `random`,
- `itertools`.
## Future Directions
- Separate methods for _sparse_ index matrices (i.e., graphs with very few edges compared to the number of vertices)
- Display graph from index matrix,
- Further optimize type computations,
- Switch to modal form,
- Store a database of pre-computed "minors",
- More graph wrappers.
