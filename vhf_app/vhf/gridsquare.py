#!/usr/bin/env python3

l1 = 'abcdefghijklmnopqr'
l2 = '0123456789'
l3 = 'abcdefghijklmnopqrstuvx'
l2 = '0123456789'

def small_square_distance(sq1, sq2):
    # calculate small grid square distance for contest
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
    # convert gridsquares to lat and long
    from_lat, from_lng, stop_lat, stop_lng = 0,0,0,0

    ONE = gridsquare[0:1]
    TWO = gridsquare[1:2]
    THREE = gridsquare[2:3]
    FOUR = gridsquare[3:4]
    FIVE = gridsquare[4:5]
    SIX = gridsquare[5:6]
   
    # lon
    Field = ((ord(ONE.lower()) - 97.0) * 20.0) 
    Square = int(THREE) * 2
    SubSquareLow = (ord(FIVE.lower()) - 97.0) * (2.0/24.0)
    SubSquareHigh = SubSquareLow + (2.0/24.0)

    from_lng = Field + Square + SubSquareLow - 180
    to_lng = Field + Square + SubSquareHigh - 180

    # lat
    Field = ((ord(TWO.lower()) - 97.0) * 10.0) 
    Square = int(FOUR)
    SubSquareLow = (ord(SIX.lower()) - 97) * (1.0/24.0)
    SubSquareHigh = SubSquareLow + (1.0/24.0)

    from_lat = Field + Square + SubSquareLow - 90.0
    to_lat = Field + Square + SubSquareHigh - 90.0

    center_lng = from_lng + (to_lng - from_lng)/2
    center_lat = from_lat + (to_lat - from_lat)/2
    
    #return (from_lat, from_lng, to_lat, to_lng)
    return (center_lat, center_lng)

if __name__ == '__main__':
    print(gridsquare2latlng('JN88oj'))
