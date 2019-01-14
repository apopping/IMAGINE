#!/usr/bin/env python

'''
This script will flag the data
'''

import os

def rename_data(args, obs_par):
    # go to the working directory
    os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])
    os.chdir('temp_data')
    files = os.listdir()

    if obs_par['target'] == 'ngc7793':
        if os.path.isdir('pnt.1419.2'):
            os.system('mv pnt.1419.2 ngc7793.1419.2')
        if os.path.isdir('1934-638.1416.7'):
            os.system('mv 1934-638.1416.7 1934-638.1419.2')
    if obs_par['target'] == 'ngc1744' and os.path.isdir('pnt.1419.2'):
        os.system('mv pnt.1419.2 ngc1744.1416.7')
        obs_par['freq'] = '1416.7'

    return obs_par