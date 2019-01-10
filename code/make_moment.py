#!/usr/bin/env python

'''
This script makes basic moment maps of spectral line data
'''

import os


def make_moment(args,obs_par):
    # go to the working directory
    os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])
    os.chdir('temp_data')

    # get an estimate of the noise:
    os.system('imstat in=' + obs_par['target'] + '.imcont log=basic_stats.log options=quaran')

    stat_file = open('basic_stats.log','rt')
    lines = []
    for line in stat_file:
        print('lines : ', lines)
        lines.append(line)

    os.system('rm -rf basic_stats.log')
    stat_line = lines[-1]
    stat_line = stat_line.split(' ')
    stat_val = []
    for h in range(len(stat_line)):
        if stat_line[h] != '':
            stat_val.append(stat_line[h])

    stat_rms = float(stat_val[2])
    clip_value = 7*stat_rms

    # file names with a "-" cause problems in maths (e.g. eso131-010)
    # make a temporary copy
    os.system('cp -r ' + obs_par['target'] + '.imcont temp_image')

    os.system('maths exp=temp_image mask="temp_image.gt.' + str(clip_value) + '" out=temp_mask')
    os.system('moment in=temp_mask out=' + obs_par['target'] + '.mom0 mom=0')
    os.system('moment in=temp_mask out=' + obs_par['target'] + '.mom1 mom=1')
    os.system('moment in=temp_mask out=' + obs_par['target'] + '.peak mom=-2')

    os.system('rm -rf temp_image')
    os.system('rm -rf temp_mask')

    return

