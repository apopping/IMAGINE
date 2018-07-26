# function to do uv based continuum subtraction (polinomial)
import os
def cont_uvlin(par):
    os.system('prthd in=' + par['source'] + '.aver  > header.log')
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

    line_fmin = 1.42041 - (par['line_vmin']/300000.0)
    line_fmax = 1.42041 - (par['line_vmax']/300000.0)
    # calculate range of milky way
    mw_fmin = 1.42041 - (-200/300000.0)
    mw_fmax = 1.42041 - (200/300000.0)
    # check whether the MW is in the data:

    if chan_1 > mw_fmin:
        chan1 = 1
        chan2 = int((mw_fmin - chan_1) / increment)
        chan3 = int((mw_fmax - chan_1) / increment)
        chan4 = int((line_fmin - chan_1) / increment)
        chan5 = int((line_fmax - chan_1) / increment)
        chan6 = chans
        cont_chan = str(chan1) + ',' + str(chan2) + ',' + str(chan3) + ',' + str(chan4) + ',' + str(chan5) + ',' + str(chan6)
    elif chan_1 < mw_fmin and chan_1 > mw_fmax:
        chan1 =(mw_fmax - chan_1) / increment
        chan2 = int((line_fmin - chan_1) / increment)
        chan3 = int((line_fmax - chan_1) / increment)
        chan4 =chans
        cont_chan = str(chan1) + ',' + str(chan2) + ',' + str(chan3) + ',' + str(chan4)
    elif chan_1 < mw_fmax:
        chan1 = 1
        chan2 = int((line_fmin - chan_1) / increment)
        chan3 = int((line_fmax - chan_1) / increment)
        chan4 =chans
        cont_chan = str(chan1) + ',' + str(chan2) + ',' + str(chan3) + ',' + str(chan4)

    #command = 'uvlin vis=' + files[i] + '/' + source + '.aver out=' + files[i] + '/' + source + '.uvlin chans=' + cont_chan
    command = 'uvlin vis=' + par['source'] + '.aver out=' + par['par_name_short'] + '.uvlin chans=' + cont_chan
    os.system(command)

    # rename the non continuum averaged datathe
    command = 'mv ' + par['source'] + '.aver ' + par['par_name_short'] + '.aver'
    os.system(command)

    return
