# function to do basic imaging and cleaning on individual observations
import os

def basic_clean(par):
    map = par['par_name_short'] + '.map'
    beam = par['par_name_short'] + '.beam'
    model = par['par_name_short'] + '.model'
    restor = par['par_name_short'] + '.restor'
    imcont = par['par_name_short'] + '.imcont'

    line_set = 'velocity,' + str(par['nchan']) + ',' + str(par['vmin']) + ',' + str(par['width'])
    print 'starting invert'
    print 'line_set', line_set

    os.system('invert vis=' + par['par_name_short'] + '.uvlin map=' + map + ' beam=' + beam + ' robust=1 imsize=256 cell=20 stokes=i slop=0.5 options=mosaic line=' + line_set + ' "select=-ant(6)"')
    os.system('mossdi map=' + map +' beam=' + beam + ' out=' + model + ' niters=500 gain=0.1')
    os.system('restor map=' + map +' beam=' + beam + ' model=' + model + ' out=' + restor + ' mode=clean')

    # do the continuum subtraction in the image domain
    z1 = int(1)
    z2 = int((par['line_vmin']-par['vmin'])/par['width'])
    z3 = int((par['line_vmax']-par['vmin'])/par['width'])
    z4 = int(par['nchan'])

    contchan='(' + str(z1) + ',' + str(z2) + '),(' + str(z3) + ',' + str(z4) + ')'
    print contchan
    os.system('contsub in=' + restor + ' out=' + imcont + ' contchan="' + contchan + '" mode=poly,1')


    # make a continuum image
    cont_map = par['par_name_short'] + '.cont.map'
    cont_beam = par['par_name_short'] + '.cont.beam'
    cont_model = par['par_name_short'] + '.cont.model'
    cont_restor = par['par_name_short'] + '.cont.restor'

    os.system('invert vis=' + par['par_name_short'] + '.aver map=' + cont_map + ' beam=' + cont_beam + ' robust=1 imsize=256 cell=20 stokes=i slop=0.5 options=mosaic,mfs "select=-ant(6)"')
    os.system('mossdi map=' + cont_map +' beam=' + cont_beam + ' out=' + cont_model + ' niters=500 gain=0.1')
    os.system('restor map=' + cont_map +' beam=' + cont_beam + ' model=' + cont_model + ' out=' + cont_restor + ' mode=clean')

    return
