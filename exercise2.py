
#!/usr/bin/env python3

""" Assignment 3, Exercise 2, INF1340, Fall, 2015. Kanadia

Computer-based immigration office for Kanadia

"""

__author__ = 'Susan Sim'
__email__ = "ses@drsusansim.org"
__copyright__ = "2015 Susan Sim"
__license__ = "MIT License"

import re
import datetime
import json

######################
## global constants ##
######################
REQUIRED_FIELDS = ["passport", "first_name", "last_name",
                   "birth_date", "home", "entry_reason", "from"]

######################
## global variables ##
######################
'''
countries:
dictionary mapping country codes (lowercase strings) to dictionaries
containing the following keys:
"code","name","visitor_visa_required",
"transit_visa_required","medical_advisory"
'''
COUNTRIES = None

with open("test_returning_citizen.json", "r") as file_reader:
    traveller_file_contents = file_reader.read()

traveller_entry_records = json.loads(traveller_file_contents)

with open("countries.json", "r") as file_reader:
    country_list = file_reader.read()

country_list_info = json.loads(country_list)

#Not sure if necessary, but do use some
for traveller in traveller_entry_records:
    passport_number = traveller['passport']
    first_name = traveller['first_name']
    last_name = traveller['last_name']
    home = traveller['home']['country']
    birth_date = traveller['birth_date']
    entry_reason = traveller['entry_reason']
    entry_from = traveller['from']['country']


#####################
# HELPER FUNCTIONS ##
#####################
def is_more_than_x_years_ago(x, date_string):
    """
    Check if date is less than x years ago.

    :param x: int representing years
    :param date_string: a date string in format "YYYY-mm-dd"
    :return: True if date is less than x years ago; False otherwise.
    """

    now = datetime.datetime.now()
    x_years_ago = now.replace(year=now.year - x)
    date = datetime.datetime.strptime(date_string, '%Y-%m-%d')

    return (date - x_years_ago).total_seconds() < 0


def decide(input_file, countries_file):
    """
    Decides whether a traveller's entry into Kanadia should be accepted

    :param input_file: The name of a JSON formatted file that contains
        cases to decide
    :param countries_file: The name of a JSON formatted file that contains
        country data, such as whether an entry or transit visa is required,
        and whether there is currently a medical advisory
    :return: List of strings. Possible values of strings are:
        "Accept", "Reject", and "Quarantine"
    """


#Check required info for completeness
    #Check first/ last name
        #if incomplete
            #return reject
    #Check DOB
        #if incomplete
            #return reject
    #Check passport number
        #if incomplete
            #return reject
    #Check location (home)
        #if incomplete
            #return reject
    #Check location (travelling from)
        #if incomplete
            #return reject
    #Check reason for entry
        #if incomplete
            #return reject

#Check location
    #if location = unknown
        #return reject
    #elif:
        #location = KAN
        #return accept

for traveller in traveller_entry_records:
    if traveller['home']['country'] == "KAN":
        print("Accept")
    else:
        #placeholder to see if working
        print ("Not home country")
    #else:
        #keep going

#if reason_for_entry = visit and visitor_visa_required = 1
    #must have visa and visa must be less than two years
#else:
    #return reject

for traveller in traveller_entry_records:
    if traveller['entry_reason'] == "visit":
        for country in country_list_info:
            if country_list_info[country]['transit_visa_required'] == "1":
                print traveller
                break
            else:
                print "No visa required"

#If from[country] has warning then
    #return quarantine




    #return ["Reject"]


def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_regex = re.compile(r'\w\w\w\w\w-\w\w\w\w\w-\w\w\w\w\w-\w\w\w\w\w-\w\w\w\w\w')
    passport_match = passport_regex.search(passport_number)

    for passport in traveller_entry_records:
        if passport_match is None:
            print "False"
        else:
            print "True"

valid_passport_format(passport_number)

def valid_visa_format(visa_code):
    """
    Checks whether a visa code is two groups of five alphanumeric characters
    :param visa_code: alphanumeric string
    :return: Boolean; True if the format is valid, False otherwise

    """
#Not sure about this one (since there are no visa codes in the json files
#but it would be formatted very similarly to the others

#valid_visa_format(visa_code)

def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    valid_date_format_regex = re.compile(r'\d\d\d\d-\d\d-\d\d')
    valid_date_match = valid_date_format_regex.search(birth_date)

    #Currently this only works for birth date
    for date in traveller_entry_records:
        if valid_date_match is None:
            print "False"
        else:
            print "True"

valid_date_format(valid_date_format)

