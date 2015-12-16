# !/usr/bin/env python3

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

# Not sure if necessary, but do use some
#for traveller in traveller_entry_records:
#    passport_number = traveller['passport']
#    first_name = traveller['first_name']
#    last_name = traveller['last_name']
#    home = traveller['home']['country']
#    birth_date = traveller['birth_date']
#    entry_reason = traveller['entry_reason']
#    entry_from = traveller['from']['country']


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

    #removes any passport incorrectly using underscores as \w will pass this type of character
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
    valid_date_format_regex = re.compile(r'\d\d\d\d-\d\d-\d\d')
    valid_date_match = valid_date_format_regex.search(date_string)

    #Currently this only works for birth date
    if valid_date_match is None:
        print "False"
    else:
        #To ensure the D.O.B. is not in the future.
        if is_more_than_x_years_ago(0, date_string):
            print "True"
        else:
            print "False"

valid_date_format("1958-07-07")

def valid_visa_format(visa_code):
    """
    Checks whether a visa code is two groups of five alphanumeric characters
    :param visa_code: alphanumeric string
    :return: Boolean; True if the format is valid, False otherwise

    """
    #NOTE: VISAS MAY BE MORE COMPLEX REQUIRING ALL TO BE UNIQUE CHARACTERS. PUTTING A QUESTION ON BB TO SEE...
    visa_regex = re.compile(r'\w\w\w\w\w-\w\w\w\w\w')
    visa_match = visa_regex.search(visa_code)

    #removes any visa incorrectly using underscores as \w will pass this type of character
    if "_" in visa_code:
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

    #This opens the json files passed into the function allowing multiple json test files to be run.
    with open(input_file, "r") as file_reader:
        traveller_file_contents = file_reader.read()

    traveller_entry_records = json.loads(traveller_file_contents)

    with open(countries_file, "r") as file_reader:
        country_list = file_reader.read()

    country_list_info = json.loads(country_list)

#TESTING FOR COMPLETENESS
#Clearly there will be a value in using separate validation functions for passport, visa and birth date
# numbers. Whether we will want to do so for things like name and such (which is relatively simple)
# or just keep that stuff here in the main function is up us as a group.

#Checks that all required fields are not empty
    #does this by creating a list of required fields and then running through
    #that list and seeing if it is blank for a traveller's record

    for traveller in traveller_entry_records:
        #print traveller
        traveller_info = []
        traveller_info.append(traveller)
        #print traveller_info

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

        required_fields = []
        required_fields = [passport_number, first_name, last_name, birth_date, home_city, home_region,\
                           home_country, entry_reason, from_city, from_region, from_country]



        for field in required_fields:
            if field == "":
                processing_step_1 = False
                break
            else:
                processing_step_1 = True


        #If all required fields are filled in then checks that countries are recognized as valid countries
            #does this by checking if the home_country and from_country of the traveller's json file are
            # are a key in the dictionary of countries

        if processing_step_1 == True:
            if home_country and from_country in country_list_info.keys():
                processing_step_2 = True
            else:
                processing_step_2 = False

            #THis is not needed in actual program, just checking it if is correct
            if processing_step_2 == True:
                print (first_name + " info is filled in and has a valid countries listed ")
            else:
                print (first_name + "info is either does not have valid countries listed")

#CALLING RESULTS OF VALIDATION FUNCTIONS
#Note: Currently we have our Validation Functions set to print "True" or "False" tho clearly
#we want it to return a boolean that will then be used to return "Accept", "Quarantine", "Reject"

    for passport in traveller_entry_records:
        testing_passport = (passport["passport"])
        valid_passport_format(testing_passport)

    for passport in traveller_entry_records:
        testing_birth_date = (passport["birth_date"])
        valid_date_format(testing_birth_date)

#Note: These are the inputs I am currently running but we should create a few more json files for different types of tests.
decide("test_returning_citizen.json", "countries.json")

# Below is Jessica's psuedocode organizing an order to check the program.
# Check required info for completeness
# Check first/ last name
#   if incomplete
#   return reject
# Check DOB
#   if incomplete
#     return reject
# Check passport number
#   if incomplete
#     return reject
# Check location (home)
#   if incomplete
#     return reject
# Check location (travelling from)
#   if incomplete
#     return reject
# Check reason for entry
#   if incomplete
#     reject

# Check location
#   if location = unknown
#     return reject
#   elif:
#   location = KAN
#     return accept
#    for traveller in traveller_entry_records:
#        if traveller['home']['country'] == "KAN":
#            print("Accept")
#        else:
        # placeholder to see if working
#            print ("Not home country")
        # else:
        # keep going

        # if reason_for_entry = visit and visitor_visa_required = 1
        # must have visa and visa must be less than two years
        # else:
        # return reject
# Check visa
#  if reason for entry is visit
#    if country on passport requires visa
#      check visa is proper format
#      check visa date is proper format (can likely reuse birthday date check function for this)
#      check visa is less than 2 years old #    for traveller in traveller_entry_records:
#        if traveller['entry_reason'] == "visit":
#            for country in country_list_info:
#                if country_list_info[country]['transit_visa_required'] == "1":
#                    print traveller
#                    break
#                else:
#                    print "No visa required"
# Check Quarantine
#  if home country on passport has medical advisory
#    then quarantine
#  elif country travelling through has medical advisory
#    then quarantine

#med_advisory_countries = []
#for country in country_list_info:
#     #print country_list_info[country]['medical_advisory']
#     if country_list_info[country]['medical_advisory'] == "":
#         print "No med adv"
#     else:
#         print country_list_info[country]['medical_advisory']
#         med_advisory_countries.append(country)

#print med_advisory_countries

#for traveller in traveller_entry_records:
#    if traveller['from']['country'] in med_advisory_countries:
#        print "quarantine"
#    else:
#        print ("no quarantine required")

                # If from[country] has warning then
                # return quarantine




                # return ["Reject"]
