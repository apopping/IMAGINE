#!/usr/bin/env python

'''
This script will flag the data
'''

import os

#def flag_data(args, obs_par):
    ## go to the working directory
    #os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])
    #os.chdir('temp_data')
    #files = os.listdir()

    #for file in files:
    #    print(f"flagging : {file}")
    #    os.system('uvflag vis=' + file + ' edge=20 flagval=flag')
    #    os.system('uvflag vis=' + file + ' select="shadow(25)" flagval=flag')
    #    #os.system('tvclip vis=' + file + ' clip=6 options=notv commands=diff,clip')
    #    os.system('pgflag vis=' + file + ' stokes=ii command="<be" flagpar="2,5,3,3,5,3,20" options=nodisp'

def flag_data(file):

    print(f"flagging : {file}")
    os.system('uvflag vis=' + file + ' edge=20 flagval=flag')
    os.system('uvflag vis=' + file + ' select="shadow(25)" flagval=flag')
    os.system('tvclip vis=' + file + ' clip=5 options=notv commands=diff,clip')
    os.system('pgflag vis=' + file + ' stokes=ii command="<be" flagpar="5,5,3,3,5,3,20" options=nodisp')



    return
