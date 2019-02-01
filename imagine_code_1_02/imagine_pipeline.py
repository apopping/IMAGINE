#!/usr/bin/env python

file_description ='''
This is the main pipeline to reduce ATCA data,
in particular data from the IMAGINE survey:
Imaging Galaxies Intergalactic and Nearby Environment

author: Attila Popping 

The script requires either and 'id' number that is used
to extract the relevant parameters from the observations database
Alternatively a 'target', 'configuration', and 'date' can be given
to reduce a particular observation

see
> python imagine_pipeline.py --help
for more information
'''

import argparse
import os
import quality_control as qc
import image_data as image
from read_observation_parameters import read_observation_parameters
from read_data import read_data
from flag_data import flag_data
from cal_data import cal_data
from cal_data import cal_data_cont
from contsub_uvlin import contsub_uvlin
from clean_data import basic_clean
from contsub_imlin import contsub_imlin
from make_moment import make_moment
from parameters import parameter_call



args, obs_par=parameter_call()
#def flag_cal_load(args,obs_par):   
#  Import the raw data



read_data(args,obs_par)
print('Data has been imported')


#  Do the basic flagging

flag_data(args, obs_par)
print('Data has undergone basic flagging')
#  Do the calibration
print(obs_par)

if args.mode=='line': #Caleb change: I have made a cal_data_cont function in the cal_data file, it is the same as the original one except with some flagging woven into the code. 
    cal_data(args, obs_par)
else:
    cal_data_cont(args, obs_par)

print('Data has been calibrated')



#  Make plots of the calibration tabble
if args.mode=='line':
    qc.plot_cal('bpass_table')
    qc.plot_cal('phase_table')
else:
    qc.plot_cal_cont('bpass_table')
    qc.plot_cal_cont('phase_table')


'''
   #  Do the continuum subtraction (uvlin)
   if args.mode == 'line':
       contsub_uvlin(args, obs_par)

   # do the imaging:
   if args.mode == 'line':
       print('Start inverting spectral line data')
       image.invert_spectral_line(args,obs_par)
       print("created dirty cube and psf for {obs_par['target']}")

       print('Make a narrowband continuum image based on the spectral line data')
       image.invert_continuum(args, obs_par)
       print("created narrowband continuuum dirty map and psf for {obs_par['target']}")



#   if args.mode == 'cont':
#       print('Start inverting spectral line data')
#       image.invert_continuum(args,obs_par)
#       print("created dirty image and psf for {obs_par['target']}")


   # do a basic clean
#   basic_clean(args,obs_par)
#   print("finished cleaning of {obs_par['target']}")


   # do the image based continuum subtractio (imlin)
#   if args.mode == 'line':
#       print('start image based continuum subtraction')
#       contsub_imlin(args, obs_par)



   # make moment maps of the line data
#   if args.mode == 'line':
#       make_moment(args, obs_par)

   # generate more control plots
   #qc.plot_uv(args, obs_par)
   #qc.plot_maps(args, obs_par)

   # move the data to its final location:
   os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])


   if args.mode == 'line':
       files = os.listdir()
       nruns = [0]
       for file in files:
           if file[0:8] == 'line_run':
               nruns.append(int(file[8]))
       run = max(nruns) + 1
       os.system('mv temp_data line_run' + str(run))
   if args.mode == 'cont':
       files = os.listdir()
       nruns = [0]
       for file in files:
           if file[0:8] == 'cont_run':
            nruns.append(int(file[8]))
       run = max(nruns) + 1
       os.system('mv temp_data cont_run' + str(run))

'''

