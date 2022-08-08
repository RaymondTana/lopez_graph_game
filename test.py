import Graph
import Optimized_Graph

import numpy as np
np.set_printoptions(formatter={'all':lambda x: str(int(x))})

# 'I' == True, 'II' == False
typemap = lambda type: 'I' if type else 'II'

# First Example
print("Example 1:")
N = 8
G = Graph.Cycle(n = N)
print(f"Consider the cycle graph C_{N}")
print(G)
G.visualize()
types = G.types()
type = typemap(types['type'])
stype = typemap(types['stype'])
print(f"C_{N} has Lopez types {type} and {stype}*")

print("\nExample 2: Graph vs. Optimized_Graph Classes\n")
print("2.a: Non-Optimized Graph Class")
for n in range(0, 9):
    Pn = Graph.Path(n)
    types = Pn.types()
    type = typemap(types['type'])
    stype = typemap(types['stype'])
    print(f"P_{n} has Lopez types {type} and {stype}*")

print("\n2.b: Optimized_Graph Class")
for n in range(0, 9):
    Pn = Optimized_Graph.Path(n)
    types = Pn.types()
    type = typemap(types['type'])
    stype = typemap(types['stype'])
    print(f"P_{n} has Lopez types {type} and {stype}*")

print("\nExample 3: Sanity Check on Complete Graphs")
print("We claimed that K_n is")
print("\tLopez type II  iff n == 0 mod 3")
print("\tLopez *-type II* iff n == 1 mod 3")
print("Let's check some values of n")
Optimized_Graph.read_typed()
print("Read in any pre-computed minors from the database `typed.txt`")
for n in range(1, 10):
    K = Optimized_Graph.Complete(n)
    types = K.types()
    type = types['type']
    stype = types['stype']
    m = n % 3
    predicted_type = m % 3 != 0
    predicted_stype = m % 3 != 1
    match_type = type == predicted_type
    match_stype = stype == predicted_stype
    smiley_face = lambda match: ":)" if match else ":("
    print(f"n = {n} === {m} mod 3:\ttype(K_{n}) = {typemap(type)} {smiley_face(match_type)} \t*-type(K_{n}) = {typemap(stype)}* {smiley_face(match_stype)}")
Optimized_Graph.write_typed()
print("Committed all minors involved in these computations to `typed.txt`")