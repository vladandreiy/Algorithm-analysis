import sys

from itertools import combinations


# Prints to stdout a logical sentence representing the transformation of K-Vertex Cover to SAT
def k_clause(k, n, m, graph):
    sat_sentence = ""

    # Add edges to sat_sentence
    for i in range(0, m):
        clause = ""
        # For a given edge (u,v), the clause will be (k*u-j V k*v-j)
        # Each node is being represented by literals k*u-j
        for j in range(0, k):
            clause += str(k * int(graph[i][0]) - j) + "V" + str(k * int(graph[i][1]) - j) + "V"
        clause = clause[:-1]
        sat_sentence += "(" + clause + ")^"

    # Add restriction so that only k literals are true (only k nodes are true)
    for i in range(0, k):
        # Generate list with 1 literal from each node
        nodes_literals = []
        for j in range(1, n + 1):
            nodes_literals.append(k * j - i)
        # Add a clause to sat_sentence to make sure at least 1 literal is true
        clause = ""
        for j in nodes_literals:
            clause += str(j) + "V"
        clause = clause[:-1]
        sat_sentence += "(" + clause + ")^"
        # Add all combinations of 2 literals from the list to sat_sentence
        # In order to make sure no more than 1 literal for each node is true
        node_combinations = combinations(nodes_literals, 2)
        for j in list(node_combinations):
            sat_sentence += "(~" + str(j[0]) + "V~" + str(j[1]) + ")^"

    # Add restriction so that for every node, only one of its literals is true
    for i in range(1, n + 1):
        # Generate list with all literals from one node
        node_literals = []
        for j in range(0, k):
            node_literals.append(k * i - j)
        # Add all combinations of 2 literals in the list to the sat_sentence
        # In order to be sure no more than 1 literal from each node is true
        literal_combinations = combinations(node_literals, 2)
        for j in list(literal_combinations):
            sat_sentence += "(~" + str(j[0]) + "V~" + str(j[1]) + ")^"
    sat_sentence = sat_sentence[:-1]

    print(sat_sentence)


if __name__ == '__main__':
    K = int(sys.stdin.readline())
    N = int(sys.stdin.readline())
    M = int(sys.stdin.readline())
    G = []
    # Graph is represented as a list of edges, an edge is represented by a list of 2 elements
    for _ in range(0, M):
        G.append(sys.stdin.readline().split())
    k_clause(K, N, M, G)
