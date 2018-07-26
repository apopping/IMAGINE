# combine ngc3137
import os
from pre_conditions import pre_conditions


par = {}
par['target']='ngc3137'
par['project']='C3157'

par = pre_conditions(par)

os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/ngc3137_h214_1.par')
os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/ngc3137_750A_1.par')
os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/ngc3137_750B_1.par')
os.system('python /home/apopping/imagine/pipeline/IMAGINE/process_imagine.py /home/apopping/imagine/new_pars/ngc3137_EW352_1.par')

os.chdir('/mnt/science1/imagine/processed/' + par['target'])

vis='h214/*.uvlin,750a/*.uvlin,750b/*.uvlin,EW352/*.uvlin'

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
