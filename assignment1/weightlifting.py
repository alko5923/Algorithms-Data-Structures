#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 1, Problem 1: Weightlifting

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
from src.weightlifting_data import data  # noqa
# If your solution needs a queue, then you can use this one:
from collections import deque  # noqa
# If you need to log information during tests, execution, or both,
# then you can use this library:
# Basic example:
#   logger = logging.getLogger("put name here")
#   a = 5
#   logger.debug(f"a = {a}")
import logging  # noqa

__all__ = ['weightlifting', 'weightlifting_subset']


def weightlifting(P: Set[int], weight: int) -> bool:
    '''
    Sig:  Set[int], int -> bool
    Pre: Elements of 'P' and 'weight' are non-negative integers
    Post: Return True if there is a subset of 'P' that sums to 'weight',
            False otherwise
    Ex:   P = {2, 32, 234, 35, 12332, 1, 7, 56}
          weightlifting(P, 299) = True
          weightlifting(P, 11) = False
    '''
    plate_list = list(P)
    # Initialise the dynamic programming matrix
    dp_matrix = [
        [None for i in range(weight + 1)] for j in range(len(plate_list) + 1)
    ]

    n=len(plate_list)

    # Build matrix dp_matrix[][] in bottom up manner
    for i in range(n + 1):
        # Variant: n - i
        for j in range(weight + 1):
            # Variant: weight - j
            # Invariant: dp_matrix[0..i][0..j] contains already computed solutions 
            if j == 0:
                dp_matrix[i][j]=True
            elif (i==0 and j>0):
                dp_matrix[i][j]=False
            elif plate_list[i-1]>j:
                dp_matrix[i][j]=dp_matrix[i-1][j]
            else: dp_matrix[i][j]=dp_matrix[i-1][j-plate_list[i-1]] or dp_matrix[i-1][j]
    return dp_matrix[n][weight]


def weightlifting_subset(P: Set[int], weight: int) -> Set[int]:
    '''
    Sig:  Set[int], int -> Set[int]
    Pre: Elements of 'P' and 'weight' are non-negative integers
    Post: Return a subset of 'P' that sums to 'weight' if such a subset exists,
            otherwise return the empty set. 
    Ex:   P = {2, 32, 234, 35, 12332, 1, 7, 56}
          weightlifting_subset(P, 299) = {56, 7, 234, 2}
          weightlifting_subset(P, 11) = {}
    '''

    plate_list = list(P)
    # Initialise the dynamic programming matrix
    dp_matrix = [
        [None for i in range(weight + 1)] for j in range(len(plate_list) + 1)
    ]

    n=len(plate_list)

    # Build matrix dp_matrix[][] in bottom up manner
    for i in range(n + 1):
        # Variant: n - i
        for j in range(weight + 1):
            # Variant: weight - j
            # Invariant: dp_matrix[0..i][0..j] contains already computed solutions 
            if j == 0:
                dp_matrix[i][j]=True
            elif (i==0 and j>0):
                dp_matrix[i][j]=False
            elif plate_list[i-1]>j:
                dp_matrix[i][j]=dp_matrix[i-1][j]
            else: dp_matrix[i][j]=dp_matrix[i-1][j-plate_list[i-1]] or dp_matrix[i-1][j]

    # Now backtrack through the matrix and pick out the weights that were included
    # in the solution, adding them to the solution_set
    solution_set = set()
    # The solution is in the top right-corner of the matrix
    res = dp_matrix[n][weight]
    # Initialize the row index to the weight given
    j = weight

    for i in range(n, 0, -1):
        # Variant: i
        if res == False:
            break
        # If true does not come from the row above, we include the item
        if res == True and res != dp_matrix[i-1][j]:
            # We include the item
            solution_set.add(plate_list[i-1])
            # And move the cursor to the row above, and to the index that equals
            # index_in_row = previous_index_in_row - the weight of the item
            j = j - plate_list[i-1]
            res = dp_matrix[n-1][j]
    return solution_set


class WeightliftingTest(unittest.TestCase):
    """
    Test Suite for weightlifting problem

    Any method named "test_something" will be run when this file is executed.
    Use the sanity check as a template for adding your own test cases if you
    wish. (You may delete this class from your submitted solution.)
    """
    logger = logging.getLogger('WeightLiftingTest')
    data = data
    weightlifting = weightlifting
    weightlifting_subset = weightlifting_subset

    def test_satisfy_sanity(self):
        """
        Sanity Test for weightlifting()

        passing is not a guarantee of correctness.
        """
        plates = {2, 32, 234, 35, 12332, 1, 7, 56}
        self.assertTrue(
            WeightliftingTest.weightlifting(plates, 299)
        )
        self.assertFalse(
            WeightliftingTest.weightlifting(plates, 11)
        )

    def test_subset_sanity(self):
        """
        Sanity Test for weightlifting_subset()

        passing is not a guarantee of correctness.
        """
        plates = {2, 32, 234, 35, 12332, 1, 7, 56}
        weight = 299
        sub = WeightliftingTest.weightlifting_subset(plates, weight)
        for p in sub:
            self.assertIn(p, plates)
        self.assertEqual(sum(sub), weight)

        weight = 11
        sub = WeightliftingTest.weightlifting_subset(plates, weight)
        self.assertSetEqual(sub, set())

    def test_satisfy(self):
        for instance in self.data:
            self.assertEqual(
                WeightliftingTest.weightlifting(instance["plates"],
                                                instance["weight"]),
                instance["expected"]
            )

    def test_subset(self):
        """
        Sanity Test for weightlifting_subset()

        passing is not a guarantee of correctness.
        """
        for instance in self.data:
            plates = WeightliftingTest.weightlifting_subset(
                instance["plates"].copy(),
                instance["weight"]
            )
            self.assertEqual(type(plates), set)

            for plate in plates:
                self.assertIn(plate, instance["plates"])

            if instance["expected"]:
                self.assertEqual(
                    sum(plates),
                    instance["weight"]
                )
            else:
                self.assertSetEqual(
                    plates,
                    set()
                )


if __name__ == '__main__':
    # Set logging config to show debug messages.
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
