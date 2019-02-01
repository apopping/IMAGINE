#!/usr/bin/env python

'''
This script makes a dirty image of the data
'''
import os



def invert_spectral_line(args, obs_par):
    # go to the working directory
    os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])
    os.chdir('temp_data')

    # define the file names
    vis = obs_par['target'] + '.uvlin'
    map = obs_par['target'] + '.map'
    beam = obs_par['target'] + '.beam'

    ant_set = 'ant'+ str(args.ant)

    # define the spectral line settings
    vmin = int(obs_par['vel'] - (args.nchan * args.chwidth / 2))
    line_set = 'velocity,' + str(args.nchan) + ',' + str(vmin) + ',' + str(args.chwidth)

    # invert the data
    os.system('invert vis=' + vis +
              ' map=' + map +
              ' beam=' + beam +
              ' robust=' + str(args.robust) +
              ' imsize=' + str(args.imsize) +
              ' cell=' + str(args.cellsize) +
              ' stokes=i slop=0.5 options=mosaic '
              'line=' + line_set +
              ' "select=' + ant_set + '"')

    #command = 'invert vis=' + vis + ' map=' + map + ' beam=' + beam + ' robust=1 imsize=256 cell=20 stokes=i slop=0.5 options=mosaic line=' + line_set + ' "select=' + ant_set + '"'


    return



def invert_continuum(args, obs_par):
    # go to the working directory
    os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration']+'/temp_data')
    files=os.listdir(args.outdir+obs_par['target']+'/'+obs_par['configuration']+'/temp_data') 
    for names in files:
    	if names[0]=='1' or names[0]=='0':
		files=names
    obs_freq='.'+files[-4:]
    print(obs_freq)
    os.chdir(args.outdir + obs_par['target']) # + '/') + obs_par['configuration'])

    #os.chdir('temp_data')
    if os.path.isdir('imaging'):
    	dir_list=os.listdir('.')[:-1]
    else: 
    	dir_list=os.listdir('.')
    obs_tar=obs_par['target']
    # define the file names for the standard continuum data reduction
    #uvaver for continuum
    for configs in dir_list:
	if not os.path.isdir(configs+'/'+obs_tar+'.uva'):
        	 os.system('uvaver vis='+configs+ '/temp_data/' + obs_tar+obs_freq+
		  	   ' out='+configs+'/temp_data/'+obs_tar+'.uva')

    vis=''
    for i in range(0,len(dir_list)): 
	if i+1 != len(dir_list):
		vis+=dir_list[i]+'/temp_data/' + obs_tar+'.uva'+',' 
	else:
		vis+=dir_list[i] +'/temp_data/' + obs_tar+'.uva'
    print(vis)	
    #vis = obs_par['target'] + '.' + obs_par['freq']
    #map = obs_par['target']  + '.map'
    beam = obs_par['target'] + '.beam'
    
    #vis=obs_par['target']+'.uva'


    # if the continuum is narrowband from the spectral line data, change the names
    if os.path.isdir(obs_par['target'] + '.uvcon'):
        vis = obs_par['target'] + '.uvcon'
        map = obs_par['target'] + '.cmap'
        beam = obs_par['target'] + '.cbeam'

    ant_set = 'ant'+ str(args.ant)
    if not os.path.isdir('imaging'):
    	os.system('mkdir imaging')
    #os.chdir(args.outdir+'/'+obs_tar+'/'+'imaging')
    # invert the data
    os.system('invert vis=' + vis +
              ' map=' +'imaging/'+ obs_tar + '.di,'+'imaging/' + obs_tar + '.dq,' 'imaging/' + obs_tar + '.du,imaging/' + obs_tar + '.dv'+
              ' beam=' +'imaging/'+ beam +
              ' robust=' + str(args.robust) +
              ' imsize=' + str(args.imsize) +
              ' cell=' + str(args.cellsize) +
              ' stokes=i,q,u,v slop=0.5 options=mfs,mosaic,double ' #line=chan,500,100 works
              ' "select=' + ant_set + '"') #still need to implment the option to select channels

    # invert the data
    #command = 'invert vis=' + vis + ' map=' + map + ' beam=' + beam + ' robust=1 imsize=256 cell=20 stokes=i slop=0.5 options=mfs,mosaic'

    #print(command)
    #os.system(command)


    return

#def invert_cont_source(args,obs_par):
#    os.chdir(args.outdir + obs_par['target'] + '/' + obs_par['configuration'])
#    os.chdir('temp_data')

    # define the file names for the standard continuum data reduction
#    vis = obs_par['target'] + '.' + obs_par['freq']
#    map = obs_par['target'] # + '.map'
#    beam = obs_par['target'] + '.beam'
#    for i in range(1000,2000,8) #start chan end chan width


