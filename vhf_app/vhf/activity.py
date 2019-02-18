#!/usr/bin/env python3
import sys
import geopy.distance

from .adif import Adif
from .gridsquare import gridsquare2latlng, small_square_distance


class Qso:
    def __init__(self, adif_vars):
        # init qso object from adif_vars (dictionary)
        for key, value in adif_vars.items():
            setattr(self, key.lower(), value)
            

class Log:
    def __init__(self, gridsquare=None, adif_file=None):
        self.qsos = []

        if adif_file is not None:
            self.init_from_adif(adif_file)
        
        # init my gridsquare from self qsos
        for qso in self.qsos:
            if hasattr(qso, 'my_gridsquare'):
                self.gridsquare = qso.my_gridsquare
                break

        # override gridsquare if given in argument instead of looking
        # for it in the adif 
        if gridsquare is not None:
            self.gridsquare = gridsquare
        
        self.latlng = gridsquare2latlng(self.gridsquare)

        # calculate distances
        for qso in self.qsos:
            qso.distance = round(geopy.distance.distance(self.latlng, qso.latlng).km)


    def init_from_adif(self, adif_file):
        adif = Adif(from_file=adif_file)
        adif.guess_gridsquares()

        for item in adif.qsos:
            qso = Qso(item['adif_vars'])
            
            if hasattr(qso, 'gridsquare') and qso.gridsquare:
                qso.latlng = gridsquare2latlng(qso.gridsquare)

            self.qsos.append(qso)

        self.qsos.sort(key = lambda x: (x.qso_date, x.time_on))

    def scores(self):
        # return all the scores
        def points(point_distance):
            return 2 + point_distance

        orig_qsos = {}
        orig_gridsquares = {}
        orig_large_gridsquares = {}
        
        # my own gridsquare is a natural multiplier
        orig_gridsquares[self.gridsquare] = 1
        
        for qso in self.qsos:
            orig_qsos[qso.call] = qso.gridsquare
            orig_gridsquares[qso.gridsquare] = orig_gridsquares.get(qso.gridsquare, 0) + 1
            orig_large_gridsquares[qso.gridsquare[0:4]] = orig_large_gridsquares.get(qso.gridsquare[0:4], 0) + 1

        # compute scores
        score = 0
        max_dist = 0
        locator_max = '' 

        for qth in orig_qsos.values():
            dist = small_square_distance(self.gridsquare, qth)
            score += points(dist)
            if dist > max_dist:
                max_dist = dist
                locator_max = qth

        scores = {
            'original_qso_count' : len(orig_qsos.values()),
            'multiplier_count' : len(orig_large_gridsquares.keys()),
            'score' : score,
            'score_multiplied':score*len(orig_large_gridsquares.keys()),
            'max_gridsquare' : locator_max
        }
        return scores

        
if __name__ == '__main__':
    if len(sys.argv) > 1:
        log = Log('JN88le', sys.argv[1])
        print('My square: %s' % log.gridsquare)
        for qso in log.qsos:
            print(qso.call)
