import numpy as np
import h5py as h5


from glob import glob


def norm(x):

	"""
	normalize
	"""

	return x / np.sum(x,axis=0)


def cMean(*args, weight=None):

	"""
	circular mean
	"""

	dr, rd = np.deg2rad, np.rad2deg
	ns, nm = np.nansum, np.nanmean
	s, c, at2 = np.sin, np.cos, np.arctan2
	
	if len(args) == 1:
		ds = args[0]
		
		if weight:
			w = norm(weight)
		else:
			w = np.empty(ds.shape)
			w.fill(1.)
			w = norm(w)

		xr = dr(ds)
		sm, cm = ( ns(s(xr)*w, axis=0)/ns(w, axis=0), 
				ns(c(xr)*w, axis=0)/ns(w,axis=0) )
		
		ret =  at2(sm,cm)
		ret = rd(ret, dtype=np.float32)
		#ret[ret < 0] = ret[ret < 0] + 360
		
		#ret = ret + 90
		#ret[ret > 360] = ret[ret > 360] - 360
		return ret

	else: 
		x, y = args

		xr, yr = dr(x), dr(y)
		sAr = np.array([s(xr), s(yr)])
		cAr = np.array([c(xr), c(yr)])
		sm, cm = nm(sAr, axis=0), nm(cAr, axis=0) 
		#print(sm.min(), sm.max())
		#print(cm.min(), cm.max())
		ret = rd( at2(sm,cm),dtype=np.float32 )
		#print(ret.min(), ret.max())
		#ret[ret < 0] = ret[ret < 0] + 360
		#ret = ret + 90
		#ret[ret > 360] = ret[ret > 360] - 360
		
		return ret




def main(*args, **kwds):
	"""
	main run
	"""

	v = args[1]
	w = args[2]
	files = sorted(glob(f"{args[0]}/*"))

	for f in files:
		fsave = f.split('/')[-1].split('.')[0]
		print(f)	
			
		with h5.File(f,'r') as hdf:
			ck = hdf[v].chunks
			shp = hdf[v].shape

			mean = np.empty(shp[-1])	
			mean.fill(np.nan)

			X, Y = shp[0]/ck[0], shp[-1]/ck[-1]
			X = [[i*ck[0],(i+1)*ck[0]-1] for i in range(int(X)+1)]
			Y = [[i*ck[1],(i+1)*ck[1]-1] for i in range(int(Y)+1)]

			X[-1][-1], Y[-1][-1] = -1, -1
			
			for x in X:
				for y in Y:
					a, b = x[0], x[-1]
					m, n = y[0], y[-1]
					ds = hdf[v][a:b,m:n].astype(np.float32)
					wgt = hdf[w][a:b,m:n].astype(np.float32)
					ds[ds == -999.] = np.nan
					wgt[wgt == -999.] = np.nan
					wgt = None	
					tmp = cMean(ds, weight=wgt)
					mean[m:n] = cMean(mean[m:n], tmp, weight=wgt)
		mean = mean + 90
		mean[mean > 360] = mean[mean > 360] - 360
		np.save(f'./mwd_{fsave}.npy',mean)


if __name__ == "__main__":


	basedir = '/datasets/US_wave/v1.0.0/Alaska'
	var = 'maximum_energy_direction'
	weight = 'omni-directional_wave_power'

	main(basedir, var, weight)
