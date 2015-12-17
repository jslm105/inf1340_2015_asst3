#!/usr/bin/env python

""" Assignment 3, Exercise 1, INF1340, Fall, 2015. DBMS

Test module for exercise3.py

"""

__author__ = 'Aaron Campbell, Jessica Mallender, Jake Miller, and Susan Sim'
__email__ = "ses@drsusansim.org"
__copyright__ = "2015 Campbell, Mallender, Miller, Sim"
__license__ = "MIT License"

from exercise1 import selection, projection, cross_product, UnknownAttributeException, remove_duplicates

###########
# TABLES ##
###########

EMPLOYEES = [["Surname", "FirstName", "Age", "Salary"],
             ["Smith", "Mary", 25, 2000],
             ["Black", "Lucy", 40, 3000],
             ["Verdi", "Nico", 36, 4500],
             ["Smith", "Mark", 40, 3900]]

R1 = [["Employee", "Department"],
      ["Smith", "sales"],
      ["Black", "production"],
      ["White", "production"]]

R2 = [["Department", "Head"],
      ["production", "Mori"],
      ["sales", "Brown"]]

SUSPECTS = [["Surname", "Title", "Age"],
            ["Mustard", "Colonel", 63],
            ["Scarlet", "Ms.", 28],
            ["Green", "Mr.", 37],
            ["White", "Mrs.", 56],
            ["Plum", "Professor", 48]]

CLUES = [["Weapon", "Location"],
         ["Candlestick", "Conservatory"],
         ["Rope", "Music Room"],
         ["Revolver", "Drawing Room"]]

A1 = [["Artist", "Album"],
      ["The Beatles", "Rubber Soul"],
      ["Rolling Stones", "Let It Bleed"],
      ["The Cure", "Disintegration"]]

A2 = [["Label", "Year"],
      ["Apple", 1965],
      ["Decca", 1969],
      ["Fiction", 1989]]

BLANK = [[]]

BLANK2 = [[]]


#####################
# HELPER FUNCTIONS ##
#####################

def is_equal(t1, t2):
    t1.sort()
    t2.sort()

    return t1 == t2


#####################
# FILTER FUNCTIONS ##
#####################
def filter_employees(row):
    """
    Check if employee represented by row
    is AT LEAST 30 years old and makes
    MORE THAN 3500.
    :param row: A List in the format:
        [{Surname}, {FirstName}, {Age}, {Salary}]
    :return: True if the row satisfies the condition, None if empty
    """
    return row[-2] >= 30 and row[-1] > 3500


def filter_employees_none(row):
    """
    Check if employee represented by row
    is AT LEAST 50 years old and makes
    MORE THAN 50000.
    :param row: A List in the format:
        [{Surname}, {FirstName}, {Age}, {Salary}]
    :return: True if the row satisfies the condition, None if empty
    """
    return row[-2] >= 50 and row[-1] > 5000


def filter_suspects(row):
    """
    Check if suspects age represented by row
    is at least 40 years old
    :param row: A List in the format:
        [{Surname}, {Title}, {Age}]
    :return: True if the row satisfies the condition, None if empty
    """
    return row[-1] > 40

def filter_employees_names(row):
    """
    Check if employee represented by row
    has a first name containing "o"
    :param row: A List in the format:
        [{Surname}, {FirstName}, {Age}, {Salary}]
    :return: True if the row satisfies the condition, None if empty
    """
    return "o" in row[1]

###################
# TEST FUNCTIONS ##
###################

######################
# Selection Function #
######################


def test_selection():
    """
    Test select operation.
    return: a new table the result of applying function to original table
    """

    result = [["Surname", "FirstName", "Age", "Salary"],
              ["Verdi", "Nico", 36, 4500],
              ["Smith", "Mark", 40, 3900]]

    assert is_equal(result, selection(EMPLOYEES, filter_employees))


def test_selection_our_test():
    """
    Another test select operation.
    return: a new table the result of applying function to original table
    """
    result = [["Surname", "Title", "Age"],
              ["Mustard", "Colonel", 63],
              ["White", "Mrs.", 56],
              ["Plum", "Professor", 48]]

    assert is_equal(result, selection(SUSPECTS, filter_suspects))

def test_selection_one_row():
    """
    Tests selection function to see if selection table
    of just one row is properly generated.
    return: a new table the result of applying function to original table)
    """
    result = [["Surname", "FirstName", "Age", "Salary"],
              ["Verdi", "Nico", 36, 4500]]
    assert is_equal(result, selection(EMPLOYEES, filter_employees_names))

def test_selection_none():
    """
    Tests selection function to see if None is returned when
    it results in an empty table
    return: None (empty table)
    """
    assert (selection(EMPLOYEES, filter_employees_none)) is None

######################
# Projection Function #
######################


def test_projection():
    """
    Test projection operation for multiple attribute
    return: list of columns named in attributes
    """

    result = [["Surname", "FirstName"],
              ["Smith", "Mary"],
              ["Black", "Lucy"],
              ["Verdi", "Nico"],
              ["Smith", "Mark"]]

    assert is_equal(result, projection(EMPLOYEES, ["Surname", "FirstName"]))


def test_projection_different_order():
    """
    Test projection for single attribute projection
    :return: list of column named in attribute
    """
    result = [["FirstName"],
              ["Mary"],
              ["Lucy"],
              ["Nico"],
              ["Mark"]]

    assert is_equal(result, projection(EMPLOYEES, ["FirstName"]))


def test_projection_error():
    """
    Checks to make sure that the UnknownAttributeException is
    raised when the indicated attribute is not found within the table
    and when attribute is left blank
    :return:
    """
    try:
        projection(EMPLOYEES, [""])
    except UnknownAttributeException:
        assert True

    try:
        projection(EMPLOYEES, ["Department"])
    except UnknownAttributeException:
        assert True

##########################
# Cross Product Function #
##########################


def test_projection_our_test():
    """
    Test cross product operation
    :return: list of cross product rows
    """
    result = [["Surname", "Title"],
              ["Mustard", "Colonel"],
              ["Scarlet", "Ms."],
              ["Green", "Mr."],
              ["White", "Mrs."],
              ["Plum", "Professor"]]

    assert is_equal(result, projection(SUSPECTS, ["Surname", "Title"]))


def test_cross_product():
    """
    Test cross product operation.
    return: list of cross product rows
    """

    result = [["Employee", "Department", "Department", "Head"],
              ["Smith", "sales", "production", "Mori"],
              ["Smith", "sales", "sales", "Brown"],
              ["Black", "production", "production", "Mori"],
              ["Black", "production", "sales", "Brown"],
              ["White", "production", "production", "Mori"],
              ["White", "production", "sales", "Brown"]]

    assert is_equal(result, cross_product(R1, R2))


def test_cross_product_our_test():
    """
    Another test cross product operation
    :return:list of cross product rows
    """

    result = [["Artist", "Album", "Label", "Year"],
              ["The Beatles", "Rubber Soul", "Apple", 1965],
              ["The Beatles", "Rubber Soul", "Decca", 1969],
              ["The Beatles", "Rubber Soul", "Fiction", 1989],
              ["Rolling Stones", "Let It Bleed", "Apple", 1965],
              ["Rolling Stones", "Let It Bleed", "Decca", 1969],
              ["Rolling Stones", "Let It Bleed", "Fiction", 1989],
              ["The Cure", "Disintegration", "Apple", 1965],
              ["The Cure", "Disintegration", "Decca", 1969],
              ["The Cure", "Disintegration", "Fiction", 1989]]

    assert is_equal(result, cross_product(A1, A2))


def test_cross_product_none():
    """
    Tests selection function to see if None is returned when
    it results in an empty table
    return: None (empty table)
    """
    assert cross_product(BLANK, BLANK2) is None
