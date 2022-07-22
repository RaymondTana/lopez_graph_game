import itertools

# returns all permutations on n elements
def permutations(n):
    return [list(tuple) for tuple in list(itertools.permutations([i for i in range(n)]))]