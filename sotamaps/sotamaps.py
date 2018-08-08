#!/usr/bin/env python3
import requests
import re
import csv
import os

SOTADATA_ROOT='http://www.sotadata.org.uk'

def get_uniques_for_id(id): 
    return ['OM/BA-002', 'OM/ZA-011']

def translate(item, fields):
    output = {}

    for field in fields:
        if field in item:
            output[field] = item[field]
    return output

def summits_for_callsign(callsign=None):
    
    if callsign is None:
        callsign='4268'

    url = SOTADATA_ROOT + '/myactivatoruniques.aspx?userid=' + str(callsign)
    #url = 'http://www.sotadata.org.uk/myactivatoruniques.aspx?userid=8284'
    r = requests.get(url)
    items = re.findall(r'<td class="gridcell" align="center">\d+</td><td class="gridcell">([^<]+)', r.text, re.DOTALL)
    
    item_pairs = map(lambda x: re.findall(r'^([^ ]+) \((.+)\)$', x)[0], items)

    summits = list(map(lambda x: x[0], item_pairs))

    #print(summits)

    summits_with_details = []

    current_dir = os.path.dirname(__file__)

    with open(os.path.join(current_dir, 'summitslist.csv')) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            if 'SummitCode' in row:
                if row['SummitCode'] in summits:
                    summits_with_details.append(row)

    exported_fields = [ 'SummitCode', 'Latitude', 'Longitude', 'SummitName', 'AltM' ]

    out = map(lambda x: translate(x, exported_fields), summits_with_details)
    return list(out)

def user_id_for_callsign(callsign):
    pass

if __name__ == '__main__':
    print(list(summits_for_callsign()))
