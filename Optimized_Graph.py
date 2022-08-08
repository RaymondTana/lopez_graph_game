import numpy as np
from random import randint
from Permutations import permutations
np.set_printoptions(formatter={'all':lambda x: str(int(x))})
import os.path

# for visualization
import networkx as nx
import matplotlib.pyplot as plt

typed_filepath = "typed.txt"

class Graph:
    def __init__(self, g = None, n = 1, e = None):
        if g is None:
            self.n = n
            self.graph = np.empty((self.n, self.n))

            # initialize values
            for i in range(self.n):
                for j in range(self.n):
                    self.graph[i][j] = 0

            # when number of random edges is specified and is appropriate
            if e is not None and e <= self.n * (self.n - 1) and e >= 0:
                count = 0
                while(count < e):
                    # produce random position
                    x = randint(0, self.n - 1)
                    y = randint(0, self.n - 1)
                    # check not already added into the edge relation / along diagonal
                    if(x != y and self.graph[x][y] == 0):
                        # add this edge into the edge relation, reflexively
                        self.graph[x][y] = 1
                        self.graph[y][x] = 1
                        count += 1
        else:
            # define based on g
            self.graph = np.copy(g)
            self.n = len(g)
    
    # list of minors already seen *and* computed
    #   intended structure {n <int>: {k <int>: { G: <Graph> , type: <Bool>, stype: <Bool> }}}
    ya = {}

    # return number of edges in the graph
    def get_e(self):
        e = 0
        for i in range(self.n):
            for j in range(i + 1, self.n):
                e += self.graph[i][j]
        return int(e)

    # return a copied graph with eliminated vertex
    def elim_vertices_copy(self, V):
        # first, make sure they're in a good ordering (descending)
        V.sort(reverse=True)
        g = np.copy(self.graph)
        for v in V:
            g = np.delete(g, obj=v, axis=0)
            g = np.delete(g, obj=v, axis=1)
        return g

    # return minor obtained by removing vertex
    def get_minor_from_vertex(self, v):
        return Graph(self.elim_vertices_copy([v]))

    # return minor obtained by removing an adjacent pair
    def get_minor_from_adjacent(self, u, v):
        return Graph(self.elim_vertices_copy([u, v]))

    # returns the minors
    # no checking for repeats happens here anymore
    def get_minors(self):
        minors = []
        # minors come in two flavors:
        # 1. those obtained by removing a single vertex
        for v in range(self.n):
            m = self.get_minor_from_vertex(v)
            # we are adding a lot of minors here
            minors.append(m)
        # 2. those obtained by removing two adjacent vertices
        for u in range(self.n):
            for v in range(u + 1, self.n):
                # check that the edge is realized
                if(self.graph[u][v] == 1):
                    m = self.get_minor_from_adjacent(u, v)
                    minors.append(m)
        return minors

    # return i-th minor Graph instances of Graph instance
    def get_minor(self, i):
        # in this case, i is treated as the vertex to remove
        if i < self.n:
            return self.get_minor_from_vertex(i)
        # in this case i >= n, we take the (i - n)-th pair (u, v) to remove from graph
        else:
            u = int((i - self.n) / self.n)
            v = (i - self.n) % self.n
            if u > v and self.graph[u][v] == 1:
                return self.get_minor_from_adjacent(u, v)
            else:
                return None

    # return the Lopez types of Graph instance as dict
    def types(self):
        # Step 0: check if equal to either base case
        if equal(self, V1):
            return {'type': True, 'stype': False}
        if equal(self, P2):
            return {'type': True, 'stype': True}

        # Step 1: check if self has been seen
        n = self.n
        e = self.get_e()
        query = buscar_match(self, n, e)
        if query:
            return query

        # Step 2: M not seen, so recurse on minors
        
        settled_type = False
        settled_stype = False
        
        # 2.a: List all minors upfront
        # M = self.get_minors()
        # for m in M:
        #     m_types = m.types()
        #     # maybe we can determine types early
        #     if not m_types['type'] and not settled_type:
        #         settled_type = True
        #     if not m_types['stype'] and not settled_stype:
        #         settled_stype = True
        #     # we (only) may terminate early if both types are settled as True
        #     if settled_type and settled_stype:
        #         break

        # 2.b Enumerate through the minors
        for i in range(self.n + self.n * self.n):
            m = self.get_minor(i)
            if m is not None:
                m_types = m.types()
                # maybe we can determine type/stype early
                if not m_types['type'] and not settled_type:
                    settled_type = True
                if not m_types['stype'] and not settled_stype:
                    settled_stype = True
                # we (only) may terminate early if both types are settled as True
                if settled_type and settled_stype:
                    break

        # Step 3: register self into Graph.ya
        if not n in Graph.ya:
            Graph.ya[n] = {}
        if not e in Graph.ya[n]:
            Graph.ya[n][e] = []
        result = {
            "graph": self,
            "types": {
                "type": settled_type,
                "stype": settled_stype,
            }
        }
        Graph.ya[n][e].append(result)
        return result['types']

    # return type
    def type(self):
        return self.types()['type']
    
    # return stype
    def stype(self):
        return self.types()['stype']

    # convert to line in database
    def to_line(self):
        line = ""
        for i in range(self.n):
            for j in range(i + 1, self.n):
                line += str(int(self.graph[i][j]))
        return line

    def copy(self):
        return Graph(g = self.graph)

    def __str__(self):
        return str(self.graph)

    def visualize(self):
        visual = []
        # add the edges to the visual first
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.graph[i][j] == 1:
                    visual.append([i, j])
        G = nx.Graph()
        G.add_edges_from(visual)
        nx.draw_networkx(G)
        plt.show()

# return a copy of a Graph with permuted vertices
# p: a permutation on n: p = [p(0), p(1), ..., p(n-1)]
def permute_vertices(G, p):
    g = np.copy(G.graph)
    id = [i for i in range(G.n)]
    g[id, :] = g[p, :]
    g[:, id] = g[:, p]
    return Graph(g = g)

# predicate whether A is equal to B as graphs
def equal(A, B):
    return np.array_equal(A.graph, B.graph)

# predicate whether A is permutation-equivalent to B,
# i.e., does there exist a permutation mapping A to B?
# A and B are both Graph objects
def permutation_equivalent(A, B):
    if(A.n == B.n):
        # list all permutations
        P = permutations(A.n)
        for p in P:
            A_p = permute_vertices(A, p)
            # if permuted A equals B, done
            if equal(A_p, B):
                return True
    return False

# search for a match in Graph.ya for graph G
def buscar_match(G, n, e): 
    # location in Graph.ya determined by n, e
    if n is None:
        n = G.n
    if e is None:
        e = G.get_e()

    # if Graph.ya has seen something of this shape before
    if n in Graph.ya and e in Graph.ya[n]:
        # list of potential matches of same #vertices and #edges
        Y = Graph.ya[n][e]
        for y in Y:
            if permutation_equivalent(G, y['graph']):
                return y['types']
    return None

# Standard base cases
V1 = Graph(g = [[0]])
P2 = Graph(g = [[0, 1], [1, 0]])

# return path graph on n vertices
def Path(n):
    G = Graph(n = n)
    for i in range(n - 1):
        G.graph[i][i + 1] = 1
        G.graph[i + 1][i] = 1
    return G

# return complete graph on n vertices
def Complete(n):
    G = Graph(n = n)
    for i in range(n):
        for j in range(i + 1, n):
            G.graph[i][j] = 1
            G.graph[j][i] = 1
    return G

# returns cyclic graph on n vertices
def Cycle(n):
    G = Path(n = n)
    G.graph[0][n - 1] = 1
    G.graph[n - 1][0] = 1
    return G

# convert a line in database to entry in Graph.ya
def line_to_graph(line):
    delimited = line.split(',')
    try:
        graph_line = delimited[0]
        type = delimited[1] == '1'
        stype = delimited[2] == '1'

        n = int((1 + np.sqrt(1 + 8 * len(graph_line))) / 2)
        e = graph_line.count('1')
        g = [None] * n
        for i in range(n):
            g[i] = [None] * n
        k = 0
        for i in range(n):
            g[i][i] = 0
            for j in range(i + 1, n):
                # k = int(j - i - 1 + (2 * n - i - 1) * i / 2)
                g[i][j] = int(graph_line[k])
                g[j][i] = int(graph_line[k])
                k += 1
        return { 'typed': { 'graph': Graph(g = g), 'types': {'type': type, 'stype': stype} }, 'n': n, 'e': e }
    except IndexError:
        return None
    
    return None

def typed_to_line(D):
    G = D['graph']
    type = D['types']['type']
    stype = D['types']['stype']
    # Type I === True === 1, Type II === False === 0
    typemap = lambda type: 1 if type else 0
    return f"{G.to_line()},{typemap(type)},{typemap(stype)}"

# read database into Graph.ya
def read_typed(filepath = typed_filepath):
    Graph.ya = {}
    if os.path.isfile(filepath):
        with open(filepath, 'r') as f:
            for line in f:
                result = line_to_graph(line) # === { 'typed': { 'graph': Graph, 'types': {'type': Bool, 'stype': Bool} }, 'n': int, 'e': int }
                # print("result['n']", result['n'])
                if result is not None:
                    if not result['n'] in Graph.ya:
                        Graph.ya[result['n']] = {}
                    if not result['e'] in Graph.ya[result['n']]:
                        Graph.ya[result['n']][result['e']] = []
                    Graph.ya[result['n']][result['e']].append(result['typed'])
        print("read", filepath)
    else:
        print("no database yet")

# # write Graph.ya into database
def write_typed(filepath = typed_filepath):
    with open(filepath, 'w') as database:
        for n in Graph.ya:
            for e in Graph.ya[n]:
                for D in Graph.ya[n][e]:
                    database.write(typed_to_line(D) + '\n')
        database.close()
    print("wrote to", filepath)