#!/usr/bin/env python

'''
This script does continuum subtraction in the image domain using contsub
'''

import os


def contsub_imlin(args,obs_par):
    # go to the working directory
    # os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])
    # os.chdir('temp_data')



    # read the header and get freqeuncy information
    if obs_par['base']:
        base = obs_par['base']
    else:
        base = obs_par['target']

    os.system('gethd in=' + base + '.clean/crval3 > crval3.log')
    os.system('gethd in=' + base + '.clean/cdelt3 > cdelt3.log')


    crval_file = open('crval3.log', 'rt')
    for line in crval_file:
        crval = line
    crval = float(crval.strip('\n'))

    cdelt_file = open('cdelt3.log', 'rt')
    for line in cdelt_file:
        cdelt = line
    cdelt = float(cdelt.strip('\n'))

    vmax = crval + args.nchan * cdelt

    # the velocity range of the target
    line_vmin = obs_par['vel_min']
    line_vmax = obs_par['vel_max']


    # the velocity range of milky way
    mw_vmin = -200
    mw_vmax = 200

    print('crval', crval)
    print('cdelt', cdelt)
    print(line_vmin)
    print(line_vmax)

    # check whether the MW is in the data:
    if crval < mw_vmin and line_vmin > mw_vmax:
        chan1 = 1
        chan2 = int((mw_vmin-crval)/cdelt)
        chan3 = int((mw_vmax-crval)/cdelt)
        chan4 = int((line_vmin-crval)/cdelt)
        chan5 = int((line_vmax-crval)/cdelt)
        chan6 = args.nchan
        cont_chan = '(' + str(chan1) + ',' + str(chan2) + '),(' + str(chan3) + ',' + str(chan4) \
                    + '),(' + str(chan5) + ',' + str(chan6) + ')'

    if crval < mw_vmin and line_vmin < mw_vmax:
        chan1 = 1
        chan2 = int((mw_vmin-crval)/cdelt)
        chan3 = int((line_vmax-crval)/cdelt)
        chan4 = args.nchan
        cont_chan = '(' + str(chan1) + ',' + str(chan2) + '),(' + str(chan3) + ',' + str(chan4) + ')'


    elif crval > mw_vmin and crval < mw_vmax:
        chan1 = int((mw_vmax-crval)/cdelt)
        chan2 = int((line_vmin-crval)/cdelt)
        chan3 = int((line_vmax-crval)/cdelt)
        chan4 = args.nchan
        cont_chan = '(' + str(chan1) + ',' + str(chan2) + '),(' + str(chan3) + ',' + str(chan4) + ')'
    elif crval > mw_vmax:
        chan1 = 1
        chan2 = int((line_vmin-crval)/cdelt)
        chan3 = int((line_vmax-crval)/cdelt)
        chan4 = args.nchan
        cont_chan = '(' + str(chan1) + ',' + str(chan2) + '),(' + str(chan3) + ',' + str(chan4) + ')'


    print(cont_chan)

    incube = base + '.clean'
    outcube = base + '.imcont'

    os.system('contsub in=' + incube + ' out=' + outcube + ' contchan="' + cont_chan + '" mode=poly,1')

    return