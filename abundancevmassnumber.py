import numpy as np
import h5py as h5
import matplotlib as mpl
import matplotlib.pyplot as plt
import random as r
import palettable as pltable

def abundancevmass(fil):
	infile = h5.File(fil, 'r')

	abundance = infile['/Y']
	nucleons = infile['/A']


	# Takes only the final abundance. A (1, 7841) array.
	Y = np.array(abundance[-1])

	# A (7841, 1) array.
	A = np.array(nucleons)


	infile.close()

	# Create a dictionary for mass number | abundance

	yzdict = {}

	# For loop iterating over nuclides--all with the same mass number
	# need to have their abundances added together.
	print 'Length of A: ', len(A)
	for i in range(len(A)):
		if A[i] in yzdict:
			yzdict[A[i]] += Y[i]
		else:
			yzdict[A[i]] = Y[i]

	print min(yzdict, key=yzdict.get)
	print 'Length of yzdict:', len(yzdict)
	return yzdict


# Plot that shit

# More generalized, requires more user input. BLAH so lazy
def plot_many(lst, legend_lst):
	cntr = 0
#	Ye_amnt = [0.01, 0.05, 0.10, 0.20, 0.30, 0.35, 0.40]
	fig = plt.figure()
	ax1 = plt.subplot(111)
	ax1.set_color_cycle(pltable.colorbrewer.qualitative.Dark2_8.mpl_colors)
	for i in lst:
		meow = plt.semilogy(i.keys(), i.values(), \
			label = legend_lst[cntr])
		cntr += 1
	plt.legend(loc=0)
	ax1.set_xlabel("Mass Number (A)")
	ax1.set_ylabel("Total Abundance (Y)")


	plt.show()
