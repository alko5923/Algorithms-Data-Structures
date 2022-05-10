#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 3, Problem 1: Controlling the Maximum Flow

Team Number: 15
Student Names: Aljaz Kovac and Jakob Nordgren
'''

'''
Copyright: justin.pearson@it.uu.se and his teaching assistants, 2020.

This file is part of course 1DL231 at Uppsala University, Sweden.

Permission is hereby granted only to the registered students of that
course to use this file, for a homework assignment.

The copyright notice and permission notice above shall be included in
all copies and extensions of this file, and those are not allowed to
appear publicly on the internet, both during a course instance and
forever after.
'''
from typing import *  # noqa
import unittest  # noqa
import math  # noqa
from src.sensitive_data import data  # noqa
from src.graph import Graph  # noqa
# If your solution needs a queue, then you can use this one:
from collections import deque  # noqa
# If you need to log information during tests, execution, or both,
# then you can use this library:
# Basic example:
#   logger = logging.getLogger('put name here')
#   a = 5
#   logger.debug(f"a = {a}")
import logging  # noqa

__all__ = ['sensitive']

def calculateResidualGraph(G: Graph, s: str) -> Graph:
    queue = []
    visited = []
    G_residual = Graph(is_directed=True)
    # Perform breadth-first search to calculate the residual graph
    def bfs(visited: List, v: str) -> Graph:
        visited.append(v)
        queue.append(v)
        while queue:
            # VARIANT: nr. of vertices encountered for the first time, which have not yet had their adjacency lists fully examined
            n=queue.pop(0)
            for neighbor in G.neighbors(n):
                # VARIANT: length of G.neighbors - nr. of iterations
                if neighbor not in visited:
                    visited.append(neighbor)
                    queue.append(neighbor)
                if G.flow(n, neighbor) == 0:
                    # add edge (n, neighbor) with flow = capacity to the residual graph
                    G_residual.add_edge(n, neighbor, flow=G.capacity(n, neighbor))
                elif G.flow(n, neighbor)==G.capacity(n, neighbor):
                    # add edge (neighbor, n) with flow = old flow to the residual graph
                    G_residual.add_edge(neighbor, n, flow=G.flow(n, neighbor))
                elif G.flow(n, neighbor)>0 and G.flow(n, neighbor)<G.capacity(n, neighbor):
                    # add edge (n, neighbor) with flow = (capacity-flow) to the residual graph
                    G_residual.add_edge(n, neighbor, flow=G.capacity(n, neighbor)-G.flow(n, neighbor))
                     # add edge (neighbor, n) with flow = old flow to the residual graph
                    G_residual.add_edge(neighbor, n, flow=G.flow(n, neighbor))
        return G_residual

    return bfs(visited, s)

def sensitive(G: Graph, s: str, t: str) -> Tuple[str, str]:
    """
    Sig:  Graph G(V,E), str, str -> Tuple[str, str]
    Pre:
    Post:
    Ex:   sensitive(g1, 'a', 'f') = ('b', 'd')
    """
    # Calculate the residual graph
    G_residual=calculateResidualGraph(G, s)
    queue = []
    visited = []
    
    def bfs(visited: List, v: str) -> List[str]:
        visited.append(v)
        queue.append(v)
        while queue:
            # VARIANT: nr. of vertices encountered for the first time, which have not yet had their adjacency lists fully examined
            n=queue.pop(0)
            for neighbor in G_residual.neighbors(n):
                # VARIANT: length of G_residual.neighbors - nr. of iterations
                if neighbor not in visited:
                    visited.append(neighbor)
                    queue.append(neighbor)
        return visited
    
    # Perform breadth-first search on the residual graph to find the min-cut (all the vertices reachable from the source)
    S=bfs(visited, s)

    # Set the vertices that are not in the min-cut S into T (T = G - S)
    T=list(set(G.nodes) - set(S))
    
    # Find a sensitive edge (min-cut edge), meaning an edge from a vertex in the min-cut (S) to a vertex in the rest of the graph (T)
    for u,v in G.edges:
        # VARIANT: length of G.edges - nr. of iterations 
        if (u in S and v in T) or (u in T and v in S):
            return u,v 
    
    return None, None


class SensitiveTest(unittest.TestCase):
    """
    Test suite for the sensitive edge problem
    """
    logger = logging.getLogger('SensitiveTest')
    data = data
    sensitive = sensitive

    def test_sanity(self):
        """Sanity check"""
        g1 = Graph(is_directed=True)
        g1.add_edge('a', 'b', capacity=16, flow=12)
        g1.add_edge('a', 'c', capacity=13, flow=11)
        g1.add_edge('b', 'd', capacity=12, flow=12)
        g1.add_edge('c', 'b', capacity=4, flow=0)
        g1.add_edge('c', 'e', capacity=14, flow=11)
        g1.add_edge('d', 'c', capacity=9, flow=0)
        g1.add_edge('d', 'f', capacity=20, flow=19)
        g1.add_edge('e', 'd', capacity=7, flow=7)
        g1.add_edge('e', 'f', capacity=4, flow=4)
        self.assertIn(
            SensitiveTest.sensitive(g1, 'a', 'f'),
            {('b', 'd'), ('e', 'd'), ('e', 'f')}
        )
        g2 = Graph(is_directed=True)
        g2.add_edge('a', 'b', capacity=1, flow=1)
        g2.add_edge('a', 'c', capacity=100, flow=4)
        g2.add_edge('b', 'c', capacity=100, flow=1)
        g2.add_edge('c', 'd', capacity=5, flow=5)
        self.assertEqual(
            SensitiveTest.sensitive(g2, 'a', 'd'),
            ('c', 'd')
        )
        g3 = Graph(is_directed=True)
        g3.add_edge('a', 'b', capacity=1, flow=1)
        self.assertEqual(
            SensitiveTest.sensitive(g3, 'a', 'b'),
            ('a', 'b')
        )
        g4 = Graph(is_directed=True)
        g4.add_edge('a', 'b', capacity=0, flow=0)
        self.assertEqual(
            SensitiveTest.sensitive(g4, 'a', 'b'),
            (None, None)
        )
        g5 = Graph(is_directed=True)
        for u, v in g1.edges:
            g5.add_edge(u, v, capacity=0, flow=0)
        self.assertEqual(
            SensitiveTest.sensitive(g5, 'a', 'f'),
            (None, None)
        )
        

    def test_sensitive(self):
        for instance in SensitiveTest.data:
            graph = instance['digraph'].copy()
            u, v = SensitiveTest.sensitive(
                graph,
                instance["source"],
                instance["sink"]
            )
            self.assertIn(u, graph, f"Invalid edge ({u}, {v})")
            self.assertIn((u, v), graph, f"Invalid edge ({u}, {v})")
            self.assertIn(
                (u, v),
                instance["sensitive_edges"]
            )


if __name__ == "__main__":
    # Set logging config to show debug messages.
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
