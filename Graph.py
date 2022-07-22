import numpy as np
from random import randint
from Permutations import permutations

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

    # output all "minors" (Graph objects) of a Graph up to permutations of vertices
    def get_minors(self):
        minors = []
        # minors come in two flavors:
        # 1. those obtained by removing a single vertex
        for v in range(self.n):
            m = self.get_minor_from_vertex(v)
            if not permutation_equivalence_found(m, minors):
                minors.append(m)
        # 2. those obtained by removing two adjacent vertices
        for u in range(self.n):
            for v in range(u + 1, self.n):
                # check that the edge is realized
                if(self.graph[u][v] == 1):
                    m = self.get_minor_from_adjacent(u, v)
                    if not permutation_equivalence_found(m, minors):
                        minors.append(m)
        return minors

    # True === Type I === I has a w.s.
    # False === Type II === II has a w.s.
    # Theorem: Type(G) iff there is a minor m of G with NOT(Type(m)). 
    def type(self):
        # the only two base cases
        if equal(self, V1) or equal(self, P2):
            return True
        # recursive step
        M = self.get_minors()
        for m in M:
            if not m.type():
                return True
        return False
    
    # True === Type I* === I has a w.s. in the * game
    # False === Type II* === II has a w.s. in the * game
    # Theorem: Type(G) iff there is a minor m of G with NOT(Type(m)).
    def stype(self):
        # the only two base cases
        if equal(self, V1): 
            return False
        if equal(self, P2):
            return True
        # recursive step
        M = self.get_minors()
        for m in M:
            if not m.stype():
                return True
        return False

    # return copied version of self
    def copy(self):
        return Graph(g = self.graph)

    def __str__(self):
        return str(self.graph)


# Standard base cases
V1 = Graph(g = [[0]])
P2 = Graph(g = [[0, 1], [1, 0]])

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
    # check of the same shape (always square matrices)
    if A.n == B.n:
        # list all permutations
        P = permutations(A.n)
        for p in P:
            A_p = permute_vertices(A, p)
            # if permuted A equals B, done
            if equal(A_p, B):
                return True
    return False

# return True iff G permutation equivalent to some element from H
def permutation_equivalence_found(G, H):
    for h in H:
        if permutation_equivalent(G, h):
            return True 
    return False

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