import numpy as np
def dijkstra_shortest_paths(adjacency_matrix_weighted, start_node, end_node):
    num_nodes = len(adjacency_matrix_weighted)
    visited = [False] * num_nodes
    shortest_distances = [float('inf')] * num_nodes
    shortest_distances[start_node] = 0
    num_shortest_paths = [0] * num_nodes
    num_shortest_paths[start_node] = 1
    previous_nodes = [[] for _ in range(num_nodes)]
    previous_nodes[start_node] = [start_node]

    for _ in range(num_nodes):
        min_distance = float('inf')
        current_node = -1
        for node in range(num_nodes):
            if not visited[node] and shortest_distances[node] < min_distance:
                min_distance = shortest_distances[node]
                current_node = node

        visited[current_node] = True
        for neighbor in range(num_nodes):
            if (adjacency_matrix_weighted[current_node][neighbor] > 0) and (not visited[neighbor]):
                total_distance = shortest_distances[current_node] + adjacency_matrix_weighted[current_node][neighbor]
                if total_distance < shortest_distances[neighbor]:
                    shortest_distances[neighbor] = total_distance
                    num_shortest_paths[neighbor] = num_shortest_paths[current_node]
                    previous_nodes[neighbor] = [current_node]
                elif total_distance == shortest_distances[neighbor]:
                    num_shortest_paths[neighbor] += num_shortest_paths[current_node]
                    previous_nodes[neighbor].append(current_node)

    shortest_paths = []
    find_paths(previous_nodes, end_node, [end_node], shortest_paths, start_node)
    
    return shortest_distances[end_node], num_shortest_paths[end_node], shortest_paths

def find_paths(previous_nodes, current_node, path, shortest_paths, start_node):
    if current_node == start_node:
        shortest_paths.append(list(reversed(path)))
    else:
        for prev_node in previous_nodes[current_node]:
            new_path = path.copy()
            new_path.append(prev_node)
            find_paths(previous_nodes, prev_node, new_path, shortest_paths, start_node)

def calculate_betweenness(adj_matrix):
    n = len(adj_matrix)
    betweenness = np.zeros_like(adj_matrix, dtype=float)
    for i in range(n):
        for j in range(i+1,n):
            if adj_matrix[i][j] != np.inf and i != j:
                shortest_distance, num_shortest_paths, shortest_paths = dijkstra_shortest_paths(adj_matrix, i, j)
                for path in shortest_paths:
                    for k in range(len(path)-1):
                        betweenness[path[k]][path[k+1]] += 1 / num_shortest_paths
                        betweenness[path[k+1]][path[k]] += 1 / num_shortest_paths

    return betweenness

def find_connected_components(adj_matrix):
    def dfs(node, visited, component):
        component.append(node)
        visited[node] = True
        for neighbor, is_connected in enumerate(adj_matrix[node]):
            if is_connected and not visited[neighbor]:
                dfs(neighbor, visited, component)

    num_nodes = adj_matrix.shape[0]
    visited = [False] * num_nodes
    components = []

    for node in range(num_nodes):
        if not visited[node]:
            component = []
            dfs(node, visited, component)
            components.append(component)

    return components

def elements_in_sublist(i, j, communities):
    for community in communities:
        if i in community or j in community:
            if i in community and j in community:
                return True
            break
    return False

def modularity(adj_org, adj_matrix):
    communities = find_connected_components(adj_matrix)
    m = np.sum(adj_org) / 2
    degrees = np.sum(adj_org, axis=1)
    Q = 0.0

    if m == 0:
        return 0, communities

    for community in communities:
        for i in community:
            for j in community:
                Aij = adj_org[i, j]
                ki = degrees[i]
                kj = degrees[j]
                Q += Aij - (ki * kj) / (2 * m)

    Q /= (2 * m)
    Q = np.round(Q, decimals=4)
    return Q, communities

edges = []
vertices = set()
edge = input().split()
while edge != []:
    edges.append(edge)
    vertices.add(int(edge[0]))
    vertices.add(int(edge[1]))
    edge = input().split()
feature_dict = {}
try:
    while 1:
        features = input().split()
        node = int(features.pop(0))
        if node not in vertices:
            vertices.add(node)
        feature_dict[node] = np.array(features, dtype=float)
except EOFError:
    pass
vertices = sorted(list(vertices))

num_vertices = len(vertices)
adj_matrix = np.zeros((num_vertices, num_vertices), dtype=float)

for edge in edges:
    v1 = vertices.index(int(edge[0]))
    v2 = vertices.index(int(edge[1]))
    adj_matrix[v1, v2] = 1
    adj_matrix[v2, v1] = 1

for i in range(num_vertices):
    for j in range(num_vertices):
        if adj_matrix[i][j] == 1:
            features_i = feature_dict[vertices[i]]
            features_j = feature_dict[vertices[j]]
            num_same = np.sum(features_i == features_j)
            adj_matrix[i][j] = len(features_i) - (num_same-1)
            adj_matrix[j][i] = len(features_i) - (num_same-1)

adj_zero = np.zeros((num_vertices, num_vertices), dtype=float)
mod_max = -10
adj_org = np.copy(adj_matrix)
while np.array_equal(adj_matrix, adj_zero) == False:
    mod, coms = modularity(adj_org, adj_matrix)
    if mod > mod_max:
        mod_max = mod
        communities = coms
    betweenness = calculate_betweenness(adj_matrix)
    max_betweenness = np.max(betweenness)
    indexes = np.argwhere(betweenness == max_betweenness)
    for index in indexes:
        adj_matrix[index[0]][index[1]] = 0
        adj_matrix[index[1]][index[0]] = 0
        if index[0] < index[1]:
            print(vertices[index[0]], vertices[index[1]])

mod, coms = modularity(adj_org, adj_matrix)
if mod > mod_max:
    mod_max = mod
    communities = coms
returnstr = ""
communities = sorted(communities, key=lambda x: (len(x), min(x)))
for component in communities:
    component.sort()
    for node in component:
        returnstr += str(vertices[node]) + "-"
    returnstr = returnstr[:-1]
    returnstr += " "
returnstr = returnstr[:-1]
print(returnstr)