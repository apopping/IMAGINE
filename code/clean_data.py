#!/usr/bin/env python

'''
This script does a basic and blind clean in two iterations
A shallow clean and a deeper clean using a mask.
'''

import os


def basic_clean(args,obs_par):
    # go to the working directory
    os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])
    os.chdir('temp_data')

    vis = obs_par['target'] + '.uvlin'
    map = obs_par['target'] + '.map'
    beam = obs_par['target'] + '.beam'
    model = obs_par['target'] + '.model'
    clean1 = obs_par['target'] + '.clean'


    # the data has been inverted from vis to image in a previous step, start with the deconvolution
    os.system('mossdi map=' + map +
              ' beam=' + beam +
              ' out=' + model +
              ' niters=500 gain=0.1')

    os.system('restor map=' + map +
              ' beam=' + beam +
              ' model=' + model +
              ' out=' + clean1 +
              ' mode=clean')

    # clean the narrowband continuum if it exists
    if os.path.isdir(obs_par['target'] + '.uvcon'):
        cvis = obs_par['target'] + '.uvcon'
        cmap = obs_par['target'] + '.cmap'
        cbeam = obs_par['target'] + '.cbeam'
        cmodel = obs_par['target'] + '.cmodel'
        cclean1 = obs_par['target'] + '.cclean'

        # the data has been inverted from vis to image in a previous step, start with the deconvolution
        os.system('mossdi map=' + cmap +
                  ' beam=' + cbeam +
                  ' out=' + cmodel +
                  ' niters=500 gain=0.1')

        os.system('restor map=' + cmap +
                  ' beam=' + cbeam +
                  ' model=' + cmodel +
                  ' out=' + cclean1 +
                  ' mode=clean')

    return