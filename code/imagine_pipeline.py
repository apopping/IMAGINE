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


print(args.datadir)
print(obs_par)

#  Import the raw data
obs_par = read_data(args, obs_par)
print('Data has been imported')
print(obs_par)

#  Correct filenames is needed for (known) exceptional cases
rename_data(args, obs_par)


#  Do the basic flagging of calibrators
if os.path.isdir('1934-638.' + obs_par['freq']):
    flag_data('1934-638.' + obs_par['freq'])
if os.path.isdir('0823-500.' + obs_par['freq']):
    flag_data('0823-500.' + obs_par['freq'])
flag_data(obs_par['phase_cal'] + '.' + obs_par['freq'])


print('Calibrators have been flagged been flagged')

#  Do the calibration
cal_data(args, obs_par)
print('Data has been calibrated')
print(obs_par)

#  Make plots of the calibration tabble
qc.plot_bpass('bpass_table')
qc.plot_phase('phase_table')

# flag the target data
flag_data(obs_par['target'] + '.' + obs_par['freq'])

#  Do the continuum subtraction (uvlin)
if args.mode == 'line':
    contsub_uvlin(args, obs_par)

# do the imaging:
if args.mode == 'line':
    print('Start inverting spectral line data')
    image.invert_spectral_line(args, obs_par)
    print(f"created dirty cube and psf for {obs_par['target']}")

    print('Make a narrowband continuum image based on the spectral line data')
    image.invert_continuum(args, obs_par)
    print(f"created narrowband continuuum dirty map and psf for {obs_par['target']}")

if args.mode == 'cont':
    print('Start inverting spectral line data')
    image.invert_continuum(args, obs_par)
    print(f"created dirty image and psf for {obs_par['target']}")

# do a basic clean
basic_clean(args, obs_par)
print(f"finished cleaning of {obs_par['target']}")

# do the image based continuum subtractio (imlin)
if args.mode == 'line':
    # check whether the cleaning step has actually worked, as there are some cases
    # where it fails as the beam cannot be fitted
    if os.path.isdir(obs_par['target'] + '.clean'):
        print('start image based continuum subtraction')
        contsub_imlin(args, obs_par)
        # make moment maps of the line data
        make_moment(args, obs_par)
    else:
        print('There has been a problem in restoring the cleaned image')
        print('No further proessing is done on deconvolved cubes')

# generate more control plots
qc.plot_uv(args, obs_par)
qc.plot_maps(args, obs_par)

# combine all the files in output file
if args.mode == 'line':
    os.system('gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=log_plots.pdf '
              '*mom*.pdf *bpass_table*.pdf *phase_table*.pdf *time*.pdf')
if args.mode == 'cont':
    os.system('gs -dBATCH -dNOPAUSE -q -sDEVICE=pdfwrite -sOutputFile=log_plots.pdf '
              '*map*.pdf *bpass_table*.pdf *phase_table*.pdf *time*.pdf')

log_name = obs_par['target'] + '_' + args.mode + '_' + obs_par['configuration'] + \
           '_' + obs_par['date'] + '_log.pdf'

print(log_name)
os.system('rm -rf *.ps')
os.system('cp log_plots.pdf ../../' + log_name)


# move the data to its final location:
os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])

if args.mode == 'line':
    os.system('mv temp_data line_' + obs_par['date'])
if args.mode == 'cont':
    os.system('mv temp_data cont_' + obs_par['date'])


# old way of renaming directories:
'''
if args.mode == 'line':
    files = os.listdir('.')
    nruns = [0]
    for file in files:
        if file[0:8] == 'line_run':
            nruns.append(int(file[8]))
    run = max(nruns) + 1
    os.system('mv temp_data line_run' + str(run))


if args.mode == 'cont':
    files = os.listdir('.')
    nruns = [0]
    for file in files:
        if file[0:8] == 'cont_run':
            nruns.append(int(file[8]))
    run = max(nruns) + 1
    os.system('mv temp_data cont_run' + str(run))
'''