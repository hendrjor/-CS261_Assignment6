# Course: 
# Author: 
# Assignment: 
# Description:

from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """Adds a new vertex to the graph"""
        if v not in self.adj_list:
            self.adj_list[v] = []

    def add_edge(self, u: str, v: str) -> None:
        """Adds a new edge to the graph"""
        if u == v:
            return
        if v in self.adj_list and u in self.adj_list:  # if both keys are in the dictionary
            u_list = self.adj_list[u]
            in_v = False
            for value in u_list:  # determines if the edge already exists
                if value == v:
                    in_v = True
            if in_v is False:  # if the edge does not exist, then add the edge
                self.adj_list[v].append(u)
                self.adj_list[u].append(v)
            else:
                return

        elif v in self.adj_list and u not in self.adj_list:  # if v is in the dictionary
            self.adj_list[v].append(u)  # adds to existing v
            self.adj_list[u] = []  # creates u
            self.adj_list[u].append(v)  # adds v to u

        elif u in self.adj_list and v not in self.adj_list:
            self.adj_list[u].append(v)  # adds to existing u
            self.adj_list[v] = []  # creates v
            self.adj_list[v].append(u)  # adds u to v
        else:
            self.adj_list[v] = []  # creates v
            self.adj_list[v].append(u)  # adds to v
            self.adj_list[u] = []  # creates u
            self.adj_list[u].append(v)  # adds v to u

    def remove_edge(self, v: str, u: str) -> None:
        """Removes an edge from the graph"""
        if v in self.adj_list and u in self.adj_list:  # if both keys are in the dictionary
            v_list = self.adj_list[v]
            u_list = self.adj_list[u]
            if v in u_list:
                u_list.remove(v)
            if u in v_list:
                v_list.remove(u)

    def remove_vertex(self, v: str) -> None:
        """Removes a vertex and all connected edges"""
        if v in self.adj_list:
            self.adj_list.pop(v)
            for key in self.adj_list:
                if v in self.adj_list[key]:
                    self.adj_list[key].remove(v)

    def get_vertices(self) -> []:
        """Returns a list of vertices in the graph (any order)"""
        vertices = []
        for vertex in self.adj_list:
            vertices.append(vertex)
        return vertices

    def get_edges(self) -> []:
        """Return list of edges in the graph (any order)"""
        edges = []
        for vertex in self.adj_list:
            for adjacent_vertex in self.adj_list[vertex]:
                pair = vertex, adjacent_vertex
                reverse_pair = adjacent_vertex, vertex
                if pair and reverse_pair not in edges:  # determines if the duplicate is already in the list
                    edges.append(pair)
        return edges

    def is_valid_path(self, path: []) -> bool:
        """Return true if provided path is valid, False otherwise"""
        if not path:
            return True
        path_length = len(path)

        for index in range(path_length):
            key_value = path[index]
            if key_value not in self.adj_list:
                return False

            if index == path_length - 1:
                return True

            key_list = self.adj_list[key_value]
            next_val = path[index + 1]
            if next_val not in key_list:
                return False

    def dfs(self, v_start, v_end=None) -> []:
        """Return list of vertices visited during DFS search Vertices are picked in alphabetical order"""
        visited = []
        if v_start not in self.adj_list:
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

            next_vertices_temp = self.adj_list[vertex]
            next_vertices = []
            for x in next_vertices_temp:
                next_vertices.append(x)
            next_vertices.sort()  # sorts the next vertices list
            next_vertices.reverse()  # reverses the list
            for v in next_vertices:
                if v not in visited:
                    stack.append(v)
        return visited

    def bfs(self, v_start, v_end=None) -> []:
        """Return list of vertices visited during BFS search Vertices are picked in alphabetical order"""
        visited = []
        if v_start not in self.adj_list:
            return visited
        que = deque()
        que.appendleft(v_start)

        while len(que) != 0:
            vertex = que.pop()

            if vertex == v_end:  # stops if the end vertex is reached
                visited.append(vertex)
                return visited

            if vertex not in visited:
                visited.append(vertex)
                next_vertices = []
                next_vertices_temp = self.adj_list[vertex]
                for x in next_vertices_temp:
                    next_vertices.append(x)
                next_vertices.sort()  # sorts the next vertices list

                for v in next_vertices:
                    if v not in visited:
                        que.appendleft(v)
        return visited

    def count_connected_components(self):
        """Return number of connected componets in the graph"""
        visited = []
        vertices = self.get_vertices()
        for i in range(len(vertices)):
            visited.append(False)
        count = 0
        for index in range(len(vertices)):
            if visited[index] is False:  # determines if the index has been visited
                vertex_list = self.adj_list[vertices[index]]
                self.count_connected_components_helper(vertex_list, index, visited)  # determines all connected components of current vertex
                count += 1
        return count

    def count_connected_components_helper(self, vertex_list, index, visited):
        """Recursively counts connected components"""
        vertices = self.get_vertices()
        visited[index] = True  # sets the corresponding index to True
        for value in vertex_list:
            next_index = 0
            for i in range(len(visited)):  # determines the next index to be visited
                if value == vertices[i]:
                    next_index = i
            if visited[next_index] is False:  # determines if the index has been visited
                vertex_list = self.adj_list[value]
                self.count_connected_components_helper(vertex_list, next_index, visited)

    def has_cycle(self):
        """Return True if graph contains a cycle, False otherwise"""
        visited = []
        vertices = self.get_vertices()
        for i in range(len(vertices)):
            visited.append(False)

        for index in range(len(vertices)):
            if visited[index] is False:  # determines if the index has been visited
                vertex_list = self.adj_list[vertices[index]]
                if self.has_cycle_helper(vertex_list, index, visited, -1):
                    return True
        return False

    def has_cycle_helper(self, vertex_list, index, visited, parent):
        """Recursively determines if there is a cycle in the graph"""
        visited[index] = True
        vertices = self.get_vertices()
        for value in vertex_list:
            next_index = 0
            for i in range(len(visited)):  # determines the next index to be visited
                if value == vertices[i]:
                    next_index = i
            if visited[next_index] is False:  # determines if the index has been visited
                vertex_list = self.adj_list[value]
                if self.has_cycle_helper(vertex_list, next_index, visited, index):
                    return True
            elif parent != next_index:
                return True
        return False



if __name__ == '__main__':

    # print("\nPDF - method add_vertex() / add_edge example 1")
    # print("----------------------------------------------")
    # g = UndirectedGraph()
    # print(g)

    # for v in 'ABCDE':
    #     g.add_vertex(v)
    # print(g)

    # g.add_vertex('A')
    # print(g)

    # for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
    #     g.add_edge(u, v)
    # print(g)

    # print("\nPDF - method remove_edge() / remove_vertex example 1")
    # print("----------------------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    # g.remove_vertex('DOES NOT EXIST')
    # g.remove_edge('A', 'B')
    # g.remove_edge('X', 'B')
    # print(g)
    # g.remove_vertex('D')
    # print(g)


    # print("\nPDF - method get_vertices() / get_edges() example 1")
    # print("---------------------------------------------------")
    # g = UndirectedGraph()
    # print(g.get_edges(), g.get_vertices(), sep='\n')
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    # print(g)
    # print(g.get_edges(), g.get_vertices(), sep='\n')


    # print("\nPDF - method is_valid_path() example 1")
    # print("--------------------------------------")
    # g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    # print(g)
    # test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    # for path in test_cases:
    #     print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    print(g)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    # print("\nPDF - method count_connected_components() example 1")
    # print("---------------------------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # print(g)
    # test_cases = (
    #     'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #     'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #     'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #     'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    # for case in test_cases:
    #     command, edge = case.split()
    #     u, v = edge
    #     g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    #     print(g.count_connected_components(), end=' ')
    # print()


    # print("\nPDF - method has_cycle() example 1")
    # print("----------------------------------")
    # edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    # g = UndirectedGraph(edges)
    # print(g)
    # test_cases = (
    #     'add QH', 'remove FG', 'remove GQ', 'remove HQ',
    #     'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
    #     'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
    #     'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
    #     'add FG', 'remove GE')
    # for case in test_cases:
    #     command, edge = case.split()
    #     u, v = edge
    #     g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
    #     print('{:<10}'.format(case), g.has_cycle())
