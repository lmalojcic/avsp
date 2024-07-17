from collections import deque

(n, e) = input().split()
n = int(n)
e = int(e)

graph = {}

for i in range(n):
    x = input()
    if x == '0':
        graph[i] = [False, []]
    else:
        graph[i] = [True, []]

for i in range(e):
    (a, b) = input().split()
    a = int(a)
    b = int(b)
    graph[a][1].append(b)
    graph[b][1].append(a)

def bfs(node):
    visited = set()
    distance = [0] * n
    queue = deque()
    queue.append(node)
    visited.add(node)
    while queue:
        current_node = queue.popleft()
        for neighbor in graph[current_node][1]:
            if graph[neighbor][0]:  # If the neighbor is black
                return neighbor, distance[current_node] + 1
            if neighbor not in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                distance[neighbor] = distance[current_node] + 1
    return -1, -1  # If no black node found

for node in range(n):
    nearest_black, distance_to_black = bfs(node)
    print(nearest_black, distance_to_black)
