'''
    Name: GraphCreation.py
    Author: Kailiang Zhu
    Version: V1.0
    Time: 30/08/2024
    Description: This file is used to create the graph for the project.
'''

class Node:
    def __init__(self, id, position):
        self.id = id
        self.connected = dict()
        self.visited = False
        self.position = position

    def add_neighbor(self, node, cost):
        self.connected[node] = cost

    def get_successors(self):
        return self.connected.keys()

    def get_neighbour(self, id):
        for key in self.connected.keys():
            if key.id == id:
                return key
        return None

    def get_position(self):
        return self.position

    # def __str__(self):
    #     return self.name

    # def __repr__(self):
    #     return self.name

class Graph:
    def __init__(self):
        self.nodes = dict()

    def add_node(self, id, position):
        self.nodes[id] = Node(id, position)

    def add_edge(self, id1, id2, cost):
        self.nodes[id1].add_neighbor(self.nodes[id2], cost)
        self.nodes[id2].add_neighbor(self.nodes[id1], cost)
    
    def get_node(self, id):
        return self.nodes[id]

    def get_nodes(self):
        nodes = []
        for key in self.nodes.keys():
            nodes.append(self.nodes[key])
        return nodes

    def get_node_ids(self):
        return self.nodes.keys()

    def get_node_id(self, node):
        for key in self.nodes.keys():
            if self.nodes[key] == node:
                return key
        return None

    def get_edges(self):
        edges = []
        for node in self.get_nodes():
            for neighbour in node.get_successors():
                edges.append((node, neighbour, node.connected[neighbour]))
        return edges
    
    
    # def __str__(self):
    #     return self.name
    
    # def __repr__(self):
    #     return self.name

    def create_graph(nodes, edges):
        graph = Graph()
        for node in nodes:
            graph.add_node(node)
        for edge in edges:
            graph.add_edge(edge[0], edge[1], edge[2])
        return graph

    def draw_graph(graph):
        for node in graph.get_nodes():
            print("Node: ", node.id)
            print("Connected to: ")
            for neighbour in node.get_successors():
                print(neighbour.id, " with cost ", node.connected[neighbour])
            print("\n")
