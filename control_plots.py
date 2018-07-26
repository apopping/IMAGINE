#function to make plots for quality control_plots
import os

def control_plots(par):
    bpass_table = 'bandpass_cal_' + par['par_name_short']
    phase_table = 'phase_cal_' + par['par_name_short']

    os.system('gpplt vis=' + bpass_table + ' yaxis=amp nxy="3,2" select="-ant(6)" device=' + par['par_name_short'] + 'bpass_amp.ps/cps')
    os.system('gpplt vis=' + bpass_table + ' yaxis=phase nxy="3,2" select="-ant(6)" device=' + par['par_name_short'] + 'bpass_phase.ps/cps')

    os.system('gpplt vis=' + phase_table + ' yaxis=amp nxy="3,2" select="-ant(6)" device=' + par['par_name_short'] + 'phase_amp.ps/cps')
    os.system('gpplt vis=' + phase_table + ' yaxis=phase nxy="3,2" select="-ant(6)" device=' + par['par_name_short'] + 'phase_phase.ps/cps')

    os.system('uvplt vis="*.uvlin" select="-ant(6)" stokes=ii average=5 options=nobase axis=uu,vv device=' + par['par_name_short'] + '_uu_vv.ps/cps')
    os.system('uvplt vis="*.uvlin" select="-ant(6)" stokes=ii average=5 options=nobase axis=hangle,amp device=' + par['par_name_short'] + '_ha_amp.ps/cps')
    os.system('uvplt vis="*.uvlin" select="-ant(6)" stokes=ii average=5 axis=time,amp device=' + par['par_name_short'] + '_time_amp.ps/cps')

    # get an estimate of the noise:
    os.system('imstat in=' + par['par_name_short'] + '.imcont region="images(1,10)" log=imcont_stats.log options=g')

    stat_file = open('imcont_stats.log','rt')
    lines = []
    for line in stat_file:
        print 'lines : ', lines
        lines.append(line)

    os.system('rm -rf restor_stats.log')
    stat_line = lines[-1]
    stat_line = stat_line.split(' ')
    stat_val = []
    for h in range(len(stat_line)):
        if stat_line[h] != '':
            stat_val.append(stat_line[h])

    stat_rms = float(stat_val[2])
    clip_value = 7*stat_rms

    # file names with a "-" cause problems in maths (e.g. eso131-010)
    # make a temporary copy

    os.system('cp -r ' + par['par_name_short'] + '.imcont temp.imcont')
    os.system('rm -rf mask_imcont*')
    os.system('maths exp=temp.imcont mask="temp.imcont.gt.' + str(clip_value) + '" out=mask_imcont')
    os.system('moment in=mask_imcont out=' + par['par_name_short'] + '.mom0 mom=0')
    os.system('moment in=mask_imcont out=' + par['par_name_short'] + '.mom1 mom=1')
    os.system('rm -rf temp.imcont')

    return
