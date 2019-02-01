import argparse
import os
from read_observation_parameters import read_observation_parameters

def parameter_call():
   file_description ='''
   This is the main pipeline to reduce ATCA data,
   in particular data from the IMAGINE survey:
   Imaging Galaxies Intergalactic and Nearby Environment
   
   author: Attila Popping

   The script requires either and 'id' number that is used
   to extract the relevant parameters from the observations database
   Alternatively a 'target', 'configuration', and 'date' can be given
   to reduce a particular observation

   see
   > python imagine_pipeline.py --help
   for more information
   '''

   parser = argparse.ArgumentParser(description=file_description,
                                    usage = "imagine_pipeline.py",
                                    epilog = "last edited 2018")

   # argument: files to process




   #i have removed all  print(f'') things

   #pwd=str(os.system('pwd'))
   #print(pwd)
   parser.add_argument("-i", "--id",
                       dest="id",
                       default='None', #normal is NONE, input is the number of the project without the C
                       type=int,
                       help="the observation id, if this is given (PREFERED) all other information is extracted\n"
                            "form the database and further user arguments are ignored")

   parser.add_argument("-dd", "--datadir",
                       dest="datadir",
                       default='/datasets/CASS_BBPOLAR/work/lau120/ngc1512/raw_files/',
                       help="the directory where the raw observations are stored")

   parser.add_argument("--od", "--outdir",
                       dest="outdir",
                       default='/datasets/CASS_BBPOLAR/work/lau120/ngc1512/imagine_files/',
                       help="the directory where the data is being processed")

   parser.add_argument("-t", "--target",
                       dest="target",
                       default='ngc1512', #normal is NONE
                       help="the target galaxy")

   parser.add_argument("-c", "--configuration",
                       dest="config",
                       default='None', #normal is NONE
                       help="the configuration")

   parser.add_argument("-d", "--date",
                       dest="date",
                       default=None,
                       help="the date of the observation, if no date is given all available observations will be used")

   parser.add_argument("-p", "--path",
                       dest="datadir",
                       default='/datasets/CASS_BBPOLAR/work/lau120/ngc1512/raw_files/',
                       help="the directory of the raw data")

   parser.add_argument("-av", "--average",
                       dest="aver",
                       default=24,
                       type=int,
                       help="number of spectral channels to average")
   parser.add_argument("-m", "--mode",
                      dest="mode",
                      default='cont',
                      help="observing mode: spectral line (line) or continuum (cont)")

   parser.add_argument("-ant", "--ant",
                       dest="ant",
                       default='(6)', #for continuum source finding ant=6 (normal is (1,2,3,4,5))
                       help="antennas to be used for imaging")

   parser.add_argument("-nc", "--nchan",
                       dest="nchan",
                       default=250,
                       help="number of channels in image cube")

   parser.add_argument("-cw", "--chwidth",
                       dest="chwidth",
                       default=4,
                       help="channels width [km/s] in image cube")


   parser.add_argument("-is", "--imsize",
                       dest="imsize",
                       default='3,3,beam', #for continuum 3,3,beam (normal setting is  256)
                       help="spatial size [pixels] of the output image")

   parser.add_argument("-cs", "--cellsize",
                       dest="cellsize",
                       default='0.5,0.5', #for continuum 0.5,0.5 (normal setting is 20)
                       help="pixel size of output image [arcsec]")


   parser.add_argument("-r", "--robust",
                       dest="robust",
                       default=1,
                       help="robust values used for image weighting")

   args = parser.parse_args()
   #observation = args.obs
   #print(observation)

   helpstring = " 'python imagine_pipeline.py --help' "



   if args.id != None:
       id = args.id
       print("start working on observation: {id}")
   else:
       print('No observation ID is given, extracting info from user input')
       # check whether input is given
       if args.target is None:
           print("the target is not given, see {helpstring}")
           exit()
       if args.config is None:
           print("the configuration is not given, see {helpstring}")
           exit()


   if args.mode != 'line' and args.mode != 'cont':
       print('no valid mode is given (specatral line or continuum), see {helpstring}')
       exit()

   # read the relevant observing parameters
   # path on my local machine
   #database = '/Users/attila/work/imagine/IMAGINE/imagineV1.sqlite'
   # path on ICRAR system
   #database = '/home/apopping/imagine/IMAGINE-master/code/imagineV1.sqlite'
   database='/datasets/CASS_BBPOLAR/work/lau120/ngc1512/imagine_code/imagineV1.sqlite'
   obs_par = read_observation_parameters(args,database)

   # manual edit during development
   #obs_par['files'] = '2016-10-16_1301.C3157'

   #convert the files into a list
   obs_par['files'] = obs_par['files'].replace(' ','')
   obs_par['files'] = obs_par['files'].split(',')

   print(args.datadir)
   print(obs_par)

   return args, obs_par
