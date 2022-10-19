# eagle_hindcast_processing
 processing and sumission scripts for hindcast datasets

# make environment for processing or move to that env 
# check for these packages: numpy, pandas, netCDF4, datetime

#### To change for each region:
#  ---> in RUN.sh
#       job name
#       username/email
#       srun location
#  ---> in process_bulk_file.py
#       line 107 - 	saveFile = f'{sd}/<region>_wave_{Year}.h5'	   
#       line 178 dataDir = '/scratch/<username>/<region>/iecParameters'
#   	line 179 saveDir = '/scratch/<username>/<region>_2020_hdf5'
#       line 180 double check the years
#  ---> in multi_sbatch.sh
#       double check years in loop

#### Checking the scripts
#       emacs ./process_bulk_file.py
# In emacs
#    sys.exit() #exits before executing everything, to text and to make sure it has all the packages  
#    
# Exit out of emacs, run it in python
# test for one year
#      python process_bulk_file.py 2011

#### Running the multi-batch script
# source multi_sbatch.sh (submits the job)
# It calls the RUN.sh which calls process_bulk_file.py
# RUN.sh asks for the resources, activates the env, then runs process_bulk_file.py#