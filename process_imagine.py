# pipeline to reduce IMAGINE data
# Attila Popping


# process_imagine.py par_name process_root

from read_parameters import read_parameters
from pre_conditions import pre_conditions
from read_data import read_data
from basic_flag import basic_flag
from object_info import object_info
from band_phase_cal import band_phase_cal
from cont_uvlin import cont_uvlin
from basic_clean import basic_clean
from control_plots import control_plots
import os
import sys
import ast


#
# process_imagine.py input.par process_dir

###########################################
##### Check whether input is correct ######
###########################################
if sys.argv[1:]:
    par_name=sys.argv[1]
    print 'Parameter file to be used: ', par_name
else:
    print 'No parameter file is given'
    exit(1)

if sys.argv[2:]:
    process_dir = sys.argv[2]
    print 'Processing data in: ', process_dir
else:
    process_dir = '/mnt/science1/imagine/processed/'
    #process_dir = '/Users/attila/work/imagine/processed/'
    print 'No process directory given'
    print 'Using default: ', process_dir


###########################
####  Read Parameters  ####
###########################
# read the parameter file to get all the input parameters
if sys.argv[1:]:
    par_name=sys.argv[1]
    print par_name
    par = read_parameters(par_name)
else:
    print 'No parameter is given'

print 'the parameters are:'
print par
print par['files']
# rename par['files'] to a more useful format
files = par['files']
files.replace("\n","")
files.replace(" ","")
files = ast.literal_eval(par['files'])
par['files'] = files
print par['files']
par['par_name'] = par_name
#################################
##### Read precondition #########
#################################
par = pre_conditions(par)



#####################################
####  Change to target directory ####
#####################################
#os.chdir(par['process_dir'])
os.chdir(process_dir)

if os.path.isdir(par['target']) == False:
    os.system('mkdir ' + par['target'])
os.chdir(par['target'])
if os.path.isdir(par['configuration']) == False:
    os.system('mkdir ' + par['configuration'])
os.chdir(par['configuration'])
os.system('mkdir tmp')
os.chdir('tmp')

###################################
####  Import the raw data #########
###################################
print 'Start importing data'
read_data(par)


################################################
#### Determine the objects and frequencies #####
################################################
# skip this for now
#print 'Getting object information'
#object_info(par)

###############################################
#### Do the basic flagging ####################
###############################################

print 'Do the first basic flagging steps'
basic_flag(par)

###############################################
#### Do the calibration #######################
###############################################
print 'Do the calibration'
par = band_phase_cal(par)

##############################################
#### Do the continuum subtraction (uvlin) ####
##############################################
print 'Do the continuum subtraction (uvlin)'
cont_uvlin(par)

##############################################
#### Do basic imaging and cleaning ###########
##############################################
print 'Do the imaging and first cleaning'
basic_clean(par)

##############################################
#### Plots for quality control ###############
##############################################
print 'make plots for quality control'
control_plots(par)

##############################################
#### Cleanup #################################
##############################################
os.system('rm -rf ../*' + par['par_name_short'] + '*' )
os.system('mv *' + par['par_name_short'] + '* ../.')
os.chdir('../')
os.system('rm -rf tmp')
