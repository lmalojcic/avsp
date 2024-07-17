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

def preprocess():
    nearest_black = {}
    for node in range(n):
        if graph[node][0]:  # If the node is black
            nearest_black[node] = 0
            queue = deque([(node, 0)])  # (node, distance)
            visited = set([node])
            while queue:
                current_node, distance = queue.popleft()
                for neighbor in graph[current_node][1]:
                    if neighbor not in visited:
                        queue.append((neighbor, distance + 1))
                        visited.add(neighbor)
                        if neighbor not in nearest_black or distance + 1 < nearest_black[neighbor]:
                            nearest_black[neighbor] = distance + 1
    return nearest_black

nearest_black = preprocess()

for node in range(n):
    if node in nearest_black:
        print(node, nearest_black[node])
    else:
        print(-1, -1)
