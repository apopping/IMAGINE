# a function to do the bandpass and phase calibration
import os
import commands

def band_phase_cal(par):

    par_name = par['par_name'].split('/')[-1].split('.')[-2]
    print par['par_name']
    print par_name

    bpass_table = 'bandpass_cal_' + par_name
    phase_table = 'phase_cal_' + par_name

    os.system('cp -r ' + par['phase_cal'] + '.aver ' + phase_table)


    # check which source to use as the bandpass calibrator:
    if os.path.exists(par['band_cal1']) == True and os.path.exists(par['band_cal2']) == False:
        os.system('cp -r ' + par['band_cal1'] + '.aver ' + bpass_table)
    elif os.path.exists(par['band_cal1']) == False and os.path.exists(par['band_cal2']) == True:
        os.system('cp -r ' + par['band_cal2'] + '.aver ' + bpass_table)
    else:
        size1 = commands.getoutput('du -sh '+ par['band_cal1']).split()[0]
        print size1
        size1 = float(size1[0:-1])
        size2 = commands.getoutput('du -sh '+ par['band_cal2']).split()[0]
        size2 = float(size2[0:-1])
        print 'find biggest file'
        print size1
        print size2
        if size1 > size2:
            os.system('cp -r ' + par['band_cal1'] + '.aver ' + bpass_table)
        else:
            os.system('cp -r ' + par['band_cal2'] + '.aver ' + bpass_table)

    os.system('mfcal vis=' + bpass_table + ' interval=5 options=interpolate')
    if par['project'] == 'C1545' or par['project'] == 'C968':
        os.system('gpcal vis=' + bpass_table + ' interval=0.1 options=nopol,noxy')
    else:
        os.system('gpcal vis=' + bpass_table + ' interval=0.1 options=xyvary')

    os.system('gpcopy vis=' + bpass_table + '  out=' + phase_table)
    os.system('gpcal vis=' + phase_table + ' interval=0.1 options=xyvary')
    os.system('gpboot vis=' + phase_table + ' cal=' + bpass_table)

    os.system('gpcopy vis=' + phase_table + ' out=' + par['source'] + '.aver')
    par['par_name_short'] = par_name

    return par
