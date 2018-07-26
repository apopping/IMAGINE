# combine ngc3109
import os
from pre_conditions import pre_conditions


par = {}
par['target']='eso274-001'
par['project']='C3157'

par = pre_conditions(par)
os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/eso274-001_h75_1.par')
os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/eso274-001_h168_1.par')
os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/eso274-001_h168_2.par')
os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/eso274-001_h214_1.par')
os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/eso274-001_750d_1.par')
os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/eso274-001_750d_2.par')

os.chdir('/mnt/science1/imagine/processed/' + par['target'])

vis='h75/*.uvlin,h214/*.uvlin,h168/*.uvlin,750d/*.uvlin'

map = par['target'] + '.map'
beam = par['target'] + '.beam'
model = par['target'] + '.model'
restor = par['target'] + '.restor'
imcont = par['target'] + '.map.imcont'
line_set = 'velocity,' + str(par['nchan']) + ',' + str(par['vmin']) + ',' + str(par['width'])
print 'starting invert'
print 'line_set', line_set

os.system('invert vis=' + vis + ' map=' + map + ' beam=' + beam + ' robust=1 imsize=256 cell=20 stokes=i slop=0.5 options=mosaic line=' + line_set + ' "select=-ant(6)"')
#os.system('mossdi map=' + map +' beam=' + beam + ' out=' + model + ' niters=200 gain=0.1')
#os.system('restor map=' + map +' beam=' + beam + ' model=' + model + ' out=' + restor + ' mode=clean')

## do the continuum subtraction in the image domain
z1 = int(1)
z2 = int((par['line_vmin']-par['vmin'])/par['width'])
z3 = int((par['line_vmax']-par['vmin'])/par['width'])
z4 = int(par['nchan'])

contchan='(' + str(z1) + ',' + str(z2) + '),(' + str(z3) + ',' + str(z4) + ')'
print contchan
os.system('contsub in=' + map + ' out=' + imcont + ' contchan="' + contchan + '" mode=poly,1')


# make the continuum image
cont_vis='h75/*.aver,h214/*.aver,h168/*.aver,750d/*.aver'

cont_map = par['target'] + '.cont.map'
beam = par['target'] + '.cont.beam'
model = par['target'] + '.cont.model'
restor = par['target'] + '.cont.restor'

os.system('invert vis=' + cont_vis + ' map=' + cont_map + ' beam=' + cont_beam + ' robust=1 imsize=256 cell=20 stokes=i slop=0.5 options=mosaic,mfs "select=-ant(6)"')
