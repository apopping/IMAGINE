#!/usr/bin/env python

'''
make a log file from all the generated info
'''

import os
import os.path
import subprocess


def make_log(args, obs_par):
    mom0_device = 'contour_mom0.ps'
    mom1_device = 'contour_mom1.ps'
    # uu_vv_device = obs_par['target'] + '_uu_vv.ps'
    ha_amp_device = obs_par['target'] + '_ha_amp.ps'
    time_amp_device = obs_par['target'] + '_time_amp.ps'
    time_rms_device = obs_par['target'] + '_time_rms.ps'
    freq_rms_device = obs_par['target'] + '_freq_rms.ps'


    with open("pipeline_log.tex", "w") as tex_file:
        #print(f"Purchase Amount: {TotalAmount}", file=tex_file)
        #print('This is the file', file=tex_file)

        print("\\documentclass{article}", file=tex_file)
        print("\\usepackage{graphicx}", file=tex_file)
        print("\\hoffset=-30mm", file=tex_file)
        print("\\textwidth=170mm", file=tex_file)
        print("\\textheight=230mm", file=tex_file)
        print("\\begin{document}", file=tex_file)

        print("{\\bf Introduction}\\", file=tex_file)
        print("Here is the text of your", file=tex_file)

        print("\\begin{figure}", file=tex_file)
        print("\includegraphics[angle=270, width=7cm]{" + mom0_device + "}", file=tex_file)
        print("\includegraphics[angle=270, width=7cm]{" + mom1_device + "}", file=tex_file)
        print("\caption{Moment maps}", file=tex_file)
        print("\label{moments}", file=tex_file)
        print("\end{figure}", file=tex_file)

        print("\\begin{figure}", file=tex_file)
        #print("\includegraphics[angle=270, width=6cm]{" + ha_amp_device + "}", file=tex_file)
        print("\includegraphics[angle=270, width=14cm]{" + time_amp_device + "}", file=tex_file)
        print("\caption{Time coverage}", file=tex_file)
        print("\label{time}", file=tex_file)
        print("\end{figure}", file=tex_file)

        print("\\begin{figure}", file=tex_file)
        print("\includegraphics[angle=270, width=14cm]{" + time_rms_device + "}", file=tex_file)
        #print("\includegraphics[angle=270, width=6cm]{" + freq_rms_device + "}", file=tex_file)
        print("\caption{RMS}", file=tex_file)
        print("\label{rms}", file=tex_file)
        print("\end{figure}", file=tex_file)

        print("\end{document}", file=tex_file)
        #tex_file.close()

    subprocess.call('ls -rtl', shell=True)
    cmd = 'latex pipeline_log.tex'
    subprocess.call(cmd, shell=True)
    cmd = 'dvipdf pipeline_log.dvi pipeline_log.pdf'
    subprocess.call(cmd, shell=True)

    #os.system("latex pipeline_log.tex")
    #os.system("dvipdf pipeline_log.dvi pipeline_log.pdf")

    return