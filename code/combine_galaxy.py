#!/usr/bin/env python

import argparse
import os
from ast import literal_eval
import sqlite3
from sqlite3 import Error
from contsub_imlin import contsub_imlin


file_description = '''
This script combines all the reduced visibilities for a given galaxy to create image cubes
and further advanced products

author: Attila Popping 

see
> python combine_galaxy.py --help
for more information
'''
# the list of all possible configurations that can be combined
all_configs = ['h75', 'h168', 'h214', 'ew352', 'ew367', '750a', '750b', '750c', '750d', '1.5a', '1.5b', '1.5c', '1.5d']
all_configs = str(all_configs)



parser = argparse.ArgumentParser(description=file_description,
                                 usage="combine_galaxy.py",
                                 epilog="last edited 2019")

parser.add_argument("-g", "--galaxy",
                    dest="galaxy",
                    default=None,
                    help="The galaxy to reduce")

parser.add_argument("-r", "--reduce",
                    dest="reduce",
                    default='no',
                    help="whether data should be reduced from raw data [yes / no], default is [no]")


parser.add_argument("-c", "--config",
                    dest="config",
                    default=all_configs,
                    help="configurations to use options are any combination of: " + all_configs)



parser.add_argument("-dd", "--datadir",
                    dest="datadir",
                    default='/Users/attila/work/imagine/rawdata/',
                    help="the directory where the raw observations are stored")

parser.add_argument("-od", "--outdir",
                    dest="outdir",
                    default='/Users/attila/work/imagine/processed/',
                    help="the directory where the data is being processed")

parser.add_argument("-m", "--mode",
                    dest="mode",
                    default='line',
                    help="observing mode: spectral line (line) or continuum (cont)")

parser.add_argument("-o", "--overwrite",
                    dest="overwrite",
                    default='no',
                    help="combined directory can be overwritten if already exists")

parser.add_argument("-ant", "--ant",
                    dest="ant",
                    default='(1,2,3,4,5)',
                    help="antennas to be used for imaging")

parser.add_argument("-p", "--python",
                    dest="pythonpath",
                    default='python',
                    help="The path to the python version to be used")

args = parser.parse_args()

if args.reduce == 'yes':
    # do the data reduction from scratch
    cmd = args.pythonpath + ' reduce_galaxy.py -g ' + args.galaxy + ' -dd ' + args.datadir + \
          ' -od ' + args.outdir + ' -m ' + args.mode + ' -p ' + args.pythonpath
    print('start reducing all the raw data')
    os.system(cmd)


# open the database
code_dir = os.popen('pwd').read()
code_dir = code_dir[:-1].strip('code')
database = code_dir + 'imagineV1.sqlite'
print(database)

try:
    conn = sqlite3.connect(database)
except Error as e:
    print(e)

cur = conn.cursor()
cur.execute("SELECT target, vel, vel_min, vel_max FROM galaxy WHERE target=" + repr(args.galaxy))
obs_val = cur.fetchall()
print(obs_val)
obs_keys = [description[0] for description in cur.description]
obs_par = dict(zip(obs_keys, obs_val[0]))


configs = literal_eval(args.config)

# change to the output directory
os.chdir(args.outdir)
if not os.path.isdir(args.galaxy):
    os.system('mkdir ' + args.galaxy)
os.chdir(args.galaxy)
if not os.path.isdir('combined_' + args.mode):
    os.system('mkdir combined_' + args.mode )
    os.chdir('combined_' + args.mode)
elif args.overwrite == 'yes':
    print('Combined products already exist but will be overwritten')
    os.system('rm -rf combined_' + args.mode + '/*')
    os.chdir('combined_' + args.mode)
else:
    print('Combined product already exist an cannot be overwritten')
    exit()

os.system('mkdir temp_links')
for i in range(len(configs)):
    config = configs[i]
    print(config)
    # make temporary softlinks
    if os.path.isdir('../' + config):
        files = os.listdir('../' + config)
        print(files)
        for j in range(len(files)):
            if args.mode in files[j]:
                if args.mode == 'line':
                    cmd = 'ln -s ' + args.outdir + '/' + args.galaxy + '/' + config + '/' + files[j] + '/' + args.galaxy + '.uvlin temp_links/' + str(i) + str(j) + '.uvlin'
                    print(cmd)
                    os.system(cmd)
                else:
                    cmd = 'ln -s ' + args.outdir + '/' + args.galaxy + '/' + config + '/' + files[j] + '/' + args.galaxy + '.2100 temp_links/' +  str(i) + str(j)+ '.2100'
                    os.system(cmd)



# invert the data into visibilities
#chwidth = [2, 4, 8, 16]
#nchan = [600, 300, 150, 75]
#robust = [-1, 0, 1]
#cellsize = [20, 20, 20]
#imsize = [180, 180, 180]

chwidth = [8, 16]
nchan = [128, 64]
robust = [-1, 1]
cellsize = [10, 10]
imsize = [512, 512]

chwidth = [4]
nchan = [256]
robust = [-1, 1]
cellsize = [10, 10]
imsize = [512, 512]

chwidth = [8]
nchan = [128]
robust = [-1, -0.5, 0.5, 1]
cellsize = [10, 10, 10, 10]
imsize = [512, 512, 512, 512]



os.system('pwd')
os.system('ls')

for i in range(len(robust)):
    if robust[i] < 0:
        rob_str = 'm' + str(abs(robust[i]))
    else:
        rob_str = str(abs(robust[i]))
    vis = 'temp_links/*'
    ant_set = 'ant' + str(args.ant)

    if args.mode == 'cont':
        map = obs_par['target'] + '_' + args.mode + '_rob' + rob_str + '.map'
        beam = obs_par['target'] + '_' + args.mode + '_rob' + rob_str + '.beam'
        # invert the data
        os.system('invert vis=' + vis +
                  ' map=' + map +
                  ' beam=' + beam +
                  ' robust=' + str(robust[i]) +
                  ' imsize=' + str(imsize[i]) +
                  ' cell=' + str(cellsize[i]) +
                  ' stokes=i slop=0.5 options=mfs,mosaic '
                  ' "select=' + ant_set + '"')

        os.system(args.pythonpath + ' ' + code_dir + '/code/autoclean.py ' + map + ' ' + beam + ' ' + args.mode)

    if args.mode == 'line':
        for j in range(len(chwidth)):
            base = obs_par['target'] + '_' + args.mode + '_vel' + str(chwidth[j]) + '_rob' + rob_str
            map =  base + '.map'
            beam = base + '.beam'
            # define the spectral line settings
            vmin = int(obs_par['vel'] - (nchan[j] * chwidth[j] / 2))
            line_set = 'velocity,' + str(nchan[j]) + ',' + str(vmin) + ',' + str(chwidth[j])
            # invert the data
            print('blaaaaaa')
            os.system('pwd')
            print(vis)

            os.system('invert vis=' + vis +
                      ' map=' + map +
                      ' beam=' + beam +
                      ' robust=' + str(robust[i]) +
                      ' imsize=' + str(imsize[i]) +
                      ' cell=' + str(cellsize[i]) +
                      ' stokes=i slop=0.5 options=mosaic '
                      'line=' + line_set +
                      ' select="' + ant_set + '"')


            os.system(args.pythonpath + ' ' + code_dir + '/code/autoclean.py ' + map + ' ' + beam + ' ' + args.mode)
            # do the image based continuum subtraction
            obs_par['base'] = base + '.map'
            args.nchan = nchan[j]
            contsub_imlin(args, obs_par)


















