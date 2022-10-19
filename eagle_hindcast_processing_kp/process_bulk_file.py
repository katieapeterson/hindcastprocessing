import os
import sys
_, Year = sys.argv # Year is passed in from the command line

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import netCDF4 as net
import datetime as dt

from glob import glob
from contextlib import contextmanager
from datetime import timedelta
from h5py import File



Format = "NETCDF4"

# conversion from names in .nc files to ME atlas Names
names = {
	#'Depth':'water_depth',
	'Hsig':'significant_wave_height',
	#'PkDir':'',
	'Dir':'mean_wave_direction',
	'RTpeak':'peak_period',
	'Period':'mean_absolute_period',
	'owp':'omni-directional_wave_power',
	'Tm_10':'energy_period', #'mean_zero-crossing_period',
	'sw':'spectral_width',
	#'jdmax':'',
	'djdmax':'maximum_energy_direction',
	'd':'directionality_coefficient'
	}

@contextmanager
def load_data(File,rw='r'):
	"""
	Simple convenience script to produce a context manager for
	accessing the netCDF datasets.

	File: absolute path and filename of netCDF file
	"""

	nc = net.Dataset(File,rw,format=Format)
	try:
		yield nc
	finally:
		nc.close()


def make_coords(xp,yp):
	"""
	convenience function to wrap the coordinate vectors

	takes in Lon, Lat -> Xp, Yp
	"""

	return np.array(list(zip(yp[:],xp[:]-360)))


def conv_mat_time(times):
	"""
	Converter from matlab based Ordinal timestamps to encoded strings

	times: Matlab ordinal timestamp
	"""

	dts = []	
	for time in times:
		dtime = pd.to_datetime(dt.date.fromordinal(int(time)))
		dts.append(dtime + timedelta(days=time%1) - timedelta(days = 366))
		
	return [d.strftime('%Y-%m-%d %H:%M:%S').encode() for d in dts]


def time_split(time):
	"""
	Reorganise data from a mis-formated string

	time: String timestamp
	"""

	string = lambda x: f'{x}'
	day,hour = string(time).split('.')
	stime = f'{day[0:4]}-{day[4:6]}-{day[6:8]} {hour}:00:00'
	return pd.to_datetime(stime).strftime('%Y-%m-%d %H:%M:%S').encode()


def scrape_files(path,shp=(10,12)):
	"""
	get all datafiles associated with a particular year

	path: path to root data directory
	"""
	return np.reshape(sorted([i for i in glob(f'{path}/*')]),shp)


def clean_name(sd):
	"""
	Makes the savefile name and removes existing

	sd: root save directory
	"""
	saveFile = f'{sd}/West_Coast_wave_{Year}.h5'	
	if os.path.isfile(saveFile):
		os.remove(saveFile)
	return saveFile


def main(*args, **kwargs):

	dss = scrape_files(args[0]) # Find the files for the year 
	saveFile = clean_name(args[1]) # make the save file and remove existing

	for i in [i+1 for i in range(12)]: # loop through months
		# load the appropriate .nc month datafile
		with load_data(dss[args[2].index(Year),i-1]) as nc:
			print(f'Month: {i}')
			if i == 1: # create the coordinate vector 
				coords = make_coords(nc['Xp'][:],nc['Yp'][:])

			# convert .nc timestamp to unicode string
			time = conv_mat_time(nc['matlab_time'][:])
			
			# open the .hdf5 file for saving
			with File(saveFile,'a') as hdf:

				# loop through variable names
				for swan,wpto in names.items():
					shp = nc[swan].shape
					print(wpto)
					if i == 1: # create variables on first iteration
						hdf.create_dataset(
								wpto,
								shp,
								data=nc[swan][:],
								dtype=np.float32,
								maxshape=(None,shp[-1],)
								)
						if 'time_index' not in list(hdf.keys()):
							hdf.create_dataset(
									'time_index',
									data = time,
									dtype = 'S19',
									maxshape=(None,)
									)
						if 'coordinates' not in list(hdf.keys()):
							hdf.create_dataset(
									'coordinates',
									data=coords,
									dtype=coords.dtype
									)
						if 'water_depth' not in list(hdf.keys()):
							hdf.create_dataset(
									'water_depth',
									data = nc['Depth'][:],
									dtype=nc['Depth'].dtype
									)									 
					else:
						# reshape and expand variable dimensions as needed
						oshp = hdf[wpto].shape
						hdf[wpto].resize((oshp[0]+shp[0],oshp[-1]))
						hdf[wpto][oshp[0]:,:] = nc[swan][:,:]

				# Save the final time vector
				ots = hdf['time_index'].shape
				hdf['time_index'].resize((ots[0]+len(time),))
				hdf['time_index'][ots[0]:] = time
							
						

if __name__ == "__main__":


	dataDir = '/scratch/abharath/West_Coast/iecParameters'
	saveDir = '/scratch/abharath/west_coast_2020_hdf5'
	year = ['2011','2012','2013','2014','2015','2016','2017','2018','2019','2020']

	# run main execution
	main(dataDir,saveDir,year)
