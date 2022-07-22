import numpy as np
from Graph import *
np.set_printoptions(formatter={'all':lambda x: str(int(x))})
from Permutations import permutations

# Translating True == I, False == II
def word(type):
    return "I" if type else "II"
def match(b):
    return "\t:)" if b else "\t:("

print("Sanity check: complete graphs")
print("A complete graph is a graph where all possible edges are realized")
print("We represent a graph by its incidence matrix, e.g., the complete graph K_6:")
print(Complete(n = 6))
print("We claimed that K_n is")
print("\tII  iff n == 0 mod 3")
print("\tII* iff n == 1 mod 3")
print("Let's check some values of n")
for n in range(1, 11):
    K = Complete(n)
    type = K.type()
    stype = K.stype()
    m = n % 3
    predicted_type = m % 3 != 0
    predicted_stype = m % 3 != 1
    match_type = type == predicted_type
    match_stype = stype == predicted_stype
    print("n = " + str(n) + " === " + str(m) + " mod 3:\tType(K_" + str(n) + ") = " + word(type) + match(match_type) + ",\t*-Type(K_" + str(n) + ") = " + word(stype) + "*" + match(match_stype))