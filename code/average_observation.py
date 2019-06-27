#!/usr/bin/env python


import argparse
import os
import quality_control as qc
import image_data as image
from read_observation_parameters import read_observation_parameters
from read_data import read_data
from rename_data import rename_data
from flag_data import flag_data
from cal_data import cal_data
from contsub_uvlin import contsub_uvlin
from clean_data import basic_clean
from contsub_imlin import contsub_imlin
from make_moment import make_moment

file_description = '''
This script averages the data in the frequency domain for a given observation
sole purpose is to decrease the data volume and increase future processing speed.

see
> python average_observations.py --help
for more information
'''


# Define the input parameters

parser = argparse.ArgumentParser(description=file_description,
                                 usage="imagine_pipeline.py",
                                 epilog="last edited 2019")

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

parser.add_argument("-od", "--outdir",
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
                    default=128,
                    help="number of channels in image cube")

parser.add_argument("-cw", "--chwidth",
                    dest="chwidth",
                    default=8,
                    help="channels width [km/s] in image cube")


parser.add_argument("-is", "--imsize",
                    dest="imsize",
                    default=240,
                    help="spatial size [pixels] of the output image")

parser.add_argument("-cs", "--cellsize",
                    dest="cellsize",
                    default=15,
                    help="pixel size of output image [arcsec]")


parser.add_argument("-r", "--robust",
                    dest="robust",
                    default=1,
                    help="robust values used for image weighting")

args = parser.parse_args()

helpstring = " 'python imagine_pipeline.py --help' "

if args.id != None:
    Id = args.id
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
code_dir = os.popen('pwd').read()
code_dir = code_dir[:-1].strip('code')
database = code_dir + '/' + 'imagineV1.sqlite'
print(database)

obs_par = read_observation_parameters(args, database)
# convert the files into a list
obs_par['files'] = obs_par['files'].replace(' ', '')
obs_par['files'] = obs_par['files'].split(',')
obs_par['code_dir'] = code_dir
