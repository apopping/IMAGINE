#!/usr/bin/env python

'''
This script has a number of functions to do quality control
'''

import os
import os.path
import subprocess


def plot_bpass(cal_table):
    os.system('gpplt vis=' + cal_table + ' yaxis=amp nxy="3,2" options=bandpass device=' + cal_table + '_amp.ps/cps')
    os.system('gpplt vis=' + cal_table + ' yaxis=phase nxy="3,2" options=bandpass device=' + cal_table + '_phase.ps/cps')

    cmd = 'ps2pdf ' + cal_table + '_amp.ps ' + cal_table +  '_amp.pdf'
    subprocess.call(cmd, shell=True)
    cmd = 'ps2pdf ' + cal_table + '_phase.ps ' + cal_table +  '_phase.pdf'
    subprocess.call(cmd, shell=True)

    return

def plot_phase(cal_table):
    os.system('gpplt vis=' + cal_table + ' yaxis=amp nxy="3,2" device=' + cal_table + '_amp.ps/cps')
    os.system('gpplt vis=' + cal_table + ' yaxis=phase nxy="3,2" device=' + cal_table + '_phase.ps/cps')

    cmd = 'ps2pdf ' + cal_table + '_amp.ps ' + cal_table +  '_amp.pdf'
    subprocess.call(cmd, shell=True)
    cmd = 'ps2pdf ' + cal_table + '_phase.ps ' + cal_table +  '_phase.pdf'
    subprocess.call(cmd, shell=True)

    return


def plot_uv(args, obs_par):
    # go to the working directory
    os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])
    os.chdir('temp_data')

    if args.mode == 'line':
        vis = obs_par['target'] + '.uvlin'
    if args.mode == 'cont':
        vis = obs_par['target'] + '.' + obs_par['freq']

    time_amp_device = obs_par['target'] + '_time_amp.ps/cps'
    time_rms_device = obs_par['target'] + '_time_rms.ps/cps'

    antset = 'ant' + str(args.ant)



    os.system('uvplt vis=' + vis +
              ' select="' + antset + '"' +
              ' stokes=ii average=5 options=nobase axis=time,amp'  +
              ' device=' + time_amp_device)

    os.system('uvstat vis=' + vis +
              ' select="' + antset + '"' +
              ' stokes=ii axes=time,rms'  +
              ' device=' + time_rms_device)

    cmd = 'ps2pdf ' + obs_par['target'] + '_time_amp.ps ' + obs_par['target'] + '_time_amp.pdf'
    subprocess.call(cmd, shell=True)
    cmd = 'ps2pdf ' + obs_par['target'] + '_time_rms.ps ' + obs_par['target'] + '_time_rms.pdf'
    subprocess.call(cmd, shell=True)

    return


def plot_maps(args, obs_par):
    # make plots of the different maps created during the processing
    # copy the optical image:

    #check whether optical image exists:
    fitsfile = '/Users/attila/work/imagine/IMAGINE/optical/' + obs_par['target'] + '_dss_blue.fits'
    fitsfile = '/home/apopping/imagine/IMAGINE/optical/' + obs_par['target'] + '_dss_blue.fits'
    fitsfile = obs_par['code_dir'] + '/optical/' + obs_par['target'] + '_dss_blue.fits'

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
            os.system('cgdisp in=' + obs_par['target'] + '.mom1.re type=pixel device=plot_mom1.ps/cps')
            os.system('cgdisp in=dss_blue.mir,' + obs_par['target'] + '.mom0.re type=pixel,contour device=contour_mom0.ps/cps')
            os.system('cgdisp in=dss_blue.mir,' + obs_par['target'] + '.mom1.re type=pixel,contour device=contour_mom1.ps/cps')

            cmd = 'ps2pdf plot_mom0.ps plot_mom0.pdf'
            subprocess.call(cmd, shell=True)
            cmd = 'ps2pdf plot_mom1.ps plot_mom1.pdf'
            subprocess.call(cmd, shell=True)
            cmd = 'ps2pdf contour_mom0.ps contour_mom0.pdf'
            subprocess.call(cmd, shell=True)
            cmd = 'ps2pdf contour_mom1.ps contour_mom1.pdf'
            subprocess.call(cmd, shell=True)
    return