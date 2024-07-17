from heapq import heappush, heappop

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


def dijkstra(start):
    distance = [float('inf')] * n
    distance[start] = 0
    min_heap = [(0, start)]  # (distance, node)

    while min_heap:
        dist, node = heappop(min_heap)
        if dist > distance[node]:
            continue
        for neighbor in graph[node][1]:
            weight = 1  # Assuming all edges have unit weight
            if graph[neighbor][0]:  # If the neighbor is black
                if dist + weight < distance[neighbor]:
                    distance[neighbor] = dist + weight
            elif dist + weight < distance[neighbor]:
                distance[neighbor] = dist + weight
                heappush(min_heap, (distance[neighbor], neighbor))

    return distance


for node in range(n):
    distances = dijkstra(node)
    min_distance = float('inf')
    nearest_black = -1
    for i, dist in enumerate(distances):
        if graph[i][0] and dist < min_distance:
            min_distance = dist
            nearest_black = i
    if min_distance == float('inf'):
        print(-1, -1)
    else:
        print(nearest_black, min_distance)
