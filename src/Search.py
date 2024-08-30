'''
    This file contains the implementation of the search algorithm.
    Author: Kailiang Zhu
    Version: V1.0
    Time: 30/08/2024
    Description: This file is used to search the graph.
'''

from GraphCreation import Graph, Node
from util import *


class Search:

    def __init__(self, search_type, graph, start, goal, heuristic):
        self.search_type = search_type
        self.graph = graph
        self.start = start
        self.goal = goal
        self.heuristic = heuristic

    def search(self):
        h = None
        if self.heuristic == "Manhattan":
            h = self.manhattan_heuristic
            print(h)
        elif self.heuristic == "Euclidean":
            h = self.euclidean_heuristic
        elif self.heuristic == "badHeuristic":
            h = self.bad_heuristic
        
        if self.search_type == "A*":
            return self.a_star_search(self.graph, self.start, self.goal, h)
        else:
            return None


    def a_star_search(self, graph, start, goal, heuristic):
        myPQ = PriorityQueue()
        startNode = (start, 0, [])
        myPQ.push(startNode, heuristic(start, goal))
        best_g = dict()

        while not myPQ.isEmpty():
            node = myPQ.pop()
            state, cost, path = node
            if (not state in best_g) or (cost < best_g[state]):
                best_g[state] = cost
                if state == goal:
                    return path
                for neighbour in state.get_successors():
                    new_cost = cost + state.connected[neighbour]
                    myPQ.push((neighbour, new_cost, path + [neighbour.id]), new_cost + heuristic(neighbour, goal))
        # If the open list is empty and the goal is not reached
        return None

    def manhattan_heuristic(self, node, goal):
        return abs(node.position[0] - goal.position[0]) + abs(node.position[1] - goal.position[1])

    def euclidean_heuristic(self, node, goal):
        return ((node.position[0] - goal.position[0]) ** 2 + (node.position[1] - goal.position[1]) ** 2) ** 0.5

    def bad_heuristic(self, node, goal):
        return 0
