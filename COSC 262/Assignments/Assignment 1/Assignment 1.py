"""Assignment 1"""
"""Part 1"""


"""Adjacency List"""


def adjacency_list(graph_str):
    """Converts strings to adjacency lists"""
    split_list = [i.split() for i in graph_str.splitlines()]
    vertex_list = [[] for _ in range(int(split_list[0][1]))]
    for edge in split_list[1:]:
        if len(edge) <= 2:
            'If graph has weight'
            vertex_list[int(edge[0])].append((int(edge[1]), None))
            if split_list[0][0] == 'U':
                vertex_list[int(edge[1])].append((int(edge[0]), None))
        else:
            'If graph doesnt have weight'
            vertex_list[int(edge[0])].append((int(edge[1]), int(edge[2])))
            if split_list[0][0] == 'U':
                vertex_list[int(edge[1])].append((int(edge[0]), int(edge[2])))
    return vertex_list


"""DFS Search"""


def dfs_tree(adj_list, start, visited, paths):
    """Recursive DFS Search"""
    for child in adj_list[start]:
        if visited[child[0]] == "U":
            visited[child[0]] = "D"
            dfs_tree(adj_list, child[0], visited, paths)
        elif visited[child[0]] == "D":
            paths.append(None)
    visited[start] = "P"
    paths.insert(0, start)
    return paths


"""Checklist"""


def checklist(conditions):
    """Checks for cycles and orders items"""
    adj_list = adjacency_list(conditions)
    visited, paths, checklist = ["U" for _ in range(len(adj_list))], [], []
    for child in range(len(adj_list)):
        if visited[child] == "U":
            visited[child] = "D"
            checklist = dfs_tree(adj_list, child, visited, paths)
    if None in checklist:
        checklist = None
    return checklist


"""Assignment 1"""
"""Part 2"""


"""BFS Function"""


def bfs_tree(adj_list, start, visited):
    """This is the BFS function"""
    queue, path = [start], [start]
    while queue:
        # Run until queue is empty
        current = queue.pop()
        for child in adj_list[current]:
            if not visited[child[0]]:
                # For each (Vertex, Weight) add vertex to visited
                visited[child[0]] = True
                queue.insert(0, child[0])
                if child[0] != start:
                    path.append(child[0])
    return path


"""Safe Road Finder"""


def possible_locations(safe_map):
    """Finds safe roads in a map"""
    adj_list = adjacency_list(safe_map)
    visited, output = [False for _ in range(0, len(adj_list))], []
    for vertex in range(0, len(adj_list)):
        if not visited[vertex]:
            output.append(bfs_tree(adj_list, vertex, visited))
    return output


"""Assignment 1"""
"""Part 3"""


"""Next Vertex"""


def next_vertex(in_tree, distance):
    """Finds next vertex"""
    tree_tuple = [(distance[i], i) for i in range(0, len(in_tree)) if in_tree[i] is False]
    return (sorted(tree_tuple, key=lambda x: x[0]))[0][1]


"""Dijkstra's Search"""


def dijkstra_tree(adj_list, start):
    """Uses the Dijkstra's algorithm to search"""
    visited, distance, parent = [False for _ in range(len(adj_list))], [float('inf') for _ in range(len(adj_list))], \
                                [None for _ in range(len(adj_list))]
    distance[start] = 0
    while not all(visited):
        next_vert = next_vertex(visited, distance)
        visited[next_vert] = True
        for vertex, time in adj_list[next_vert]:
            if (not visited[vertex]) and (distance[next_vert] + time < distance[vertex]):
                distance[vertex] = distance[next_vert] + time
                parent[vertex] = next_vert
    return parent, distance


"""Longest Path Finder"""


def longest_path(city_map, position):
    """Finds a reachable path which is the longest path"""
    adj_list = adjacency_list(city_map)
    parent, distance = dijkstra_tree(adj_list, position)
    # Sorts the distance by the weight of the vertex
    distance = [(i, distance[i]) for i in range(len(distance)) if distance[i] != float('inf')]
    distance = [i for i in sorted(distance, key=lambda x: x[1])]
    path = [distance[-1][0]]
    while path[0] != position:
        path.insert(0, parent[path[0]])
    return path



city_map = """\
U 4 W
0 2 5
0 3 2
3 2 2
"""
# print(dijkstra_tree(adjacency_list(city_map), 0))
print(longest_path(city_map, 0))
print(longest_path(city_map, 1))
print(longest_path(city_map, 2))
print(longest_path(city_map, 3) in [[3, 0], [3, 2]])

