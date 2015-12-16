#!/usr/bin/env python3

""" Module to test papers.py  """

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"

__copyright__ = "2014 Susan Sim"
__license__ = "MIT License"

__status__ = "Prototype"

# imports one per line
import pytest
import os
from exercise2 import decide

DIR = "test_jsons/"
os.chdir(DIR)


def test_returning():
    """
    Travellers are returning to KAN.
    """
    assert decide("test_returning_citizen.json", "countries.json") ==\
        ["Accept", "Accept", "Quarantine"]

def test_visitors_with_visas():
    """
    Visitors to KAN
    """
    assert decide("test_visitors_with_visas.json", "countries.json") ==\
        ["Accept"]

def test_incomplete_entries():
    """
    Travellers with one entry missing from all possible fields
    """
    assert decide("test_incomplete_entries.json", "countries.json") ==\
        ["Reject", "Reject", "Reject", "Reject", "Reject", "Reject", \
         "Reject", "Reject", "Reject", "Reject", "Reject", "Quarantine", \
         "Reject", "Reject"]

def test_improper_passports():
    """
    Travellers with passports with more or less characters or "_"
    """
    assert decide("test_improper_passports.json", "countries.json") ==\
           ["Reject", "Reject", "Reject"]