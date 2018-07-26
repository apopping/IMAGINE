# a function to do the first default flagging steps
import os




def basic_flag(par):

    os.system('uvflag vis=' + par['band_cal1'] + '.aver edge=20 flagval=flag')
    os .system('uvflag vis=' + par['band_cal1'] + '.aver select="shadow(25)" flagval=flag')
    os.system('tvclip vis=' + par['band_cal1'] + '.aver  clip=6 options=notv commands=diff,clip')

    os.system('uvflag vis=' + par['band_cal2'] + '.aver edge=20 flagval=flag')
    os .system('uvflag vis=' + par['band_cal2'] + '.aver select="shadow(25)" flagval=flag')
    os.system('tvclip vis=' + par['band_cal2'] + '.aver  clip=6 options=notv commands=diff,clip')

    os.system('uvflag vis=' + par['phase_cal'] + '.aver edge=20 flagval=flag')
    os .system('uvflag vis=' + par['phase_cal'] + '.aver select="shadow(25)" flagval=flag')
    os.system('tvclip vis=' + par['phase_cal'] + '.aver  clip=6 options=notv commands=diff,clip')

    os.system('uvflag vis=' + par['source'] + '.aver edge=20 flagval=flag')
    os .system('uvflag vis=' + par['source'] + '.aver select="shadow(25)" flagval=flag')
    os.system('tvclip vis=' + par['source'] + '.aver  clip=6 options=notv commands=diff,clip')

    return
