
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
        1)traveller is from KAN and returning from medically safe country
        2)traveller is from KAN and returning from medically safe country
        3)traveller is from KAN and returning from medically unsafe country
    """
    assert decide("test_returning_citizen.json", "countries.json") ==\
        ["Accept", "Accept", "Quarantine"]

def test_visitors_with_visas():
    """
    Visitors to KAN
        1)traveller from a foreign country that requires a visitor visa
          and visa is valid
        2)traveller from a foreign country that requires a visa
          and visa is expired
        3)traveller from a foreign country that requires a visa
          and visa is improperly formatted
    """
    assert decide("test_visitors_with_visas.json", "countries.json") ==\
        ["Accept", "Reject", 'Reject']

def test_incomplete_entries():
    """
    Travellers with one entry missing from all possible fields
        1)Missing passport number
        2)Missing first name
        3)Missing last name
        4)Missing birth date
        5)Missing home: city
        6)Missing home: region
        7)Missing home: country
        8)Missing entry reason
        9)Missing from: city
        10)Missing from: region
        11)Missing from: country
        12)Missing passport number but quarantine takes priority over reject
        13)Missing visa date
        14)Missing visa code
    """
    assert decide("test_incomplete_entries.json", "countries.json") ==\
        ["Reject", "Reject", "Reject", "Reject", "Reject", "Reject", \
         "Reject", "Reject", "Reject", "Reject", "Reject", "Quarantine", \
         "Reject", "Reject"]

def test_improper_passports():
    """
    Travellers with passports with more or less characters or "_" and mixed letter cases
        1)Passport number is missing letter/digit
        2)Passport number has extra letter/ digit
        3)Passport number contains an underscore

    """
    assert decide("test_improper_passports.json", "countries.json") ==\
           ["Reject", "Reject", "Reject"]

def test_improper_visas():
    """
    Travellers with visas with more or less characters or "_" and mixed letter cases
        1)Visa number is missing letter/digit
        2)Visa number has extra letter/ digit
        3)Visa number contains an underscore

    """
    assert decide("test_improper_passports.json", "countries.json") ==\
           ["Reject", "Reject", "Reject"]

def test_mixed_capitalization():
    """
    Traveller with valid country codes and passport numbers but with
    mixed letter cases
        1)Passport is valid format but some capitals some lower case letters
        2)Country code is not all caps, but still valid

    """
    assert decide("test_mixed_capitalization.json", "countries.json") ==\
        ["Accept", "Accept"]

def test_date_formats():
    """
    Travellers with various date formats
        1)Traveller with correct data format
        2)Traveller with incorrect date format (YYY-MM-DD)
        3)Traveller with date format out of order
        4)Traveller with date month and day out of possible range
        5)Traveller with incorrect date and coming from medical advisory
          country so quarantine should take priority over reject
    :return:
    """
    assert decide("test_improper_birthday_format.json", "countries.json")==\
        ["Accept", "Reject", "Reject", 'Reject', "Quarantine"]

