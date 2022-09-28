#%%
import sys
import numpy as np
import matplotlib.pyplot as plt

#from scripts.rustbca import *
sys.path.insert(1,'/Users/toyo/Library/CloudStorage/GoogleDrive-ty20@illinois.edu/My Drive/NPRE598 Computational Plasma Physics/RustBCA/scripts/')
import rustbca
from rustbca import do_trajectory_plot

do_trajectory_plot("boron_dust_grain_")

deposited_ions = np.genfromtxt(
    "2000.0eV_0.0001deg_He_TiO2_Al_Sideposited.output",
    delimiter=",",
    names=["M", "Z", "x", "y", "z", "collisions"],
)

plt.hist(deposited_ions["x"], bins=100)

plt.show()
#%%
