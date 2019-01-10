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
from contsub_uvlin import contsub_uvlin
from clean_data import basic_clean
from contsub_imlin import contsub_imlin
from make_moment import make_moment


# Define the input parameters

parser = argparse.ArgumentParser(description=file_description,
                                 usage = "imagine_pipeline.py",
                                 epilog = "last edited 2018")

# argument: files to process


parser.add_argument("-i", "--id",
                    dest="id",
                    default=None,
                    type=int,
                    help="the observation id, if this is given (PREFERED) all other information is extracted\n"
                         "form the database and further user arguments are ignored")

parser.add_argument("-dd", "--datadir",
                    dest="datadir",
                    default='/Users/attila/work/imagine/rawdata/',
                    help="the directory where the raw observations are stored")

parser.add_argument("--od", "--outdir",
                    dest="outdir",
                    default='/Users/attila/work/imagine/processed/',
                    help="the directory where the data is being processed")

parser.add_argument("-t", "--target",
                    dest="target",
                    default=None,
                    help="the target galaxy")

parser.add_argument("-c", "--configuration",
                    dest="config",
                    default=None,
                    help="the configuration")

parser.add_argument("-d", "--date",
                    dest="date",
                    default=None,
                    help="the date of the observation, if no date is given all available observations will be used")

parser.add_argument("-p", "--path",
                    dest="datadir",
                    default='/Users/attila/work/imagine/rawdata/',
                    help="the directory of the raw data")

parser.add_argument("-av", "--average",
                    dest="aver",
                    default=24,
                    type=int,
                    help="number of spectral channels to average")

parser.add_argument("-m", "--mode",
                   dest="mode",
                   default='line',
                   help="observing mode: spectral line (line) or continuum (cont)")

parser.add_argument("-ant", "--ant",
                    dest="ant",
                    default='(1,2,3,4,5)',
                    help="antennas to be used for imaging")

parser.add_argument("-nc", "--nchan",
                    dest="nchan",
                    default=250,
                    help="number of channels in image cube")

parser.add_argument("-cw", "--chwidth",
                    dest="chwidth",
                    default=4,
                    help="channels width [km/s] in image cube")


parser.add_argument("-is", "--imsize",
                    dest="imsize",
                    default=256,
                    help="spatial size [pixels] of the output image")

parser.add_argument("-cs", "--cellsize",
                    dest="cellsize",
                    default=20,
                    help="pixel size of output image [arcsec]")


parser.add_argument("-r", "--robust",
                    dest="robust",
                    default=1,
                    help="robust values used for image weighting")





args = parser.parse_args()
#observation = args.obs
#print(observation)

helpstring = " 'python imagine_pipeline.py --help' "



if args.id != None:
    id = args.id
    print(f"start working on observation: {id}")
else:
    print('No observation ID is given, extracting info from user input')
    # check whether input is given
    if args.target is None:
        print(f"the target is not given, see {helpstring}")
        exit()
    if args.config is None:
        print(f"the configuration is not given, see {helpstring}")
        exit()


if args.mode != 'line' and args.mode != 'cont':
    print(f'no valid mode is given (specatral line or continuum), see {helpstring}')
    exit()

# read the relevant observing parameters
# path on my local machine
database = '/Users/attila/work/imagine/IMAGINE/imagineV1.sqlite'
# path on ICRAR system
database = '/mnt/science1/imagine/code/IMAGINE-master/code/imagineV1.sqlite'
obs_par = read_observation_parameters(args,database)

# manual edit during development
obs_par['files'] = '2018-09-28_0532.C3157, 2018-09-28_0608.C3157'

# convert the files into a list
obs_par['files'] = obs_par['files'].replace(' ','')
obs_par['files'] = obs_par['files'].split(',')

print(args.datadir)
print(obs_par)

#  Import the raw data
read_data(args,obs_par)
print('Data has been imported')



#  Do the basic flagging
flag_data(args, obs_par)
print('Data has been flagged')

#  Do the calibration
cal_data(args, obs_par)
print('Data has been calibrated')

#  Make plots of the calibration tabble
qc.plot_cal('bpass_table')
qc.plot_cal('phase_table')

#  Do the continuum subtraction (uvlin)
if args.mode == 'line':
    contsub_uvlin(args, obs_par)

# do the imaging:
if args.mode == 'line':
    print('Start inverting spectral line data')
    image.invert_spectral_line(args,obs_par)
    print(f"created dirty cube and psf for {obs_par['target']}")

    print('Make a narrowband continuum image based on the spectral line data')
    image.invert_continuum(args, obs_par)
    print(f"created narrowband continuuum dirty map and psf for {obs_par['target']}")



if args.mode == 'cont':
    print('Start inverting spectral line data')
    image.invert_continuum(args,obs_par)
    print(f"created dirty image and psf for {obs_par['target']}")



# do a basic clean
basic_clean(args,obs_par)
print(f"finished cleaning of {obs_par['target']}")


# do the image based continuum subtractio (imlin)
if args.mode == 'line':
    print('start image based continuum subtraction')
    contsub_imlin(args, obs_par)



# make moment maps of the line data
if args.mode == 'line':
    make_moment(args, obs_par)


# generate more control plots
qc.plot_uv(args, obs_par)
qc.plot_maps(args, obs_par)







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

