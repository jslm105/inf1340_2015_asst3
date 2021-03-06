#!/usr/bin/env python3

""" Assignment 3, Exercise 1, INF1340, Fall, 2015. DBMS

This module performs table operations on database tables
implemented as lists of lists. """

__author__ = 'Aaron Campbell, Jessica Mallender, Jake Miller, and Susan Sim'
__email__ = "ses@drsusansim.org"
__copyright__ = "2015 Campbell, Mallender, Miller, Sim"
__license__ = "MIT License"


#####################
# HELPER FUNCTIONS ##
#####################

def remove_duplicates(l):
    """
    Removes duplicates from l, where l is a List of Lists.
    :param l: a List
    """

    d = {}
    result = []
    for row in l:
        if tuple(row) not in d:
            result.append(row)
            d[tuple(row)] = True

    return result


class UnknownAttributeException(Exception):
    """
    Raised when attempting set operations on a table
    that does not contain the named attribute
    """
    pass


def selection(t, f):
    """
    Perform select operation on table t that satisfy condition f.
    :param t: a table (a list of lists)
    :param f: a function to apply to t
    :returns: a new table (a list of lists) that is the result of applying function f to table t
    :returns: None if the result is an empty table

    Example:
    > R = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
    ># Define function f that returns True if
    > # the last element in the row is greater than 3.
    > def f(row): row[-1] > 3
    > select(R, f)
    [["A", "B", "C"], [4, 5, 6]]

    """
    selection_list = []
    selection_list.append(t[0])
    for row in t[1:]:  # iterate through the rows of a table
        if f(row) is True:
            selection_list.append(row)  # if return True append to new table
    if len(selection_list) == 1:  # return None if only first row was added to the table
        print None
    else:
        return selection_list


def projection(t, r):
    """
    Perform projection operation on table t
    using the attributes subset r.

    :param: t: a table (list of lists)
    :param: r: item found in a list (table)
    :returns: new table (list of lists)
    :raises: AttributeError if item not found in table

    Example:
    > R = [["A", "B", "C"], [1, 2, 3], [4, 5, 6]]
    > projection(R, ["A", "C"])
    [["A", "C"], [1, 3], [4, 6]]

    """
    new_table = []
    for item in r:  # for each item in a list
        if item in t[0]:  # searches header of table
            index = t[0].index(item)  # finds all the values in index and adds them to new table
        counter = 0
        for row in t:
            if item not in t[0]:
                raise UnknownAttributeException
            if r.index(item) == 0:
                new_table.append([row[index]])
            elif r.index(item) > 0:
                new_table[counter].append(row[index])
                counter += 1
    return new_table


def cross_product(t1, t2):
    """
    :param: t1 a list of lists
    :param: t2 a list of lists
    :returns: cross-product of tables t1 and t2.

    Example:
    > R1 = [["A", "B"], [1,2], [3,4]]
    > R2 = [["C", "D"], [5,6]]
    [["A", "B", "C", "D"], [1, 2, 5, 6], [3, 4, 5, 6]]

    """
    new_table = t1[0] + t2[0]
    new_table_2 = []
    for l1 in t1[1:]:  # iterate through table1
        for l2 in t2[1:]:  # iterate through table2
            l3 = l1 + l2  # create new table of the product of table1 and table2
            new_table_2.append(l3)
    new_table_2.insert(0, new_table)
    if len(new_table_2) <= 1:  # return None if table2 is empty
        return None
    else:
        return new_table_2
