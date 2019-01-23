#!/usr/bin/env python

'''
This script does continuum subtraction in the uv domain, using uvlin
'''

import os


def contsub_uvlin(args, obs_par):
    cmd = None
    # go to the working directory
    os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])
    os.chdir('temp_data')

    # read the header and get freqeuncy information
    print('prthd in=' + obs_par['target'] + '.' + obs_par['freq'] + ' > header.log')
    os.system('prthd in=' + obs_par['target'] + '.' + obs_par['freq'] + ' > header.log')

    head_file = open('header.log', 'rt')
    lines = []
    for line in head_file:
        lines.append(line)

    header = lines[14][0:-4]
    header = header.split(' ')
    freq_set = []
    for h in range(len(header)):
        if header[h] != '':
            freq_set.append(float(header[h]))

    chans = freq_set[1]
    chan_1 = freq_set[2]
    increment = freq_set[3]

    print('print frequency settings:')
    print('chans', chans)
    print('chan_1', chan_1)
    print('increment', increment)

    # calculate the frequency range of the target
    line_fmin = 1.42041 - (obs_par['vel_min']/300000.0)
    line_fmax = 1.42041 - (obs_par['vel_max']/300000.0)

    # calculate frequency range of milky way
    mw_fmin = 1.42041 - (-200/300000.0)
    mw_fmax = 1.42041 - (200/300000.0)

    # check whether the MW is in the data:
    if chan_1 > mw_fmin:
        chan1 = 1
        chan2 = int((mw_fmin - chan_1) / increment)
        chan3 = int((mw_fmax - chan_1) / increment)
        chan4 = int((line_fmin - chan_1) / increment)
        chan5 = int((line_fmax - chan_1) / increment)
        chan6 = chans
        cont_chan = str(chan1) + ',' + str(chan2) + ',' + str(chan3) + ',' + str(chan4) + \
                    ',' + str(chan5) + ',' + str(chan6)
    elif chan_1 < mw_fmin and chan_1 > mw_fmax:
        chan1 = (mw_fmax - chan_1) / increment
        chan2 = int((line_fmin - chan_1) / increment)
        chan3 = int((line_fmax - chan_1) / increment)
        chan4 = chans
        cont_chan = str(chan1) + ',' + str(chan2) + ',' + str(chan3) + ',' + str(chan4)
    elif chan_1 < mw_fmax:
        chan1 = 1
        chan2 = int((line_fmin - chan_1) / increment)
        chan3 = int((line_fmax - chan_1) / increment)
        chan4 = chans
        cont_chan = str(chan1) + ',' + str(chan2) + ',' + str(chan3) + ',' + str(chan4)

    # make continuum subtracted line data
    cmd = 'uvlin vis=' + obs_par['target'] + '.' + obs_par['freq'] + \
              ' out=' + obs_par['target'] + '.uvlin  mode=line chans=' + cont_chan
    os.system(cmd)

    # make also store the continuuum data in an averaged channel
    cmd = 'uvlin vis=' + obs_par['target'] + '.' + obs_par['freq'] + \
              ' out=' + obs_par['target'] + '.uvcon  mode=continuum chans=' + cont_chan
    os.system(cmd)

    return





