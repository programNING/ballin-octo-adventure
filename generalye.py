import numpy as np
import h5py as h5
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch
import sys
import palettable as pltable

def main(argv):
	a_flag = 0
	time = []
	yabun = []
	label = []
	A_bar_lst = []

	for i in argv:
		if i == '-a':
			a_flag = 1
		else:
			ye, t = get_data(i) # Filename written with no front slash
			yabun.append(ye)
			time.append(t)
			label.append(i)
	if a_flag == 1:
		for i in argv:
			if i != '-a':
				A_bar = avgmassnum(i)
				A_bar_lst.append(A_bar)
		plot_w_avgmass(time, yabun, A_bar_lst, label)
	else:
		plot_ye(time, yabun, label)


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

### calculate average mass number per timestep per file fed to it
def avgmassnum(fil):
	infile = h5.File(fil, 'r')

	# Get abundance and nucleons.

	nucleons = infile['A']
	abundance = infile['Y']

	# Find out how many time steps in this simulation.

	shape_tuple = abundance.shape
	tsteps = shape_tuple[0]
	nuclid = shape_tuple[1]

	# Turn them into numpy arrays.

	A = np.array(nucleons)
	Y = np.array(abundance)

	# Remove nuclides with mass # <= 12. First stack them into \
	# one array, and then delete columns of mass # <= 12.

	A_Y = np.vstack((A,Y))
	first_row = A_Y[0]
	for i in first_row:
		if i <= 12:
			A_Y = np.delete(A_Y, np.where(first_row==i), axis = 1)

	# Now set A, Y so that they lack the nuclei <= 12.

	A = A_Y[0]
	Y = A_Y[1:]

	# Calculate average mass number per time step
	AiYi = np.dot(Y, A)
	Yi = np.sum(Y, axis = 1)
	avgmassnum = AiYi / (Yi + 10**-24)

	return avgmassnum

### Plot ###

def plot_ye(tlst, yelst, lablst):
	# Initialize the figure.
	fig = plt.figure()
	ax1 = plt.subplot(111)
	ax1.set_color_cycle(pltable.colorbrewer.qualitative.Dark2_8.mpl_colors)
	for i in range(len(yelst)):
		plt.semilogx(tlst[i], yelst[i], lw = 1, label = lablst[i])

	ax1.set_xlabel("Time (s)")
	ax1.set_ylabel("Abundance Y_e")

	plt.legend(loc=0)

	plt.show()

def plot_w_avgmass(tlst, yelst, abarlst, lablst):

	## EDIT THIS TO PUT ON MULTIPLE SUBPLOTS ##

	# Initialize the figure.
	fig = plt.figure()
	ax1 = plt.subplot(111)
	ax1.set_color_cycle(pltable.colorbrewer.qualitative.Dark2_8.mpl_colors)
	ax1.set_xscale('log')
	ax2 = ax1.twinx()
	ax2.set_color_cycle(pltable.colorbrewer.qualitative.Dark2_8.mpl_colors)
	for i in range(len(yelst)):
		ax1.plot(tlst[i], yelst[i], lw = 1, label = lablst[i])
		ax2.plot(tlst[i], abarlst[i], lw = 1, ls = '--', label = '__nolegend__')

	ax1.set_xlabel("Time (s)")
	ax1.set_ylabel("Abundance Y_e")
	ax2.set_ylabel('Average Mass Number')

	ax1.legend(loc=0)

	plt.show()

if __name__ == "__main__":
	main(sys.argv[1:])

