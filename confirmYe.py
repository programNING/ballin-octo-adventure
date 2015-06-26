import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch

infile = h5.File('SkyNet_r-process_python.h5', 'r')

# These are (7841,) long, and should be constant numbers.
nucleons = infile['A']
protons = infile['Z']

# Abundance appears to have (2147, 7841): Rows are time steps, 
# columns are nuclides. Tracks the abundance of nuclides thru time.
#
abundance = infile['/Y']

# Get Ye as calculated by SkyNet
Ye = infile['/Ye']

# Get time.
time = infile['/Time']

Y_e = np.array(Ye)
T = np.array(time)
Y_i = np.array(abundance)
Z_i = np.array(protons)
A_i = np.array(nucleons)

shape_tuple = abundance.shape
tsteps = shape_tuple[0]

infile.close()

# Dot and sum Y_i dot Z_i for each timestep. Put these into a 
# (2147, 1) array.

YiZi = np.dot(Y_i, Z_i)

# Dot and sum Y_i dot A_i for each timestep. Put these into a
# (2147, 1) array.

YiAi = np.dot(Y_i, A_i)

# Divide Y_i dot Z_i / Y_i dot A_i. Is this cumbersome? Will check.
# Put result into (2147, 1) array.

calc_Ye = (YiZi / YiAi)

# Plot some stuff.

skynet_Yeplot, = plt.semilogx(T, Y_e, "r", linewidth = 2)
calc_Yeplot = plt.semilogx(T, calc_Ye, "b", linewidth = 2, ls = '--')


plt.xlabel("Time (s)")
plt.ylabel("Abundance Y_e")

skynet_patch = mpatch.Patch(color='red', label='SkyNet')
calc_patch = mpatch.Patch(color='blue', label='Calculated')
plt.legend( handles=[skynet_patch, calc_patch], \
	loc = (0, max(Y_e)), frameon=False)

plt.show()

# Doesn't show anything... :/
plt.savefig("confirmYe.pdf")
