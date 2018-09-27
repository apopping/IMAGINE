# combine ngcic5052
import os
from pre_conditions import pre_conditions


par = {}
par['target']='eso154-023'
par['project']='C3157_plus'
par['configuration'] = 'all'


par = pre_conditions(par)

#os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/eso154-023_h75_1.par')
#os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/eso154-023_h168_1.par')
#os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/eso154-023_h168_2.par')
#os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/eso154-023_h214_1.par')
#os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/eso154-023_ew352_1.par')
#os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/eso154-023_ew367_1.par')
#os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/eso154-023_750b_1.par')
#os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/eso154-023_15a_1.par')




os.chdir('/mnt/science1/imagine/processed/' + par['target'])

vis='15a/*.uvlin,750b/*.uvlin,ew367/*.uvlin,ew352/*.uvlin,h214/*.uvlin,h168/*.uvlin,h75/*.uvlin'

map = par['target'] + '.map'
beam = par['target'] + '.beam'
model = par['target'] + '.model'
restor = par['target'] + '.restor'
imcont = par['target'] + '.map.imcont'

# change from defaults
par['vmin'] = 350
par['nchan'] = 100


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
