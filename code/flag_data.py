#!/usr/bin/env python

'''
This script will flag the data
'''

import os


def flag_data(file):
    print(f"flagging : {file}")
    os.system('uvflag vis=' + file + ' edge=20 flagval=flag')
    os.system('uvflag vis=' + file + ' select="shadow(25)" flagval=flag')
    os.system('tvclip vis=' + file + ' clip=5 options=notv commands=diff,clip')
    os.system('pgflag vis=' + file + ' stokes=ii command="<be" flagpar="4,5,3,3,5,3,20" options=nodisp')

    return
