from os import path
from webbrowser import get
import requests
import json
import phonenumbers
from phonenumbers.phonenumberutil import region_code_for_number

witness   = {}
witnesses = []

def get_reports():
    url = 'https://api.fbi.gov/wanted/v1/list'
    response  = requests.get(url)
    data = json.loads(response.text)
    return data['items']

# Checks if title can be found in FBI DB
def title_check(title):

    data = get_reports() #getting new data just in case something changed on their side in meantine
    for report in data:

            if report['title'] == title.upper().strip():

                return True, report
                
    return False, {}


def create_file_reports(title, number, country_code):

    pn            = True
    tn, report    = title_check(title) #checking as someone could delete that record in meantime even though I populated select with data from API call
    match         = True

    # Minimum and maximum length required for a number and if it could be parsed
    if len(number) < 4 or len(number) > 19 or not phonenumbers.parse(number) or not phonenumbers.is_valid_number(phonenumbers.parse(number)) or not phonenumbers.is_possible_number(phonenumbers.parse(number)):

        pn = False
        
        return pn, tn, 0, match

    # To see if number is valid or possible

    region = region_code_for_number(phonenumbers.parse(number))
    
    
    if not tn:
        #baci exception za neispravan title
        return pn, tn, 0, match
    

    match = True if region == country_code else False

    witness = {
                "report"                 : report, #saving whole report - as it says in task, but saving memory, and space, we could only save uid and retrieve it when needed by that uid
                "number"                 : number,
                "country_code_by_number" : region,
                "country_code_by_ip"     : country_code,
                "number_and_ip_match"    : match
                }

    if witness not in witnesses:
        witnesses.append(witness)
        witn = open("witness.json", "w")
        json.dump(witnesses, witn, indent=4)
        witn.close()
    
    return pn, tn, 0, match

