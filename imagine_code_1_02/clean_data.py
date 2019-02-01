#!/usr/bin/env python

'''
This script does a basic and blind clean in two iterations
A shallow clean and a deeper clean using a mask.
'''

import os


def basic_clean(args,obs_par):
    # go to the working directory
    os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])
    os.chdir('temp_data')
    stokes=['i','q','u','v']

    #vis = obs_par['target'] + '.uvlin'
    map = obs_par['target'] + '.map'
    beam = obs_par['target'] + '.beam'
    model = obs_par['target'] + '.model'
    mask = obs_par['target'] + '.mask'
    clean1 = obs_par['target'] + '.clean'
    #os.system('maths exp=' + map +
    #          ' mask="abs(' + map + ').gt.0.00001"' +
    #          ' out=' + mask)
    if args.mode=='line':

    # the data has been inverted from vis to image in a previous step, start with the deconvolution
	    os.system('mossdi map=' + map +
        	      ' beam=' + beam +
        	      ' out=' + model +
            	      ' niters=1000 gain=0.1' +
        	      ' region="mask(' + mask + ')"')

   	    os.system('restor map=' + map +
    	              ' beam=' + beam +
      	              ' model=' + model +
      	              ' out=' + clean1 +
      	              ' mode=clean')


    else:
   	    os.chdir(args.outdir + obs_par['target']+'/'+ 'imaging')
	    if not os.path.isdir('v_logs'):
	    	os.system('mkdir v_logs')
	    os.system('imhist in='+obs_par['target']+'.dv log=v_logs/'+obs_par['target']+'.log')
	    os.chdir('v_logs')
	    print(os.system('pwd'))
	    f=open(obs_par['target']+'.log','r')
	    a=f.readlines()
	    rms=a[6].split()
	    cut_rms=2*float(rms[2])
	    print(cut_rms)
	    os.chdir(args.outdir+obs_par['target']+'/'+'imaging')
	    for pol in stokes:
	    	os.system('mossdi map=' + obs_par['target'] +'.d'+ pol+ 
		          ' beam=' + beam +
			  ' out=' + obs_par['target'] +'.'+ pol +'model' +
			  ' niters=1 gain=0.1 '+'cutoff='+str(cut_rms))

		os.system('restor map='+ obs_par['target'] + '.d' + pol + 
			  ' beam=' + beam + 
		 	  ' model=' + obs_par['target']+'.'+ pol +'model'  +
    			  ' out=' + obs_par['target'] + '.' + pol + 'clean' ) 


    # clean the narrowband continuum if it exists
    if os.path.isdir(obs_par['target'] + '.uvcon'):
        cvis = obs_par['target'] + '.uvcon'
        cmap = obs_par['target'] + '.cmap'
        cbeam = obs_par['target'] + '.cbeam'
        cmodel = obs_par['target'] + '.cmodel'
        cclean1 = obs_par['target'] + '.cclean'

        # the data has been inverted from vis to image in a previous step, start with the deconvolution
        os.system('mossdi map=' + cmap +
                  ' beam=' + cbeam +
                  ' out=' + cmodel +
                  ' niters=1000 gain=0.1')

        os.system('restor map=' + cmap +
                  ' beam=' + cbeam +
                  ' model=' + cmodel +
                  ' out=' + cclean1 +
                  ' mode=clean')

    return
