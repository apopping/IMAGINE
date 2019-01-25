#!/usr/bin/env python

import argparse
import os
import sqlite3
from sqlite3 import Error

file_description = '''
This script opens the sql database for IMAGINE and reduces all the observations for a given galaxy

author: Attila Popping 

see
> python reduce_galaxy.py --help
for more information


steps:




'''


parser = argparse.ArgumentParser(description=file_description,
                                 usage="reduce_galaxy.py",
                                 epilog="last edited 2019")


parser.add_argument("-g", "--galaxy",
                    dest="galaxy",
                    default=None,
                    help="The galaxy to reduce")


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



args = parser.parse_args()

helpstring = " 'python reduce_galaxy.py --help' "

# check whether a galaxy is given
if args.galaxy is None:
    print(f"No galaxy is given given, see {helpstring}")
    exit()

# open the database
code_dir = os.popen('pwd').read()
code_dir = code_dir[:-1].strip('code')
database = code_dir + '/' + 'imagineV1.sqlite'
print(database)

try:
    conn = sqlite3.connect(database)
except Error as e:
    print(e)

cur = conn.cursor()
cur.execute("SELECT id FROM observation WHERE target=" + repr(args.galaxy))
IDs = cur.fetchall()
for i in range(len(IDs)):
    ID = str(IDs[i][0])
    print(f"start reducing ID: {ID}")
    cmd = 'python imagine_pipeline.py -i ' + ID + ' -dd ' + args.datadir + ' -od ' + args.outdir + ' -m ' + args.mode
    print(f"finished reducing ID: {ID}")
    os.system(cmd)









