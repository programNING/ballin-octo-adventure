import numpy as np
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.patches as mpatch

infile = h5.File('SkyNet_r-process_python.h5', 'r')

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

for i in range(len(A)):
	if A[i] in yzdict:
		yzdict[A[i]] += Y[i]
	else:
		yzdict[A[i]] = Y[i]


# Plot that stuff!!!

y_vs_z = plt.semilogy(yzdict.keys(), yzdict.values(), "b", lw = 1)

plt.xlim(0, max(A))
plt.ylim(10**-13, max(Y))

plt.xlabel("Mass Number (A)")
plt.ylabel("Total Abundance (Y)")


plt.show()
plt.savefig("Abundance_vs_Mass.pdf")

