# a function to import ATCA observations into miriad
import os

def read_data(par):
    files = par['files']
    print 'Files to be processed:'
    print files

    for i in range(0,len(files),1):
        print 'Working on : ', files[i]
        #os.system('rm -rf ' + files[i])
        #os.system('mkdir ' + files[i])
        #os.chdir(files[i])
        copy_file = par['data_dir'] + files[i] + '.' + par['project']
        print copy_file
        os.system('cp -r ' + copy_file + ' .')



    command = 'atlod in=*.' + par['project'] + ' out=data  ifsel=' + par['if'] + ' restfreq=1.420405752 options=bary,birdie,rfiflag,noauto edge=0'

    print command
    os.system(command)
    os.system('uvindex vis=data log=' + files[i] + '.log')
    os.system('uvsplit vis=data options=mosaic')
    os.system('rm -rf data')


    # correct for differences based on different projects:
    if par['project'] == 'C1528' and par['target'] == 'ngc24':
        os.system('mv src02.' + str(par['frequency']) + ' ngc24.' + str(par['frequency']))
    if par['project'] == 'C1179' and par['target'] == 'ngc24':
        os.system('mv ngc0024.' + str(par['frequency']) + ' ngc24.' + str(par['frequency']))
    if par['project'] == 'C3041' and par['target'] == 'ngc625' and par['configuration'] == 'h214':
        os.system('mv 1934-638.1417.2 1934-638.' + str(par['frequency']))
    if par['project'] == 'C3041' and par['target'] == 'eso154-023':
        os.system('mv eso154-g023.' + str(par['frequency']) + ' eso154-023.' + str(par['frequency']))
    if par['project'] == 'C968' and par['target'] == 'ngc625':
        os.system('mv ngc.' + str(par['frequency']) + ' ngc625.' + str(par['frequency']))

    if par['project'] == 'CX294' and par['target'] == 'eso154-023':
        os.system('mv eso154-g023.' + str(par['frequency']) + ' eso154-023.' + str(par['frequency']))
    if par['project'] == 'CX062' and par['target'] == 'eso154-023':
        os.system('mv eso154-g23.' + str(par['frequency']) + ' eso154-023.' + str(par['frequency']))
    if par['project'] == 'C1341' and par['target'] == 'eso154-023':
        os.system('mv e154.' + str(par['frequency']) + ' eso154-023.' + str(par['frequency']))    

    # get channel information
    command = 'prthd in=' + par['source'] + '> header.log'
    os.system(command)
    head_file = open('header.log','rt')
    lines = []
    for line in head_file:
        print 'lines : ', lines
        lines.append(line)

    os.system('rm -rf header.log')
    header = lines[14][0:-4]
    header = header.split(' ')
    freq_set = []
    for h in range(len(header)):
        if header[h] != '':
            freq_set.append(float(header[h]))

    chans = freq_set[1]
    chan_1 = freq_set[2]
    increment = freq_set[3]

    print 'print frequency settings:'
    print 'chans', chans
    print 'chan_1',chan_1
    print 'increment', increment

    if chans > 2048:
        out_chan = int(chans/24)
        line_set = 'channel,' + str(out_chan) + ',1,24,24'
    else:
        out_chan = chans
        line_set = 'channel,' + str(out_chan) + ',1,1,1'


    #average the data
    os.system('uvaver vis=' + par['band_cal1'] + '  line=' + line_set + ' out=' + par['band_cal1'] + '.aver ')
    os.system('uvaver vis=' + par['band_cal2'] + '  line=' + line_set + ' out=' + par['band_cal2'] + '.aver ')
    os.system('uvaver vis=' + par['phase_cal'] + '  line=' + line_set + ' out=' + par['phase_cal'] + '.aver ')
    os.system('uvaver vis=' + par['source'] + '  line=' + line_set + ' out=' + par['source'] + '.aver ')

    return
