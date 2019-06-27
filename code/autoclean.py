# ____________________________________________________________________
#
# AutoClean (autoclean.py) v0.1 - Automated CLEANing Script
# Copyright (C) 2018 Tobias Westmeier
# ____________________________________________________________________
#
# Script to use Miriad and SoFiA for automatically deconvolving HI
# data cubes. Miriad will be used for deconvolution (using clean for
# single pointings and mossdi for mosaics), while SoFiA will be needed
# to create a cleaning mask. Clip level of 5 and 2 times the RMS will
# be used in the initial and final CLEANing steps.
#
# Usage:
#    python autoclean.py <dirty_map> <dirty_beam> [<rms>]
#
# <dirty_map> and <dirty_beam> must be Miriad images/cubes containing
# the dirty map and beam, respectively.
#
# <rms> specifies the noise level of the image. If <rms> is missing or
# set to 0, then the script will attempt to automatically measure the
# RMS noise level using the median absolute deviation.
# ____________________________________________________________________
#
# Address:  Tobias Westmeier
#           ICRAR M468
#           The University of Western Australia
#           35 Stirling Highway
#           Crawley WA 6009
#           Australia
#
# E-mail:   tobias.westmeier [at] uwa.edu.au
# ____________________________________________________________________
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
# ____________________________________________________________________
#


import sys
import os


# Function for running system commands
def run_command(command):
	sys.stdout.write("\n\033[32mRunning command:\033[0m " + command + "\n");
	sys.stdout.flush();
	os.system(command);
	return;


# Function to create SoFiA parameter file
def create_sofia_par(filename_in, filename_flag, filename_out, spec_mode):
	with open(filename_out, "w") as output_file:
		output_file.write("CNHI.maxScale\t=\t-1\n");
		output_file.write("CNHI.medianTest\t=\ttrue\n");
		output_file.write("CNHI.minScale\t=\t5\n");
		output_file.write("CNHI.pReq\t=\t1e-5\n");
		output_file.write("CNHI.qReq\t=\t3.8\n");
		output_file.write("CNHI.verbose\t=\t1\n");
		output_file.write("SCfind.edgeMode\t=\tconstant\n");
		output_file.write("SCfind.fluxRange\t=\tnegative\n");
		output_file.write("SCfind.kernelUnit\t=\tpixel\n");
		if spec_mode == 'cont':
			output_file.write("SCfind.kernels\t=\t[[ 0, 0, 0,'b'][ 3, 3, 0,'b'],[ 6, 6, 0,'b'],[ 10, 10, 0,'b']]\n");
		else:
			output_file.write("SCfind.kernels\t=\t[[ 0, 0, 0,'b'],[ 0, 0, 3,'b'],[ 0, 0, 7,'b'],[ 3, 3, 0,'b'],[ 3, 3, 3,'b'],[ 3, 3, 7,'b'],[ 6, 6, 0,'b'],[ 6, 6, 3,'b'],[ 6, 6, 7,'b'],[ 10, 10, 0,'b'],[ 10, 10, 3,'b'],[ 10, 10, 7,'b']]\n");
		output_file.write("SCfind.maskScaleXY\t=\t2.0\n");
		output_file.write("SCfind.maskScaleZ\t=\t2.0\n");
		output_file.write("SCfind.rmsMode\t=\tgauss\n");
		output_file.write("SCfind.sizeFilter\t=\t0.0\n");
		output_file.write("SCfind.threshold\t=\t7.0\n"); # changed from 5
		output_file.write("SCfind.verbose\t=\ttrue\n");
		output_file.write("flag.file\t=\t" + filename_flag + "\n");
		output_file.write("flag.regions\t=\t[]\n");
		output_file.write("import.inFile\t=\t" + filename_in + "\n");
		output_file.write("import.maskFile\t=\t\n");
		output_file.write("import.subcube\t=\t[]\n");
		output_file.write("import.subcubeMode\t=\tpixel\n");
		output_file.write("import.weightsFile\t=\t\n");
		output_file.write("import.weightsFunction\t=\t\n");
		output_file.write("merge.minSizeX\t=\t7\n");
		output_file.write("merge.minSizeY\t=\t7\n");
		if spec_mode == 'cont':
			output_file.write("merge.minSizeZ\t=\t1\n");
		else:
			output_file.write("merge.minSizeZ\t=\t7\n");
		output_file.write("merge.positivity\t=\ttrue\n");  # changed from false
		output_file.write("merge.radiusX\t=\t3\n");
		output_file.write("merge.radiusY\t=\t3\n");
		if spec_mode == 'cont':
			output_file.write("merge.radiusZ\t=\t1\n");
		else:
			output_file.write("merge.radiusZ\t=\t3\n");
		output_file.write("optical.sourceCatalogue\t=\t\n");
		output_file.write("optical.spatSize\t=\t0.01\n");
		output_file.write("optical.specSize\t=\t1e+5\n");
		output_file.write("optical.storeMultiCat\t=\tfalse\n");
		output_file.write("parameters.dilateChan\t=\t1\n");
		output_file.write("parameters.dilateMask\t=\tfalse\n");
		output_file.write("parameters.dilatePixMax\t=\t10\n");
		output_file.write("parameters.dilateThreshold\t=\t0.02\n");
		output_file.write("parameters.fitBusyFunction\t=\tfalse\n");
		output_file.write("parameters.getUncertainties\t=\tfalse\n");
		output_file.write("parameters.optimiseMask\t=\tfalse\n");
		output_file.write("reliability.autoKernel\t=\ttrue\n");
		output_file.write("reliability.fMin\t=\t10.0\n");
		output_file.write("reliability.kernel\t=\t[0.15,0.05,0.1]\n");
		output_file.write("reliability.logPars\t=\t[1,1,1]\n");
		output_file.write("reliability.makePlot\t=\tfalse\n");
		output_file.write("reliability.negPerBin\t=\t1.0\n");
		output_file.write("reliability.parSpace\t=\t['n_pix','snr_sum','snr_max']\n");
		output_file.write("reliability.scaleKernel\t=\t0.50\n");
		output_file.write("reliability.skellamTol\t=\t-0.5\n");
		output_file.write("reliability.threshold\t=\t0.90\n");
		output_file.write("reliability.usecov\t=\ttrue\n");
		output_file.write("scaleNoise.edgeX\t=\t0\n");
		output_file.write("scaleNoise.edgeY\t=\t0\n");
		output_file.write("scaleNoise.edgeZ\t=\t0\n");
		output_file.write("scaleNoise.fluxRange\t=\tall\n");
		output_file.write("scaleNoise.gridSpatial\t=\t10\n");
		output_file.write("scaleNoise.gridSpectral\t=\t10\n");
		output_file.write("scaleNoise.method\t=\tglobal\n");
		output_file.write("scaleNoise.scaleX\t=\tfalse\n");
		output_file.write("scaleNoise.scaleY\t=\tfalse\n");
		output_file.write("scaleNoise.scaleZ\t=\ttrue\n");
		output_file.write("scaleNoise.statistic\t=\tmad\n");
		output_file.write("scaleNoise.windowSpatial\t=\t20\n");
		output_file.write("scaleNoise.windowSpectral\t=\t20\n");
		output_file.write("smooth.edgeMode\t=\tconstant\n");
		output_file.write("smooth.kernel\t=\tgaussian\n");
		output_file.write("smooth.kernelX\t=\t3.0\n");
		output_file.write("smooth.kernelY\t=\t3.0\n");
		output_file.write("smooth.kernelZ\t=\t3.0\n");
		output_file.write("steps.doCNHI\t=\tfalse\n");
		output_file.write("steps.doCubelets\t=\tfalse\n");
		output_file.write("steps.doDebug\t=\tfalse\n");
		output_file.write("steps.doFlag\t=\ttrue\n");
		output_file.write("steps.doMerge\t=\ttrue\n");
		output_file.write("steps.doMom0\t=\tfalse\n");
		output_file.write("steps.doMom1\t=\tfalse\n");
		output_file.write("steps.doOptical\t=\tfalse\n");
		output_file.write("steps.doParameterise\t=\tfalse\n");
		output_file.write("steps.doReliability\t=\tfalse\n");
		output_file.write("steps.doSCfind\t=\ttrue\n");
		output_file.write("steps.doScaleNoise\t=\tfalse\n");
		output_file.write("steps.doSmooth\t=\tfalse\n");
		output_file.write("steps.doSubcube\t=\tfalse\n");
		output_file.write("steps.doThreshold\t=\tfalse\n");
		output_file.write("steps.doWavelet\t=\tfalse\n");
		output_file.write("steps.doWriteCat\t=\ttrue\n");
		output_file.write("steps.doWriteFilteredCube\t=\tfalse\n");
		output_file.write("steps.doWriteMask\t=\ttrue\n");
		output_file.write("threshold.clipMethod\t=\trelative\n");
		output_file.write("threshold.fluxRange\t=\tall\n");
		output_file.write("threshold.rmsMode\t=\tstd\n");
		output_file.write("threshold.threshold\t=\t4.0\n");
		output_file.write("threshold.verbose\t=\tfalse\n");
		output_file.write("wavelet.iterations\t=\t3\n");
		output_file.write("wavelet.positivity\t=\tfalse\n");
		output_file.write("wavelet.scaleXY\t=\t-1\n");
		output_file.write("wavelet.scaleZ\t=\t-1\n");
		output_file.write("wavelet.threshold\t=\t5.0\n");
		output_file.write("writeCat.basename\t=\t\n");
		output_file.write("writeCat.compress\t=\tfalse\n");
		output_file.write("writeCat.outputDir\t=\t\n");
		output_file.write("writeCat.overwrite\t=\ttrue\n");
		output_file.write("writeCat.parameters\t=\t['*']\n");
		output_file.write("writeCat.writeASCII\t=\tfalse\n");
		output_file.write("writeCat.writeSQL\t=\tfalse\n");
		output_file.write("writeCat.writeXML\t=\tfalse\n");
	return;


# Check command-line arguments
if len(sys.argv) < 4 or len(sys.argv) > 5:
	sys.stderr.write("Usage: python autoclean.py <dirty_map> <dirty_beam> <mode> [<rms>]\n");
	sys.exit(1);

# Define basic parameters
file_map  = sys.argv[1].rstrip("/");
file_beam = sys.argv[2].rstrip("/");
file_out  = file_map + ".clean";
spec_mode = sys.argv[3];

if len(sys.argv) > 4:
	rms = abs(float(sys.argv[4]));
else:
	rms = 0.0;

# Define temporary file names
basename             = "autoclean-tmp-file.";
file_model           = basename + "model";
file_restor          = basename + "restor";
file_map_fits        = basename + "map.fits";
file_restor_fits     = basename + "restor.fits";
file_sofia           = basename + "sofia.par";
file_sofia_mask_fits = file_restor + "_mask.fits";
file_sofia_mask      = basename + "sofia.mask";
file_sofia_mask_2    = basename + "sofia.mask.2";
file_model_2         = basename + "model.2";
file_restor_2        = basename + "restor.2";

# Ensure that input files exist and are directories
if not os.path.isdir(file_map):
	sys.stderr.write("Input file does not exist or is not directory: " + file_map + "\n");
	sys.exit(1);

if not os.path.isdir(file_beam):
	sys.stderr.write("Input file does not exist or is not directory: " + file_beam + "\n");
	sys.exit(1);

# Check if the input map is a mosaic
if os.path.isfile(file_map + "/mostable"): mosaic = True;
else: mosaic = False;

# Remove existing temporary and output files
run_command("rm -rf " + basename + "*");
run_command("rm -rf " + file_out);

# Convert dirty map to FITS
run_command("fits op=xyout in=" + file_map + " out=" + file_map_fits);

# Measure noise if requested, using two-pass MAD
if rms == 0.0:
	try:
		from astropy.io import fits
	except:
		sys.stderr.write("ERROR: Failed to load \'fits\' module. Is Astropy installed?\n");
		sys.exit(1);
	
	try:
		from numpy import nanmedian
	except ImportError:
		try:
			from scipy.stats import nanmedian
		except ImportError:
			try:
				from scipy import nanmedian
			except ImportError:
				sys.stderr.write("ERROR: Failed to load \'nanmedian\' function. Is NumPy or SciPy installed?\n");
				sys.exit(1);
	
	sys.stdout.write("Measuring noise level using median absolute deviation.\n");
	sys.stdout.flush();
	
	# Open FITS file
	hdu = fits.open(file_map_fits);
	data = hdu[0].data;
	
	# Use at most about 1 million samples
	cadence = max(1, int(float(data.size) / 1.0e+6));
	
	# Measure RMS via MAD, using 2nd pass with 4-sigma clip level
	rms = 1.4826 * nanmedian(abs(data[::cadence]), axis=None);
	rms = 1.4826 * nanmedian(abs(data[::cadence][abs(data[::cadence]) < 4.0 * rms]), axis=None);
	
	# Close FITS file
	hdu.close();
	sys.stdout.write("  Using measured noise level of " + str(rms) + ".\n\n");
	sys.stdout.flush();

# Define thresholds
thresh_hi = 5.0 * rms;
thresh_lo = 2.0 * rms;

# Blind CLEAN to 5-sigma
if mosaic: run_command("mossdi map=" + file_map + " beam=" + file_beam + " out=" + file_model + " niters=1000 cutoff=" + str(thresh_hi));
else: run_command("clean map=" + file_map + " beam=" + file_beam + " out=" + file_model + " niters=1000 cutoff=" + str(thresh_hi));

# Restore image
run_command("restor map=" + file_map + " beam=" + file_beam + " model=" + file_model + " out=" + file_restor);

# Convert restored image to FITS
run_command("fits op=xyout in=" + file_restor + " out=" + file_restor_fits);

# Create SoFiA parameter file
create_sofia_par(file_restor_fits, file_map_fits, file_sofia, spec_mode);

# Run SoFiA
#run_command("sofia_pipeline.py " + file_sofia);
# hardcoded for now, but not a good solution
myhost = os.uname()[1]
if myhost == 'epeius.icrar.org':
	run_command("~/anaconda2/bin/python ~/Software/sofia/SoFiA-1.2.0/sofia_pipeline.py " + file_sofia);
else:
	run_command("sofia_pipeline.py " + file_sofia);


# Convert SoFiA mask to Miriad
run_command("fits op=xyin in=" + file_sofia_mask_fits + " out=" + file_sofia_mask);

# Mask mask
run_command("maths exp=\"<" + file_sofia_mask + ">\" mask=\"<" + file_sofia_mask + ">.gt.0\" out=" + file_sofia_mask_2);

# Repeat CLEAN down to 2-sigma
if mosaic: run_command("mossdi map=" + file_map + " beam=" + file_beam + " out=" + file_model_2 + " niters=10000 cutoff=" + str(thresh_lo) + " region=\"mask(" + file_sofia_mask_2 + ")\"");
else: run_command("clean map=" + file_map + " beam=" + file_beam + " out=" + file_model_2 + " niters=10000 cutoff=" + str(thresh_lo) + " region=\"mask(" + file_sofia_mask_2 + ")\"");
run_command("restor map=" + file_map + " beam=" + file_beam + " model=" + file_model_2 + " out=" + file_restor_2);

# Create final, masked cube
#run_command("maths exp=\"<" + file_restor_2 + ">\" mask=\"<" + file_map + ">.lt.1e+38\" out=" + file_out);
os.system('cp -r '+ file_restor_2 + ' ' + file_out)




# Print summary and clean-up instructions
if mosaic: obs_type = "mosaic";
else: obs_type = "single pointing"
sys.stdout.write("\033[32m\n==========================================================\033[0m\n");
sys.stdout.write("\033[32mPipeline finished.\033[0m\n");
sys.stdout.write("Noise level assumed for " + obs_type + ":\n");
sys.stdout.write("  " + str(rms) + "\n");
sys.stdout.write("The final, cleaned image should have been saved as:\n");
sys.stdout.write("  " + file_out + "\n");
sys.stdout.write("Temporary files can be deleted with the following command:\n");
sys.stdout.write("  rm -rf " + basename + "*\n");
sys.stdout.write("\033[32m==========================================================\033[0m\n\n");
