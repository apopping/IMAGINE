#!/usr/bin/env python

'''
This script has a number of functions to do quality control
'''

import os
import os.path


def plot_cal(cal_table):
    os.system('mkdir sol_images')
    os.system('gpplt vis=' + cal_table + ' yaxis=amp nxy="3,2" device=sol_images/' + cal_table + '_amp.ps/cps')
    os.system('gpplt vis=' + cal_table + ' yaxis=phase nxy="3,2" device=sol_images/' + cal_table + '_phase.ps/cps')

    #os.system('gpplt vis=' + phase_table + ' yaxis=amp nxy="3,2" select="-ant(6)" device=phase_amp.ps/cps')
    #os.system('gpplt vis=' + phase_table + ' yaxis=phase nxy="3,2" select="-ant(6)" device=phase_phase.ps/cps')

    return
def plot_cal_cont(cal_table):
    os.system('mkdir sol_images')
    os.system('gpplt vis=' + cal_table + ' options=bandpass device=sol_images/' + cal_table + '_amp.ps/cps')
    os.system('gpplt vis=' + cal_table + ' yrange=-200,200 yaxis=ph device=sol_images/' + cal_table + '_phase.ps/cps')


def plot_uv(args, obs_par):
    # go to the working directory
    os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])
    os.chdir('temp_data')

    if args.mode == 'line':
        vis = obs_par['target'] + '.uvlin'
    if args.mode == 'cont':
        vis = obs_par['target'] + '.' + obs_par['freq']

    uu_vv_device = obs_par['target'] + '_uu_vv.ps/cps'
    ha_amp_device = obs_par['target'] + '_ha_amp.ps/cps'
    time_amp_device = obs_par['target'] + '_time_amo.ps/cps'
    antset = 'ant' + str(args.ant)

    os.system('uvplt vis=' + vis +
              ' select=' + antset +
              ' stokes=ii average=5 options=nobase axis=uu,vv ' +
              'device=' + uu_vv_device)

    os.system('uvplt vis=' + vis +
              ' select=' + antset +
              ' stokes=ii average=5 options=nobase axis=hangle,amp ' +
              'device=' + ha_amp_device)

    os.system('uvplt vis=' + vis +
              ' select=' + antset +
              ' stokes=ii average=5 options=nobase axis=time,amp ' +
              'device=' + time_amp_device)


    return


def plot_maps(args, obs_par):
    # make plots of the different maps created during the processing
    # copy the optical image:

    #check whether optical image exists:
    fitsfile = '/Users/attila/work/imagine/IMAGINE/optical/' + obs_par['target'] + '_dss_blue.fits'
    if os.path.isfile(fitsfile):
        mirfile = args.outdir + obs_par['target'] + '/' + obs_par['configuration'] + '/temp_data/dss_blue.mir'
        os.system('fits in=' + fitsfile + ' out=' + mirfile + ' op=xyin')
        if args.mode == 'line':
            mom0_in = obs_par['target'] + '.mom0'
            mom0_out = obs_par['target'] + '.mom0.re'
            mom1_in = obs_par['target'] + '.mom1'
            mom1_out = obs_par['target'] + '.mom1.re'
            os.system('regrid in=' + mom0_in + ' out=' + mom0_out + ' tin=dss_blue.mir axes=1,2')
            os.system('regrid in=' + mom1_in + ' out=' + mom1_out + ' tin=dss_blue.mir axes=1,2')

            os.system('cgdisp in=' + obs_par['target'] + '.mom0.re type=pixel device=plot_mom0.ps/cps')
            os.system('cgdisp in=' + obs_par['target'] + '.mom1.re type=pixel device=plot_mom0.ps/cps')
            os.system('cgdisp in=dss_blue.mir,' + obs_par['target'] + '.mom0.re type=pixel,contour device=contour_mom0.ps/cps')
            os.system('cgdisp in=dss_blue.mir,' + obs_par['target'] + '.mom1.re type=pixel,contour device=contour_mom0.ps/cps')


    return
