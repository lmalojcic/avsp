import numpy as np
from collections import defaultdict
from scipy.sparse import lil_matrix


def noderank(node, iteration, beta, graph, out_degree):
    n = len(graph)
    rank_vector = np.ones(n) / n
    teleport_prob = (1 - beta) / n

    # Construct the sparse transition matrix
    transition_matrix = lil_matrix((n, n))
    for i, neighbors in graph.items():
        if out_degree[i] == 0:
            transition_matrix[:, i] = teleport_prob
        else:
            for neighbor in neighbors:
                transition_matrix[neighbor, i] = beta / out_degree[i]

    # Convert to CSR format for efficient matrix-vector multiplication
    transition_matrix = transition_matrix.tocsr()

    for _ in range(iteration):
        rank_vector = transition_matrix.dot(rank_vector) + teleport_prob

    return f"{rank_vector[node]:.10f}"


(n, b) = input().split()
n = int(n)
b = float(b)

graph_dict = defaultdict(list)
out_degree = np.zeros(n)

for i in range(n):
    temp = list(map(int, input().split()))
    graph_dict[i] = temp
    out_degree[i] = len(temp)

q = int(input())

for i in range(q):
    query = list(map(int, input().split()))
    n = query[0]
    t = query[1]
    print(noderank(n, t, b, graph_dict, out_degree))
