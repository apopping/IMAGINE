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

    if obs_par['target'] == 'ngc7090':
        if os.path.isdir('1934-638.1416.2'):
            os.system('mv 1934-638.1416.2 1934-638.1415.2')
            obs_par['freq'] = '1415.2'

    if obs_par['target'] == 'ngc7793':
        if os.path.isdir('pnt.2100'):
            os.system('mv pnt.2100 ngc7793.2100')
        if os.path.isdir('pnt.1419.2'):
            os.system('mv pnt.1419.2 ngc7793.1419.2')
            obs_par['freq'] = '1419.2'
        if os.path.isdir('1934-638.1416.7'):
            os.system('mv 1934-638.1416.7 1934-638.1419.2')
            obs_par['freq'] = '1419.2'

    if obs_par['target'] == 'ngc1744':
        if os.path.isdir('pnt.2100'):
            os.system('mv pnt.2100 ngc1744.2100')
        if os.path.isdir('pnt.1419.2'):
            os.system('mv pnt.1419.2 ngc1744.1416.7')
            obs_par['freq'] = '1416.7'
        if os.path.isdir('0438-436.1419.2'):
            os.system('mv 0438-436.1419.2 0438-436.1416.7')
            obs_par['freq'] = '1416.7'
        if os.path.isdir('pnt.1419.5'):
            os.system('mv pnt.1419.5 ngc1744.1419.5')


    if obs_par['target'] == 'eso154-023':
        if os.path.isdir('eso154-023.1418'):
            os.system('mv eso154-023.1418 eso154-023.1417.7')
            obs_par['freq'] = '1417.7'


    return obs_par