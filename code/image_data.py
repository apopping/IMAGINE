#!/usr/bin/env python

'''
This script makes a dirty image of the data
'''
import os



def invert_spectral_line(args, obs_par):
    # go to the working directory
    os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])
    os.chdir('temp_data')

    # define the file names
    vis = obs_par['target'] + '.uvlin'
    map = obs_par['target'] + '.map'
    beam = obs_par['target'] + '.beam'

    ant_set = 'ant'+ str(args.ant)

    # define the spectral line settings
    vmin = int(obs_par['vel'] - (args.nchan * args.chwidth / 2))
    line_set = 'velocity,' + str(args.nchan) + ',' + str(vmin) + ',' + str(args.chwidth)

    # invert the data
    os.system('invert vis=' + vis +
              ' map=' + map +
              ' beam=' + beam +
              ' robust=' + str(args.robust) +
              ' imsize=' + str(args.imsize) +
              ' cell=' + str(args.cellsize) +
              ' stokes=i slop=0.5 options=mosaic '
              'line=' + line_set +
              ' "select=' + ant_set + '"')

    #command = 'invert vis=' + vis + ' map=' + map + ' beam=' + beam + ' robust=1 imsize=256 cell=20 stokes=i slop=0.5 options=mosaic line=' + line_set + ' "select=' + ant_set + '"'


    return



def invert_continuum(args, obs_par):
    # go to the working directory
    os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])
    os.chdir('temp_data')

    # define the file names for the standard continuum data reduction
    vis = obs_par['target'] + '.' + obs_par['freq']
    map = obs_par['target'] + '.map'
    beam = obs_par['target'] + '.beam'


    # if the continuum is narrowband from the spectral line data, change the names
    if os.path.isdir(obs_par['target'] + '.uvcon'):
        vis = obs_par['target'] + '.uvcon'
        map = obs_par['target'] + '.cmap'
        beam = obs_par['target'] + '.cbeam'

    ant_set = 'ant'+ str(args.ant)

    # invert the data
    os.system('invert vis=' + vis +
              ' map=' + map +
              ' beam=' + beam +
              ' robust=' + str(args.robust) +
              ' imsize=' + str(args.imsize) +
              ' cell=' + str(args.cellsize) +
              ' stokes=i slop=0.5 options=mfs,mosaic '
              ' "select=' + ant_set + '"')

    # invert the data
    #command = 'invert vis=' + vis + ' map=' + map + ' beam=' + beam + ' robust=1 imsize=256 cell=20 stokes=i slop=0.5 options=mfs,mosaic'

    #print(command)
    #os.system(command)


    return

