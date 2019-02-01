#!/usr/bin/env python

'''
This script will check whether data exists and import it to be further processed
'''

import os


def aver_line_set(file, aver):
    # define the line setttings when averaging a file
    # file = filename
    # aver = number of channels to average

    # read the number of channels:
    cmd = 'prthd in=' + file + '> header.log'
    os.system(cmd)
    head_file = open('header.log', 'rt')
    lines = []
    for line in head_file:
        print(f'lines : {line}')
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

    print('print frequency settings:')
    print(f'chans {chans}')
    print(f'chan_1 {chan_1}')
    print(f'increment {increment}')

    out_chan = int(chans/aver)
    line_set = 'channel,' + str(out_chan) + ',1,' + str(aver) + ',' + str(aver)

    return line_set


def read_data(args, obs_par):
    cmd = None
    # create the work directory in case it does not exist:
    if not os.path.isdir(args.outdir):
        os.system('mkdir ' + args.outdir)
    os.chdir(args.outdir)
    if not os.path.isdir(obs_par['target']):
        os.system('mkdir ' + obs_par['target'])
    os.chdir(obs_par['target'])
    if not os.path.isdir(obs_par['configuration']):
        os.system('mkdir ' + obs_par['configuration'])
    os.chdir(obs_par['configuration'])

    for file in obs_par['files']:
        file_path = args.datadir + file.strip('\n')
        if not os.path.isfile(file_path):
            print(f"WARNING: The file {file_path} does not exist!")
            print("Continueuing script with next file if possible ...")
        else:
            # make a softlink to the workdirectory
            os.system('mkdir temp_links')
            cmd = 'ln -s ' + file_path + ' temp_links/' + file.strip('\n')
            print(cmd)
            os.system(cmd)

    os.system('mkdir temp_data')
    print('mode:', args.mode)
    if args.mode == 'line':
        cmd = 'atlod in=temp_links/* out=temp_data/data  ifsel=' + str(obs_par['line_if']) + \
              ' restfreq=1.420405752 options=bary,birdie,rfiflag,noauto edge=0'
    if args.mode == 'cont':
        cmd = 'atlod in=temp_links/* out=temp_data/data  ifsel=' + str(obs_par['cont_if']) + \
              ' restfreq=1.420405752 options=bary,birdie,rfiflag,noauto edge=0'

    os.system(cmd)
    os.system('uvindex vis=temp_data/data log=uvindex.log')
    os.chdir('temp_data')
    os.system('uvsplit vis=data options=mosaic')
    os.system('rm -rf data')
    os.system('rm -rf ../temp_links')

    # get list of files
    files = os.listdir('.')
    freq = files[0][-4:]
    # depending in miriad installation and os, freq has 4 or 6 characters
    if float(freq) < 1000:
        freq = files[0][-6:]

    obs_par['freq'] = freq
    print(obs_par)

    # read the number of channels:
    #cmd = 'prthd in=' + files[0] + '> header.log'
    #os.system(cmd)
    #head_file = open('header.log', 'rt')
    #lines = []
    #for line in head_file:
    #    print(f'lines : {line}')
    #    lines.append(line)

    #os.system('rm -rf header.log')
    #header = lines[14][0:-4]
    #header = header.split(' ')
    #freq_set = []
    #for h in range(len(header)):
    #    if header[h] != '':
    #        freq_set.append(float(header[h]))

    #chans = freq_set[1]
    #chan_1 = freq_set[2]
    #increment = freq_set[3]

    #print('print frequency settings:')
    #print(f'chans {chans}')
    #print(f'chan_1 {chan_1}')
    #print(f'increment {increment}')

    #out_chan = int(chans/args.aver)
    #line_set = 'channel,' + str(out_chan) + ',1,' + str(args.aver) + ',' + str(args.aver)


    for file in files:
        line_set = aver_line_set(file, args.aver)
        print(f"averaging : {file}")
        print('uvaver vis=' + file + ' line=' + line_set + ' out=' + file + '.aver ')
        os.system('uvaver vis=' + file + ' line=' + line_set + ' out=' + file + '.aver ')
        # rename the averaged file to the original
        os.system('rm -rf ' + file)
        os.system('mv ' + file + '.aver ' + file)

    return obs_par