import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
import sys
import os
import palettable as pltable

# issues with strings?

def main(argv):
	time = []
	yabun = []
	label = []
	for i in argv:
		ye, t = get_data(i) # Filename written with no front slash
		yabun.append(ye)
		time.append(t)
		label.append(i)
	plot_shit(time, yabun, label)


def get_data(fil):

	infile = h5.File(fil, 'r')

	# Get Ye as calculated by SkyNet
	Ye = infile['/Ye']

	# Get time
	time = infile['/Time']

	Y_e = np.array(Ye)
	T = np.array(time)

	infile.close()

	return (Y_e, T)


### Plot some shit. ###
def plot_shit(tlst, yelst, lablst):
	# Initialize the figure.
	fig = plt.figure()
	ax1 = plt.subplot(111)
	ax1.set_color_cycle(pltable.colorbrewer.qualitative.Dark2_8.mpl_colors)
	for i in range(len(yelst)):
		plt.semilogx(tlst[i], yelst[i], lw = 2, label = lablst[i])

	ax1.set_xlabel("Time (s)")
	ax1.set_ylabel("Abundance Y_e")

	plt.legend(loc=0)

	plt.show()

if __name__ == "__main__":
	main(sys.argv[1:])

