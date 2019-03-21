#!/usr/bin/env python3
import sys
import re

class Adif:
    def __init__(self, from_file=None, from_string=None):

        self.qsos = []

        if from_string is not None:
            self.init_from_string(from_string)
        elif from_file is not None:
            self.init_from_file(from_file)

    def init_from_file(self, adif_file):
        with open(adif_file) as f:
            data = f.read()
        self.init_from_string(data)

    def init_from_string(self, adif_string):
        # ignore header
        data = re.sub("^.*<EOH>", "", adif_string, flags=re.IGNORECASE)
        items = [ item.strip() for item in re.split("<EOR>", data, flags=re.IGNORECASE) ]

        # process QSOs
        for item in items:
            # process QSO variables
            # ADIF = <variable_name:length>value\s - and substring the value according to
            # length. This should probably be read sequentially, not as a regexp. (value with < will probably suck)
            variables = re.findall('<(\w+):(\d+)>([^<]+)', item)
            adif_vars = dict((var[0].upper(), var[2][:int(var[1])]) for var in variables)
        
            # variable postprocessing
            
            # 1. some software puts SRX and STX to _STRING variables. Attempt to extract these.
            if ('SRX' not in adif_vars 
                and 'STX' not in adif_vars
                and 'SRX_STRING' in adif_vars
                and 'STX_STRING' in adif_vars):

                stx = re.findall('^(\d+)', adif_vars['STX_STRING'])
                srx = re.findall('^(\d+)', adif_vars['SRX_STRING'])

                if stx and srx:
                    adif_vars['STX'] = stx[0]
                    adif_vars['SRX'] = srx[0]

            if 'CALL' in adif_vars:
                self.qsos.append({'adif_vars': adif_vars})


if __name__ == '__main__':
    if len(sys.argv) > 1:
        adif = Adif(from_file=sys.argv[1])

        for qso in adif.qsos:
            print(qso['adif_vars'].get('CALL'))
            
    else:
        print("Please supply filename as an argument")

    
    
