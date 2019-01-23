#!/usr/bin/env python

'''
This script will do the calibration
'''

import os


def cal_data(args, obs_par):
    # go to the working directory
    os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])
    os.chdir('temp_data')

    if os.path.exists('1934-638.' + obs_par['freq']) and os.path.exists('0823-500.' +  obs_par['freq']):
        #  they both exist, check which to use
        size1934 = os.popen('du -s 1934-638*').read()
        size1934 = float(size1934.split()[0])
        size0823 = os.popen('du -s 0823-500*').read()
        size0823 = float(size0823.split()[0])
        if size1934 > size0823:
            os.system('cp -r 1934-638.' + obs_par['freq'] + ' bpass_table')
        else:
            os.system('cp -r 0823-500.' + obs_par['freq'] + ' bpass_table')

    elif os.path.exists('1934-638.' + obs_par['freq']) and not os.path.exists('0823-500.' + obs_par['freq']):
        os.system('cp -r 1934-638.' + obs_par['freq'] + ' bpass_table')
    elif not os.path.exists('1934-638.' + obs_par['freq']) and  os.path.exists('0823-500.' + obs_par['freq']):
        os.system('cp -r 0823-500.' + obs_par['freq'] + ' bpass_table')
    else:
        print('ERROR: there is no calibrator !!')

    os.system('cp -r ' + obs_par['phase_cal'] + '.' + obs_par['freq'] + ' phase_table')

    os.system('mfcal vis=bpass_table  interval=5 options=interpolate')
    if obs_par['project'] == 'C1545' \
            or obs_par['project'] == 'C968' \
            or obs_par['project'] == 'CX062' \
            or obs_par['project'] == 'C1341':
        os.system('gpcal vis=bpass_table interval=0.1 options=nopol,noxy')
    else:
        os.system('gpcal vis=bpass_table interval=0.1 options=xyvary')

    os.system('gpcopy vis=bpass_table  out= phase_table')
    os.system('gpcal vis=phase_table interval=0.1 options=xyvary')
    os.system('gpboot vis=phase_table cal=bpass_table')
    os.system('gpcopy vis=phase_table out=' + obs_par['target'] + '.' + obs_par['freq'])

    return
