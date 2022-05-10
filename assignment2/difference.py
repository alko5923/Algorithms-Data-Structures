#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Assignment 2, Problem 1: Search String Replacement

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
from src.difference_data import data  # noqa
from collections import defaultdict  # noqa
from string import ascii_lowercase  # noqa
# If your solution needs a queue, then you can use this one:
from collections import deque  # noqa
# If you need to log information during tests, execution, or both,
# then you can use this library:
# Basic example:
#   logger = logging.getLogger("put name here")
#   a = 5
#   logger.debug(f"a = {a}")
import logging  # noqa


# Solution to Task B:
def min_difference(u: str, r: str, R: Dict[str, Dict[str, int]]) -> int:
    """
    Sig:  str, str, Dict[str, Dict[str, int]] -> int
    Pre:  For all characters c in u and k in r,
          then R[c][k] exists, and R[k][c] exists.
    Post: Return the minimal cost of changing string u into string r according to
            the given resemblance matrix
    Ex:   Let R be the resemblance matrix where every change and skip
          costs 1
          min_difference("dinamck", "dynamic", R) --> 3
    """
    # To get the resemblance between two letters, use code like this:
    # difference = R['a']['b']

    # List comprehension loop Variant: len(r)-len(u)-(iteration_number)
    # The u string goes on the x-axis, r goes on the y-axis
    dp_matrix = [
        [None for _ in range(len(r)+1)] for _ in range(len(u)+1)
        ]
    dp_matrix[0][0] = R['-']['-']
    for x in range(1,len(u)+1):
        # Variant: len(u)-x
        dp_matrix[x][0] = dp_matrix[x-1][0] + R[u[x-1]]['-']
    for y in range(1,len(r)+1):
        # Variant: len(r)-y
        dp_matrix[0][y] = dp_matrix[0][y-1] + R['-'][r[y-1]]


    # Populate the matrix
    for x in range(1, len(u)+1):
        # Variant: len(u)-x
        for y in range(1, len(r)+1):
            # Variant: len(r)-y
            dp_matrix[x][y] = min(
                dp_matrix[x-1][y] + R[u[x-1]]['-'], 
                dp_matrix[x][y-1] + R['-'][r[y-1]], 
                dp_matrix[x-1][y-1] + R[u[x-1]][r[y-1]])
    
    # Read the result
    result = dp_matrix[len(u)][len(r)]
    return result

# Solution to Task C:
def min_difference_align(u: str, r: str,
                         R: Dict[str, Dict[str, int]]) -> Tuple[int, str, str]:
    """
    Sig:  str, str, Dict[str, Dict[str, int]] -> Tuple[int, str, str]
    Pre:  For all characters c in u and k in r,
          then R[c][k] exists, and R[k][c] exists.
    Post: Return the minimal cost of changing string u into string r according to
            the given resemblance matrix, as well as the aligned strings.
    Ex:   Let R be the resemblance matrix where every change and skip
          costs 1
          min_difference_align("dinamck", "dynamic", R) -->
                                    3, "dinam-ck", "dynamic-"
    """

    # List comprehension loop Variant: len(r)-len(u)-(iteration_number)
    # The u string goes on the x-axis, r goes on the y-axis
    dp_matrix = [
        [None for _ in range(len(r)+1)] for _ in range(len(u)+1)
        ]
    dp_matrix[0][0] = R['-']['-']
    for x in range(1,len(u)+1):
        # Variant: len(u)-x
        dp_matrix[x][0] = dp_matrix[x-1][0] + R[u[x-1]]['-']
    for y in range(1,len(r)+1):
        # Variant: len(r)-y
        dp_matrix[0][y] = dp_matrix[0][y-1] + R['-'][r[y-1]]


    # Populate the matrix
    for x in range(1, len(u)+1):
        # Variant: len(u)-x
        for y in range(1, len(r)+1):
            # Variant: len(r)-y
            dp_matrix[x][y] = min(
                dp_matrix[x-1][y] + R[u[x-1]]['-'], 
                dp_matrix[x][y-1] + R['-'][r[y-1]], 
                dp_matrix[x-1][y-1] + R[u[x-1]][r[y-1]])
    
    # Read the result
    result = dp_matrix[len(u)][len(r)]

    def align(x, y, u, r):
        '''
        Sig: int, int, str, str -> Tuple[str, str]
        Pre: dp_matrix[i][j] contains the minimum difference for strings u[i-1] and r[j-1]
                On the first(non-recursive) call, x=len(u) andn y=len(r)
        Post: Returns strings r and u with inserted '-' characters, indicating the minimal
                cost alignment of the strings.
        Ex: (Let R map all changes and skips to value 1)
            align(len("dinamic"), len("dynamck"), "dynamic", "dinamck") -> "dinam-ck", "dynamic-"
        
        Variant: x+y
        Invariant: At each call the tails of each string, u[x:] and r[y:], are aligned
        '''
        if x == 0 and y == 0:
            return u, r
        
        leftVal = dp_matrix[x-1][y] + R[u[x-1]]['-']
        underVal = dp_matrix[x][y-1] + R['-'][r[y-1]]
        diagonalVal = dp_matrix[x-1][y-1] + R[u[x-1]][r[y-1]]

        if  leftVal < underVal and leftVal < diagonalVal:
            return align(x-1, y, u, r[:y] + '-' + r[y:])
        elif underVal < diagonalVal:
            return align(x, y-1, u[:x] + '-' + u[x:], r)
        else:
            return align(x-1, y-1, u, r)

    alignedU, alignedR = align(len(u), len(r), u, r)

    return result, alignedU, alignedR

# Sample matrix provided by us:
def qwerty_distance() -> Dict[str, Dict[str, int]]:
    """
    Generates a QWERTY Manhattan distance resemblance matrix

    Costs for letter pairs are based on the Manhattan distance of the
    corresponding keys on a standard QWERTY keyboard.
    Costs for skipping a character depends on its placement on the keyboard:
    adding a character has a higher cost for keys on the outer edges,
    deleting a character has a higher cost for keys near the middle.

    Usage:
        R = qwerty_distance()
        R['a']['b']  # result: 5
    """
    R = defaultdict(dict)
    R['-']['-'] = 0
    zones = ["dfghjk", "ertyuislcvbnm", "qwazxpo"]
    keyboard = ["qwertyuiop", "asdfghjkl", "zxcvbnm"]
    for row, content in enumerate(zones):
        for char in content:
            R['-'][char] = row + 1
            R[char]['-'] = 3 - row
    for a, b in ((a, b) for b in ascii_lowercase for a in ascii_lowercase):
        row_a, pos_a = next(
            (row, content.index(a))
            for row, content in enumerate(keyboard) if a in content
        )
        row_b, pos_b = next(
            (row, content.index(b))
            for row, content in enumerate(keyboard) if b in content
        )
        R[a][b] = abs(row_b - row_a) + abs(pos_a - pos_b)
    return R


class MinDifferenceTest(unittest.TestCase):
    """
    Test Suite for search string replacement problem

    Any method named "test_something" will be run when this file is
    executed. Use the sanity check as a template for adding your own test
    cases if you wish.
    (You may delete this class from your submitted solution.)
    """
    logger = logging.getLogger('MinDifferenceTest')
    data = data
    min_difference = min_difference
    min_difference_align = min_difference_align

    def assertMinDifference(self, u, r, difference, R):
        res_difference = MinDifferenceTest.min_difference(u, r, R)
        self.assertEqual(
            res_difference,
            difference,
            'Difference for '
            f'u="{u}" and '
            f'r="{r}" was '
            f'{res_difference}, '
            f'{difference} expected'
        )

    def assertMinDifferenceAlign(self, u, r, difference, R):
        res_difference, res_u, res_r = MinDifferenceTest.min_difference_align(
            u,
            r,
            R
        )
        self.assertEqual(
            res_difference,
            difference,
            f'Difference of u="{u}" and r="{r}" was {res_difference}, '
            f'{difference} expected.'
        )

        self.assertEqual(
            len(res_u),
            len(res_r),
            f'len("{u}") != len("{r}")'
        )

        res_sum = sum(
            (R[res_u[i]][res_r[i]] for i in range(len(res_u)))
        )

        self.assertEqual(
            res_sum,
            difference,
            'Difference for '
            f'u="{u}", r={r}, res_r={res_u}, and '
            f'r="{res_r}" was summed to '
            f'{res_sum}, '
            f'{difference} expected.'
        )

    def test_diff_sanity(self):
        """
        Difference sanity test

        Given a simple resemblance matrix, test that the reported
        difference is the expected minimum. Do NOT assume we will always
        use this resemblance matrix when testing!
        """
        alphabet = ascii_lowercase + '-'
        # The simplest (reasonable) resemblance matrix:
        R = {
            a: {b: (0 if a == b else 1) for b in alphabet} for a in alphabet
        }
        # Warning: we may (read: 'will') use another matrix!
        self.assertMinDifference("dinamck", "dynamic", 3, R)

    def test_align_sanity(self):
        """
        Simple alignment

        Passes if the returned alignment matches the expected one.
        """
        # QWERTY resemblance matrix:
        self.assertMinDifferenceAlign(
            "polynomial",
            "exponential",
            15,
            qwerty_distance()  # QWERTY resemblance matrix
        )
        _, u, r = MinDifferenceTest.min_difference_align(
            "polynomial",
            "exponential",
            qwerty_distance()
        )
        # Warning: there may be other optimal matchings!
        if u != '--polyn-om-ial':
            self.logger.warning(f"'{u}' != '--polyn-om-ial'")
        if r != 'exp-o-ne-ntial':
            self.logger.warning(f"'{r}' != 'exp-o-ne-ntial'")

    def test_min_difference(self):
        for instance in MinDifferenceTest.data:
            self.assertMinDifference(
                instance["u"],
                instance["r"],
                instance["expected"],
                qwerty_distance()
            )

    def test_min_difference_align(self):
        for instance in MinDifferenceTest.data:
            self.assertMinDifferenceAlign(
                instance["u"],
                instance["r"],
                instance["expected"],
                qwerty_distance()
            )

if __name__ == '__main__':
    # Set logging config to show debug messages.
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()
