#!/usr/bin/env python3
"""
Module that contains functions dealing with Maidenhead grid squares
"""

import math
import re

l1 = 'abcdefghijklmnopqr'
l2 = '0123456789'
l3 = 'abcdefghijklmnopqrstuvx'
gridsquare_reg = '^[A-R]{2}\d{2}([a-x]{2})?$'
gridsquare_subreg = '([A-R]{2}\d{2}[a-x]{2})'
R = 6371e3 # earth radius

def is_gridsquare(text):
    if isinstance(text, str):
        if re.match(gridsquare_reg, text, re.IGNORECASE):
            return True
    return False

def extract_gridsquare(text):
    # find a gridsquare as a substring of a string
    match = re.search(gridsquare_subreg, text, re.DOTALL | re.IGNORECASE)
    if match:
        return match.groups()[0]
    return None

def small_square_distance(sq1, sq2):
    # calculate small grid square distance for contest (small square = JN88)
    sq1 = sq1.lower() 
    sq2 = sq2.lower() 

    if len(sq1) < 6 or len(sq2) < 6:
        return -1

    x1 = (l1.index(sq1[0]) + 1)*10 + int(sq1[2:4])//10 + 1
    x2 = (l1.index(sq2[0]) + 1)*10 + int(sq2[2:4])//10 + 1

    y1 = (l1.index(sq1[1]) + 1)*10 + int(sq1[2:4]) % 10 + 1
    y2 = (l1.index(sq2[1]) + 1)*10 + int(sq2[2:4]) % 10 + 1

    x_max = len(l1)*len(l2)
    y_max = len(l1)*len(l2)

    dist_x_direct = abs(x1 - x2)
    dist_x_indirect = abs((x_max - x1) - (x_max - x2))
    dist_x = min(dist_x_direct, dist_x_indirect)

    dist_y_direct = abs(y1 - y2)
    dist_y_indirect = abs((y_max - y1) - (y_max - y2))
    dist_y = min(dist_y_direct, dist_y_indirect)

    return max(dist_x, dist_y)

def gridsquare2latlng(gridsquare):
    # get gridsquare center latlng (returns one (lat,lng))
    ((from_lat, from_lng),(to_lat, to_lng)) = gridsquare2latlngedges(gridsquare)
    center_lng = from_lng + (to_lng - from_lng)/2
    center_lat = from_lat + (to_lat - from_lat)/2

    return (center_lat, center_lng)

def gridsquare2latlngedges(gridsquare):
    # Convert gridsquares to lat and long and returns top/left, bottom/right ((lat,lng),(lat,lng))
    # Works for 4-character squares and 6-character squares

    from_lat, from_lng, stop_lat, stop_lng = 0,0,0,0

    ONE = gridsquare[0:1]
    TWO = gridsquare[1:2]
    THREE = gridsquare[2:3]
    FOUR = gridsquare[3:4]
    FIVE = gridsquare[4:5]
    SIX = gridsquare[5:6]
   
    # longitude
    Field = ((ord(ONE.lower()) - 97.0) * 20.0) 
    Square = int(THREE) * 2

    if FIVE:
        SubSquareLow = (ord(FIVE.lower()) - 97.0) * (2.0/24.0)
        SubSquareHigh = SubSquareLow + (2.0/24.0)
    else:
        SubSquareLow = 0
        SubSquareHigh = 2.0


    from_lng = Field + Square + SubSquareLow - 180
    to_lng = Field + Square + SubSquareHigh - 180

    # latitute
    Field = ((ord(TWO.lower()) - 97.0) * 10.0) 
    Square = int(FOUR)

    if SIX:
        SubSquareLow = (ord(SIX.lower()) - 97) * (1.0/24.0)
        SubSquareHigh = SubSquareLow + (1.0/24.0)
    else:
        SubSquareLow = 0
        SubSquareHigh = 1.0

    from_lat = Field + Square + SubSquareLow - 90.0
    to_lat = Field + Square + SubSquareHigh - 90.0
    
    return ((from_lat, from_lng), (to_lat, to_lng))

def dist_haversine(param1, param2):
    # Standard implementation of haversine algorithm, guess operands 
    # so that we can work with both gridsquares and latlng tuples.

    if type(param1) is tuple:
        (lat1, lng1) = param1
    else:
        (lat1, lng1) = gridsquare2latlng(param1)

    if type(param2) is tuple:
        (lat2, lng2) = param2
    else:
        (lat2, lng2) = gridsquare2latlng(param2)

    (phi1, phi2) = (math.radians(lat1), math.radians(lat2))

    delta_phi = math.radians(lat2-lat1)
    delta_lambda = math.radians(lng2-lng1)

    a = (math.sin(delta_phi/2))**2 + math.cos(phi1) * math.cos(phi2) * (math.sin(delta_lambda/2))**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    # distance is in meters so return it in km
    distance = R * c / 1000;

    return distance

def dist_ham(*args):
    # just use haversine with some "bulgarian" constants

    distance = dist_haversine(*args)
    return int(distance) + 1

if __name__ == '__main__':
    print(gridsquare2latlng('JN88oj'))
