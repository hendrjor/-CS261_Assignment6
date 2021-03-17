# Course: CS261 - Data Structures
# Author:
# Assignment:
# Description:

from collections import deque


class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """Adds a vertex to the directed graph"""
        self.v_count += 1
        v_count = self.v_count
        self.adj_matrix = [[0 for _ in range(v_count)] for _ in range(v_count)]
        return self.v_count

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """Adds weighted edges to the graph"""
        if weight < 0 or src == dst:
            return

        row_num = 0
        for row in self.adj_matrix:
            if src == row_num:
                if dst < len(row):
                    row[dst] = weight
            row_num += 1

    def remove_edge(self, src: int, dst: int) -> None:
        """Removes an edge from the directed graph"""
        row_num = 0
        if src < 0 or dst < 0:
            return
        for row in self.adj_matrix:
            if src == row_num:
                if dst < len(row):
                    row[dst] = 0
            row_num += 1

    def get_vertices(self) -> []:
        """Returns a list of vertices in the graph"""
        vertices = []
        for n in range(self.v_count):
            vertices.append(n)
        return vertices

    def get_edges(self) -> []:
        """Returns a list of edges in the graph"""
        edges = []
        row_num = 0
        for row in self.adj_matrix:
            column_num = 0
            for val in row:
                if val != 0:
                    edges.append((row_num, column_num, val))
                column_num += 1
            row_num += 1
        return edges

    def is_valid_path(self, path: []) -> bool:
        """Determines if the first and last vertex are connected in a path"""
        if not path:
            return True
        path_length = len(path)
        for i in range(path_length):
            row_index = path[i]
            if i == path_length - 1:
                return True
            column_index = path[i + 1]
            if self.adj_matrix[row_index][column_index] == 0:
                return False

    def dfs(self, v_start, v_end=None) -> []:
        """Return list of vertices visited during DFS search Vertices are picked in alphabetical order"""
        visited = []
        num_rows = len(self.adj_matrix)
        if v_start >= num_rows:
            return visited
        stack = deque()
        stack.append(v_start)  # adds first vertex to the end of the list

        while len(stack) != 0:
            vertex = stack.pop()
            if vertex == v_end:  # stops if the end vertex is reached
                visited.append(vertex)
                return visited

            if vertex not in visited:
                visited.append(vertex)

            next_vertices_temp = self.adj_matrix[vertex]
            next_vertices = []
            index = 0
            for x in next_vertices_temp:
                if x != 0:
                    next_vertices.append(index)  # appends the index to the next vertices list
                index += 1
            next_vertices.sort()  # sorts the next vertices list
            next_vertices.reverse()  # reverses the list

            for v in next_vertices:
                if v not in visited:
                    stack.append(v)
        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """Return list of vertices visited during DFS search Vertices are picked in alphabetical order"""
        visited = []
        num_rows = len(self.adj_matrix)
        if v_start >= num_rows:
            return visited
        que = deque()
        que.appendleft(v_start)  # adds the first vertex to the que

        while len(que) != 0:
            vertex = que.pop()
            if vertex == v_end:  # stops if the end vertex is reached
                visited.append(vertex)
                return visited

            if vertex not in visited:
                visited.append(vertex)
                next_vertices_temp = self.adj_matrix[vertex]
                next_vertices = []
                index = 0
                for x in next_vertices_temp:
                    if x != 0:
                        next_vertices.append(index)  # appends the index to the next vertices list
                    index += 1
                next_vertices.sort()  # sorts the next vertices list

                for v in next_vertices:
                    if v not in visited:
                        que.appendleft(v)
        return visited

    def has_cycle(self):
        """Determines if there is a cycle in the graph"""
        visited = [False for _ in range(self.v_count)]
        rec_stack = [False for _ in range(self.v_count)]

        for vertex in range(self.v_count):
            if visited[vertex] is False:
                if self.has_cycle_helper(vertex, visited, rec_stack):
                    return True
        return False

    def has_cycle_helper(self, vertex, visited, rec_stack):
        """Recursively determines if the node and its neighbors have been visited"""
        visited[vertex] = True
        rec_stack[vertex] = True

        neighbor_index = 0
        for neighbor in self.adj_matrix[vertex]:
            if visited[neighbor_index] is False and neighbor != 0:
                if self.has_cycle_helper(neighbor_index, visited, rec_stack):
                    return True
            elif rec_stack[neighbor_index] is True and neighbor != 0:
                return True
            neighbor_index += 1

        rec_stack[vertex] = False
        return False

    def dijkstra(self, src: int) -> []:
        """Implements dijkstra's algorithm to determine the cumulative distance to each vertex"""
        visited = dict()
        priority = deque()
        priority.append((src, 0))

        while len(priority) != 0:
            element = priority.popleft()
            vertex = element[0]
            distance = element[1]
            if vertex in visited and distance < visited[vertex]:  # determines if the path is less than the previous distance stored
                visited[vertex] = distance
            if vertex not in visited:
                visited[vertex] = distance
                next_vertices_temp = self.adj_matrix[vertex]
                next_vertices = []
                next_distances = []
                index = 0
                for dist in next_vertices_temp:
                    if dist != 0:
                        # if not next_vertices:
                        next_vertices.append(index)  # appends the index to the next vertices list
                        next_distances.append(dist)
                        # else:
                        #     z = 0
                        #     for v in next_distances:
                        #         if dist < v:
                        #             next_vertices.insert(z, index)
                        #             next_distances.insert(z, dist)
                        #             break
                        #         z += 1

                    index += 1
                # next_vertices.sort()  # sorts the next vertices list
                # print(next_distances)

                dist_index = 0
                for v in next_vertices:
                    v_distance = next_distances[dist_index]
                    next_element = (v, v_distance + distance)
                    priority.append(next_element)
                    dist_index += 1


        lengths = [float('inf') for _ in range(len(self.adj_matrix))]
        for val in visited:
            lengths[val] = visited[val]
        return lengths


if __name__ == '__main__':

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = DirectedGraph()
    # print(g)
    # for _ in range(5):
    #     g.add_vertex()
    # print(g)

    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # for src, dst, weight in edges:
    #     g.add_edge(src, dst, weight)
    # print(g)


    # print("\nPDF - method get_edges() example 1")
    # print("----------------------------------")
    # g = DirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # print(g.get_edges(), g.get_vertices(), sep='\n')


    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # print(g)
    # test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    # for path in test_cases:
    #     print(path, g.is_valid_path(path))


    # print("\nPDF - method dfs() and bfs() example 1")
    # print("--------------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # print(g)
    # for start in range(5):
    #     print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    # print("\nPDF - method has_cycle() example 1")
    # print("----------------------------------")
    # edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
    #          (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    # g = DirectedGraph(edges)
    # # print(g)
    #
    # edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    # for src, dst in edges_to_remove:
    #     g.remove_edge(src, dst)
    #
    #     print(g.get_edges(), g.has_cycle(), sep='\n')
    #
    # edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    # for src, dst in edges_to_add:
    #     g.add_edge(src, dst)
    #     print(g.get_edges(), g.has_cycle(), sep='\n')
    #     # print(g)
    # print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
