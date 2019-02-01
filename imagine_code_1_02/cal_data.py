#!/usr/bin/env python

'''
This script will do the calibration
'''

import os


def cal_data(args, obs_par):
    # go to the working directory
    os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])
    os.chdir('temp_data')
    #files = os.listdir()
    #freq = files[0][-4:]

    #for file in files:
    #    if obs_par['target'] in file:
    #        freq = file.strip(obs_par['target'] + '.')
    #        print(freq)



    if os.path.exists('1934-638.' + obs_par['freq']):
        if os.path.exists('0823-500.' +  obs_par['freq']):
            #  they both exist, check which to use
            size1934 = os.popen('du -s 1934-638*').read()
            size1934 = float(size1934.split()[0])
            size0823 = os.popen('du -s 0823-500*').read()
            size0823 = float(size0823.split()[0])
            if size1934 > size0823:
                os.system('cp -r 1934-638.' + obs_par['freq'] + ' bpass_table')
            else:
                os.system('cp -r 0823-500.' + obs_par['freq'] + ' bpass_table')

        else:
            os.system('cp -r 1934-638.' + obs_par['freq'] + ' bpass_table')
    elif os.path.exists('0823-500' + obs_par['freq']):
        os.system('cp -r 0823-500.' + obs_par['freq'] + ' bpass_table')
    else:
        print('ERROR: there is no calibrator !!')

    os.system('cp -r ' + obs_par['phase_cal'] + '.' + obs_par['freq'] + ' phase_table')

    os.system('mfcal vis=bpass_table  interval=5 options=interpolate')
    if obs_par['project'] == 'C1545' \
            or obs_par['project'] == 'C968' \
            or obs_par['project'] == 'CX062' \
            or obs_par['project'] == 'C1341':
        os.system('gpcal vis=bpass_table interval=0.1 options=nopol,noxy')
    else:
        os.system('gpcal vis=bpass_table interval=0.1 options=xyvary') #FLAGGING  IN HERE

    os.system('gpcopy vis=bpass_table  out= phase_table')
    os.system('gpcal vis=phase_table interval=0.1 options=xyvary,qusolve')
    os.system('gpboot vis=phase_table cal=bpass_table')
    os.system('gpcopy vis=phase_table out=' + obs_par['target'] + '.' + obs_par['freq'])


    return


def cal_data_cont(args, obs_par):
    # go to the working directory
    os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])
    os.chdir('temp_data')
    #files = os.listdir()
    #freq = files[0][-4:]

    #for file in files:
    #    if obs_par['target'] in file:
    #        freq = file.strip(obs_par['target'] + '.')
    #        print(freq)



    if os.path.exists('1934-638.' + obs_par['freq']):
        if os.path.exists('0823-500.' +  obs_par['freq']):
            #  they both exist, check which to use
            size1934 = os.popen('du -s 1934-638*').read()
            size1934 = float(size1934.split()[0])
            size0823 = os.popen('du -s 0823-500*').read()
            size0823 = float(size0823.split()[0])
            if size1934 > size0823:
                os.system('cp -r 1934-638.' + obs_par['freq'] + ' bpass_table')
            else:
                os.system('cp -r 0823-500.' + obs_par['freq'] + ' bpass_table')

        else:
            os.system('cp -r 1934-638.' + obs_par['freq'] + ' bpass_table')
    elif os.path.exists('0823-500' + obs_par['freq']):
        os.system('cp -r 0823-500.' + obs_par['freq'] + ' bpass_table')
    else:
        print('ERROR: there is no calibrator !!')

    os.system('cp -r ' + obs_par['phase_cal'] + '.' + obs_par['freq'] + ' phase_table')

    os.system('mfcal vis=bpass_table  interval=0.1')
    if obs_par['project'] == 'C1545' \
            or obs_par['project'] == 'C968' \
            or obs_par['project'] == 'CX062' \
            or obs_par['project'] == 'C1341':
        os.system('gpcal vis=bpass_table interval=0.1 options=nopol,noxy')
    else:
	#could have an option which makes code fully automatic ie. ignores blflag but for now hash them out
#	os.system('blflag vis=bpass_table device=/xs axis=chan,amp options=nofqav,nobase stokes=xx,yy') #bandpass calibation and flagging
	os.system('pgflag vis=bpass_table device=/xs command=\<b stokes=i,v,q,u flagpar=8,5,5,3,6,3 options=nodisp')
	os.system('pgflag vis=bpass_table device=/xs command=\<b stokes=i,v,u,q flagpar=8,5,5,3,6,3 options=nodisp')
        os.system('pgflag vis=bpass_table device=/xs command=\<b stokes=i,q,u,v flagpar=8,5,5,3,6,3 options=nodisp')
        os.system('pgflag vis=bpass_table device=/xs command=\<b stokes=u,v,q,i flagpar=8,5,5,3,6,3 options=nodisp') 
        os.system('gpcal vis=bpass_table interval=0.1 options=xyvary nfbin=4') #FLAGGING IN HERE
#	os.system('blflag vis=bpass_table device=/xs axis=real,imag options=nofqav,nobase stokes=xx,yy')
	os.system('gpcal vis=bpass_table interval=0.1 options=xyvary,reset nfbin=4')

    os.system('gpcopy vis=bpass_table  out=phase_table')
    os.system('gpcal vis=phase_table interval=0.1 options=xyvary,qusolve,reset nfbin=4')
 #   os.system('blflag vis=phase_table device=/xs axis=chan,amp options=nofqav,nobase stokes=xx,yy')
    os.system('pgflag vis=phase_table device=/xs command=\<b stokes=i,v,q,u flagpar=8,5,5,3,6,3 options=nodisp')
    os.system('pgflag vis=phase_table device=/xs command=\<b stokes=i,v,u,q flagpar=8,5,5,3,6,3 options=nodisp')
    os.system('pgflag vis=phase_table device=/xs command=\<b stokes=i,q,u,v flagpar=8,5,5,3,6,3 options=nodisp')
    os.system('pgflag vis=phase_table device=/xs command=\<b stokes=u,v,q,i flagpar=8,5,5,3,6,3 options=nodisp')
    os.system('gpcal vis=phase_table interval=0.1 options=xyvary,qusolve,reset nfbin=4')
 #   os.system('blflag vis=phase_table device=/xs axis=chan,amp options=nofqav,nobase stokes=xx,yy')
 #   os.system('blflag vis=phase_table device=/xs axis=real,imag options=nofqav,nobase stokes=xx,yy') 
    #could add a while loop for the flagging.... but it would only be the blflagging parts and would need manual intervention
    os.system('gpcal vis=phase_table interval=0.1 options=xyvary,qusolve,reset nfbin=4')
    os.system('gpboot vis=phase_table cal=bpass_table')
    os.system('gpcopy vis=phase_table out=' + obs_par['target'] + '.' + obs_par['freq'])
    os.system('pgflag vis='+ obs_par['target']+ '.' + obs_par['freq']+ ' device=/xs command=\<b stokes=i,v,q,u flagpar=8,5,5,3,6,3 options=nodisp') 
    os.system('pgflag vis='+ obs_par['target']+ '.' + obs_par['freq']+ ' device=/xs command=\<b stokes=i,v,u,q flagpar=8,5,5,3,6,3 options=nodisp')
    os.system('pgflag vis='+ obs_par['target']+ '.' + obs_par['freq']+ ' device=/xs command=\<b stokes=i,q,u,v flagpar=8,5,5,3,6,3 options=nodisp')
    os.system('pgflag vis='+ obs_par['target']+ '.' + obs_par['freq']+ ' device=/xs command=\<b stokes=u,v,q,i flagpar=8,5,5,3,6,3 options=nodisp')

    return

