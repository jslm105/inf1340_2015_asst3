# !/usr/bin/env python3

""" Assignment 3, Exercise 2, INF1340, Fall, 2015. Kanadia

Computer-based immigration office for Kanadia

"""

__author__ = 'Aaron Campbell, Jessica Mallender, Jake Miller, and Susan Sim'
__email__ = "ses@drsusansim.org"
__copyright__ = "2015 Campbell, Mallender, Miller, Sim"
__license__ = "MIT License"

import re
import datetime
import json
import os



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


########################
# VALIDATION FUNCTIONS #
########################

def valid_passport_format(passport_number):
    """
    Checks whether a passport number is five sets of five alpha-number characters separated by dashes
    :param passport_number: alpha-numeric string
    :return: Boolean; True if the format is valid, False otherwise
    """
    passport_regex = re.compile(r'\w\w\w\w\w-\w\w\w\w\w-\w\w\w\w\w-\w\w\w\w\w-\w\w\w\w\w')
    passport_match = passport_regex.search(passport_number)

    # removes any passport incorrectly using underscores as \w will pass this type of character
    if "_" in passport_number:
        return False
    else:
        if passport_match is None:
            return False
        else:
            return True


def valid_date_format(date_string):
    """
    Checks whether a date has the format YYYY-mm-dd in numbers
    :param date_string: date to be checked
    :return: Boolean True if the format is valid, False otherwise
    """
    valid_date_format_regex = re.compile(r'(\d\d\d\d)-(\d\d)-(\d\d)')
    valid_date_match = valid_date_format_regex.search(date_string)

    if valid_date_match is None:
        return False
    else:
        # Assuming anybody over 115 years or visas that old are not travelling
        if int(valid_date_match.group(1)) < 1900:
            return False
        # Ensure valid month entry
        elif int(valid_date_match.group(2)) not in range(1,13):
            return False
        # Ensure valid date entry
        elif int(valid_date_match.group(3)) not in range(1,32):
            return False
        # Ensure correct number of days in Feb.
        elif int(valid_date_match.group(2)) in [2] and int(valid_date_match.group(3)) > 29:
            return False
        # Ensure correctness for 30-day months
        elif int(valid_date_match.group(2)) in [4, 6, 9, 10] and int(valid_date_match.group(3)) > 30:
            return False
        # Ensure date is not in the future
        elif is_more_than_x_years_ago(0, date_string):
            return True

#valid_date_format("1969-12-11")


def valid_visa_format(visa_number):
    """
    Checks whether a visa code is two groups of five alphanumeric characters
    :param visa_number: alphanumeric string
    :return: Boolean; True if the format is valid, False otherwise

    """
    # NOTE: VISAS MAY BE MORE COMPLEX REQUIRING ALL TO BE UNIQUE CHARACTERS. PUTTING A QUESTION ON BB TO SEE...
    visa_regex = re.compile(r'\w\w\w\w\w-\w\w\w\w\w')
    visa_match = visa_regex.search(visa_number)

    # removes any visa incorrectly using underscores as \w will pass this type of character
    if "_" in visa_number:
        return False
    else:
        if visa_match is None:
            return False
        else:
            return True


#########################
# MAIN DECISION PROGRAM #
#########################

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

    # This opens the json files passed into the function allowing multiple json test files to be run.
    with open(input_file, "r") as file_reader:
        traveller_file_contents = file_reader.read()

    traveller_entry_records = json.loads(traveller_file_contents)

    with open(countries_file, "r") as file_reader:
        country_list = file_reader.read()

    country_list_info = json.loads(country_list)

    # TESTING FOR COMPLETENESS
    # Clearly there will be a value in using separate validation functions for passport, visa and birth date
    # numbers. Whether we will want to do so for things like name and such (which is relatively simple)
    # or just keep that stuff here in the main function is up us as a group.

    # Checks that all required fields are not empty
    # does this by creating a list of required fields and then running through
    # that list and seeing if it is blank for a traveller's record

    # makes list of countries that require visitor visas
    visitor_visa_countries = []
    for country in country_list_info:
        if country_list_info[country]["visitor_visa_required"] == "1":
            visitor_visa_countries.append(country)
            # print visitor_visa_countries

            # makes lists of countries according to medical advisories
    med_advisory_countries = []
    non_med_advisory_countries = []
    for country in country_list_info:
        if country_list_info[country]['medical_advisory'] == "":
            non_med_advisory_countries.append(country)
        else:
            med_advisory_countries.append(country)
            # print med_advisory_countries

    decision = []
    # Checks that all required fields are not empty
    # does this by creating a list of required fields and then running through
    # that list and seeing if it is blank for a traveller's record

    for traveller in traveller_entry_records:
        # A list of every check performed on traveller
        traveller_info = []

        passport_number = traveller['passport']
        first_name = traveller['first_name']
        last_name = traveller['last_name']
        birth_date = traveller['birth_date']
        home_city = traveller['home']['city']
        home_region = traveller['home']['region']
        home_country = traveller['home']['country']
        entry_reason = traveller['entry_reason']
        from_city = traveller['from']['city']
        from_region = traveller['from']['region']
        from_country = traveller['from']['country']

        required_fields = [passport_number, first_name, last_name, birth_date, home_city, home_region,
                           home_country.upper(), entry_reason, from_city, from_region, from_country.upper()]

        if home_country in visitor_visa_countries:
            visa_date = traveller['visa']['date']
            required_fields.append(visa_date)
            visa_code = traveller['visa']['code']
            required_fields.append(visa_code)

        for field in required_fields:
            if field == "":
                traveller_info.append(False)
                break
            else:
                traveller_info.append(True)


                # If all required fields are filled in then checks that countries are recognized as valid countries
                # does this by checking if the home_country and from_country of the traveller's json file are
                # are a key in the dictionary of countries

        if home_country == "KAN":
            traveller_info.append(True)
        elif home_country in country_list_info.keys():
            traveller_info.append(True)
        elif from_country in country_list_info.keys():
            traveller_info.append(True)
        else:
            traveller_info.append(False)

        # Check formatting of passport
        traveller_info.append(valid_passport_format(passport_number))

        # Check formatting of D.O.B.
        traveller_info.append(valid_date_format(birth_date))

        # Check if visa is required
        if entry_reason == "VISIT":
            if home_country in visitor_visa_countries:
                # Check that visa is correct format
                traveller_info.append(valid_visa_format(visa_code))
                # Check that visa is up-to-date
                if valid_date_format(visa_date):
                    traveller_info.append(is_more_than_x_years_ago(2, visa_date))

                else:
                    traveller_info.append(False)
            else:
                traveller_info.append(True)

        # Check if traveller should be quarantined
        if from_country in med_advisory_countries:
            traveller_info.append("Quarantine")
        if home_country in med_advisory_countries:
            traveller_info.append("Quarantine")
        else:
            traveller_info.append(True)
        
        # Decide to accept/reject/quarantine
        if "Quarantine" in traveller_info:
            decision.append("Quarantine")
        elif False in traveller_info:
            decision.append("Reject")
        else:
            decision.append("Accept")

    return decision

#decide("test_visitors_with_visas.json", "countries.json")

# CALLING RESULTS OF VALIDATION FUNCTIONS
# Note: Currently we have our Validation Functions set to print "True" or "False" tho clearly
# we want it to return a boolean that will then be used to return "Accept", "Quarantine", "Reject"

# Note: These are the inputs I am currently running but we should create a few more json files for different types of tests.
# decide("test_returning_citizen.json", "countries.json")
