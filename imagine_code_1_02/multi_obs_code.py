#import argparse 
import os
#from imagine_pipeline import * 
from parameters import parameter_call
#from imagine_pipeline import flag_cal_load
from image_data import invert_continuum
from image_data import invert_spectral_line
from read_data import read_data
from clean_data import basic_clean




#manually input the files names in sql file (imagineV1) and set the id's which the different galaxy obs dates below
id=['2','3' ,'5','6']

for i in range(0,len(id)):
	os.system('python imagine_pipeline.py -i '+ id[i])


args,obs_par= parameter_call()


if args.mode=='line':
	invert_spectral_line(args,obs_par)
else:
	invert_continuum(args,obs_par)



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

basic_clean(args,obs_par)

