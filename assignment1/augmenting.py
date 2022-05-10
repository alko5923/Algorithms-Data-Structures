#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 1, Problem 2: Augmenting Path Detection in Network Graphs

Team Number:
Student Names:
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
from src.augmenting_data import data  # noqa
from src.graph import Graph  # noqa
# If your solution needs a queue, then you can use this one:
from collections import deque  # noqa
# If you need to log information during tests, execution, or both,
# then you can use this library:
# Basic example:
#   logger = logging.getLogger("put name here")
#   a = 5
#   logger.debug(f"a = {a}")
import logging  # noqa

__all__ = ['augmenting', 'augmenting_extended']


def augmenting(G: Graph, s: str, t: str) -> bool:
    """
    Sig:  Graph G(V, E), str, str -> bool
    Pre: There are no incoming edges to 's',
            no outgoing edges from 't'.
            If there is an edge from u to v in 'G', then
            there cannot be an edge from v to u in 'G'.
            'G' has no self-loops.
            Capacities and flows of edges in 'G' are non-negative.
    Post: Return true if there is an augmenting path (as defined in the assignment)
            from 's' to 't', False otherwise.
    Ex:   Sanity tests below
          augmenting(g1, 'a', 'f') = False
          augmenting(g2, 'a', 'f') = True
    """

    visited = set()

    def dfs(v: str):
        # Recursion variant: (Nubmer of nodes in G) - len(visited)    
        if v == t:
            return True
        visited.add(v)
        for neighbor in G.neighbors(v):
            # Loop Variant: len(G.neighbors(v)) - (index of 'neighbor' in G.neighbors(v))
            if neighbor not in visited and G.capacity(v, neighbor) > G.flow(v, neighbor):
                if dfs(neighbor):
                    return True
        return False
    
    return dfs(s)


def augmenting_extended(G: Graph, s: str, t: str) \
                        -> Tuple[bool, List[Tuple[str, str]]]:
    """
    Sig:  Graph G(V,E), str, str -> Tuple[bool, List[Tuple[str, str]]]
    Pre: There are no incoming edges to 's',
            no outgoing edges from 't'.
            If there is an edge from u to v in 'G', then
            there cannot be an edge from v to u in 'G'.
            'G' has no self-loops.
            Capacities and flows of edges in 'G' are non-negative.
    Post: Returns (True, path) if there is an augmenting path from 's' to 't', 
            where path is a list of all edges in the augmenting path,
            (False, []) otherwise.
    Ex:   Sanity tests below
          augmenting_extended(g1, 'a', 'f') = False, []
          augmenting_extended(g2, 'a', 'f') = True, [('a', 'c'), ('c', 'b'),
                                                     ('b', 'd'), ('d', 'f')]
    """
    
    visited = set()
    path = []

    def dfs(v):
        # Recursion Variant: (Nubmer of nodes in G) - len(visited)    
        # Invariant: 'path' contains an augmented path from 's' to 'v'
        visited.add(v)
        if v == t:
            return True
        for neighbor in G.neighbors(v):
            # Loop Variant: len(G.neighbors(v)) - (index of 'neighbor' in G.neighbors(v))
            if neighbor not in visited and G.capacity(v, neighbor) > G.flow(v, neighbor):
                if dfs(neighbor):
                    path.insert(0, (v, neighbor))
                    return True
        return False
    
    return dfs(s), path


class AugmentingTest(unittest.TestCase):
    """
    Test Suite for augmenting path dectection problem

    Any method named "test_something" will be run when this file is executed.
    Use the sanity check as a template for adding your own test cases if you
    wish. (You may delete this class from your submitted solution.)
    """
    logger = logging.getLogger('AugmentingTest')
    data = data
    augmenting = augmenting
    augmenting_extended = augmenting_extended

    def assertIsAugmentingPath(self, graph, s, t, path):
        """
        Asserts that path is an augmenting path in the network graph
        """
        if len(path) == 0:
            self.assertTrue(
                False,
                "The path should be non-empty."
            )

        self.assertEqual(
            path[0][0],
            s,
            f"The path does not start at the source {s}."
        )
        self.assertEqual(
            path[-1][1],
            t,
            f"The path does not end at the sink {t}."
        )

        for u, v in path:
            self.assertIn(
                (u, v),
                graph,
                f"The edge {(u, v)} of the path does not exist in the graph."
            )
            self.assertLess(
                graph.flow(u, v),
                graph.capacity(u, v),
                f"The flow is not less than the capacity for the edge {(u, v)}."
            )

        for i, e in enumerate(path):
            self.assertNotIn(
                e,
                path[i+1:],
                f"The edge {e} occurs more than once in the path."
            )

    def test_sanity(self):
        """
        Sanity Test

        This is a simple sanity check for your function;
        passing is not a guarantee of correctness.
        """

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
        self.assertFalse(AugmentingTest.augmenting(g1, 'a', 'f'))

        g2 = g1.copy()
        g2.set_flow('b', 'd', 11)
        self.assertTrue(AugmentingTest.augmenting(g2, 'a', 'f'))

        g3 = Graph(is_directed=True)
        g3.add_edge('a', 'b', capacity=1, flow=0)
        self.assertTrue(AugmentingTest.augmenting(g3, 'a', 'b'))

        g4 = Graph(is_directed=True)
        g4.add_edge('a', 'b', capacity=0, flow=0)
        self.assertFalse(AugmentingTest.augmenting(g4, 'a', 'b'))

    def test_extended_sanity(self):
        """
        sanity test for returned augmenting path

        This is a simple sanity check for your function;
        passing is not a guarantee of correctness.
        """
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
        path_exists, path = AugmentingTest.augmenting_extended(g1, 'a', 'f')
        self.assertFalse(path_exists)
        self.assertListEqual(path, [])

        g2 = g1.copy()
        g2.set_flow('b', 'd', 11)
        path_exists, path = AugmentingTest.augmenting_extended(g2, 'a', 'f')
        self.assertTrue(path_exists)
        self.assertIsAugmentingPath(g2, 'a', 'f', path)

        g3 = Graph(is_directed=True)
        g3.add_edge('a', 'b', capacity=1, flow=0)
        path_exists, path = AugmentingTest.augmenting_extended(g3, 'a', 'b')
        self.assertTrue(path_exists)
        self.assertIsAugmentingPath(g2, 'a', 'b', path)

        g4 = Graph(is_directed=True)
        g4.add_edge('a', 'b', capacity=0, flow=0)
        path_exists, path = AugmentingTest.augmenting_extended(g4, 'a', 'b')
        self.assertFalse(path_exists)
        self.assertListEqual(path, [])

    def test_augmenting(self):
        """
        Test for augmenting

        passing is not a guarantee of correctness.
        """
        for i, instance in enumerate(AugmentingTest.data):
            graph = instance["digraph"].copy()
            found = AugmentingTest.augmenting(
                graph,
                instance["source"],
                instance["sink"]
            )
            m = "" if instance["expected"] else " not"
            self.assertEqual(
                found,
                instance["expected"],
                f"The network should{m} contain an augmenting path, "
                f"but the returned value is {found} for instance {i}."
            )

    def test_augmenting_extended(self):
        """
        Test for returned augmenting path

        passing is not a guarantee of correctness.
        """
        for i, instance in enumerate(AugmentingTest.data):
            graph = instance["digraph"].copy()
            found, path = AugmentingTest.augmenting_extended(
                graph,
                instance["source"],
                instance["sink"]
            )
            m = "" if instance["expected"] else " not"
            self.assertEqual(
                found,
                instance["expected"],
                f"The network should{m} contain an augmenting "
                f"path for instance {i}."
            )
            if instance["expected"]:
                self.assertIsAugmentingPath(
                    instance["digraph"].copy(),
                    instance["source"],
                    instance["sink"],
                    path
                )
            else:
                self.assertListEqual(path, [])


if __name__ == '__main__':
    # Set logging config to show debug messages.
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
