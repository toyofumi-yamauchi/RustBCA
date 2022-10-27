import os
import time
from weakref import ref

import toml
import numpy as np
from shapely.geometry import Point, Polygon, box
from scipy import constants
import matplotlib.pyplot as plt
from matplotlib import rcParams, cm
import matplotlib as mpl
import matplotlib.colors as colors

from materials import *
from formulas import *

#from generate_ftridyn_input import *

rcParams.update({'figure.autolayout': True})

#Constants
Q = constants.physical_constants["elementary charge"][0]
PI = constants.pi
AMU = constants.physical_constants["unified atomic mass unit"][0]
ANGSTROM = constants.angstrom
MICRON = constants.micro
NM = constants.nano
CM = constants.centi
EPS0 = constants.epsilon_0
A0 = constants.physical_constants["Bohr radius"][0]
K = constants.physical_constants["atomic unit of permittivity"][0]
ME = constants.physical_constants["electron mass"][0]
SQRTPI = np.sqrt(PI)
SQRT2PI = np.sqrt(2 * PI)
C = constants.physical_constants["speed of light in vacuum"][0]

INTERPOLATED = "INTERPOLATED"
LOW_ENERGY_NONLOCAL = "LOW_ENERGY_NONLOCAL"
LOW_ENERGY_LOCAL= "LOW_ENERGY_LOCAL"
LOW_ENERGY_EQUIPARTITION = "LOW_ENERGY_EQUIPARTITION"

LIQUID = "LIQUID"
GASEOUS = "GASEOUS"

MOLIERE = "MOLIERE"
KR_C = "KR_C"
ZBL = "ZBL"
LENZ_JENSEN = "LENZ_JENSEN"

QUADRATURE = "MENDENHALL_WELLER"
MAGIC = "MAGIC"

def max_min_finder(X,Y,X_max,Y_max,X_min,Y_min):
    if np.max(X) > X_max:
        X_max = np.max(X)
    if np.min(X) < X_min:
        X_min = np.min(X)
    if np.max(Y) > Y_max:
        Y_max = np.max(Y)
    if np.min(Y) < Y_min:
        Y_min = np.min(Y)
    return X_max,X_min,Y_max,Y_min

def empty_file_check(name,filetype):
    file_size = os.stat(name+filetype).st_size
    if file_size == 0:
        check = False
    else:
        check = True
    return check

def pie_chart_maker(name,particle,target,energy,angle):
    '''
    Make a pie chart showing the fraction of sputtered, reflected, and reposited particles

    Args:
        name (string): name of rustbca simulation
        particle (string): name of incident particle
        target (string): name of target material
        energy (string): energy of incident particle [eV]
        angle (string): angle of incident particle [degree]
    '''

    plt.style.use('tableau-colorblind10')

    N_tot, N_ref, N_spu, N_dep = 0, 0, 0, 0
    if empty_file_check(name,'sputtered.output'):
        sputtered = np.atleast_2d(np.genfromtxt(name+'sputtered.output', delimiter=','))
        N_spu = len(sputtered)
        N_tot += N_spu
    if empty_file_check(name,'reflected.output'):
        reflected = np.atleast_2d(np.genfromtxt(name+'reflected.output', delimiter=','))
        N_ref = len(reflected)
        N_tot += N_ref
    if empty_file_check(name,'deposited.output'):
        deposited = np.atleast_2d(np.genfromtxt(name+'deposited.output', delimiter=','))
        N_dep = len(deposited)
        N_tot += N_dep

    fig1,ax1 = plt.subplots()
    ax1 = plt.pie(np.array((N_spu,N_ref,N_dep)),
                  labels=['Sputtered = {:.0f}'.format(N_spu),'Reflected = {:.0f}'.format(N_ref),'Deposited = {:.0f}'.format(N_dep)],
                  startangle=90,autopct="%1.1f%%",
                  labeldistance=0.3,textprops={'color': "white", 'weight': "bold"})
    plt.title(energy+' eV '+particle+' → '+target+' with '+angle+'$\degree$')
    plt.savefig('Pie_'+name+'.png',dpi=300)
    #plt.show()

    return

def trajectory_plot_maker(name,particle,target,energy,angle):
    '''
    Plot the sputtered/reflected particle's angle with respect to the surface from [name]trajectories.output.
    
    Args:
        name (string): name of rustbca simulation
        particle (string): name of incident particle
        target (string): name of target material
        energy (string): energy of incident particle [eV]
        angle (string): angle of incident particle [degree]
    '''
    
    plt.style.use('tableau-colorblind10')

    fig1, ax1 = plt.subplots()

    trajectories = np.atleast_2d(np.genfromtxt(name+'trajectories.output', delimiter=','))
    trajectory_data = np.atleast_1d(np.genfromtxt(name+'trajectory_data.output', delimiter=',').transpose().astype(int))
    hitting_index=trajectory_data[0]

    ax1.plot(trajectories[0,3],trajectories[0,4],'rx',label='Starting Point')
    ax1.plot(trajectories[hitting_index,3],trajectories[hitting_index,4],'bx',label='Hitting Point')

    x_max, x_min, y_max, y_min = 0.0, 0.0, 0.0, 0.0
    if empty_file_check(name,'sputtered.output'):
        sputtered = np.atleast_2d(np.genfromtxt(name+'sputtered.output', delimiter=','))
        ax1.plot(sputtered[:,3],sputtered[:,4],'.',label='sputtered')
        x_max, x_min, y_max, y_min = max_min_finder(sputtered[:,3],sputtered[:,4], x_max, x_min, y_max, y_min)
    if empty_file_check(name,'reflected.output'):
        reflected = np.atleast_2d(np.genfromtxt(name+'reflected.output', delimiter=','))
        ax1.plot(reflected[:,3],reflected[:,4],'.',label='reflected')
        x_max, x_min, y_max, y_min = max_min_finder(reflected[:,3],reflected[:,4], x_max, x_min, y_max, y_min)
    if empty_file_check(name,'deposited.output'):
        deposited = np.atleast_2d(np.genfromtxt(name+'deposited.output', delimiter=','))
        ax1.plot(deposited[:,3],deposited[:,4],'.',label='deposited')
        x_max, x_min, y_max, y_min = max_min_finder(deposited[:,3],deposited[:,4], x_max, x_min, y_max, y_min)

    index = 0    
    for trajectory_length in trajectory_data:
        M = trajectories[index,0] # mass [amu]
        Z = trajectories[index,1] # atomic number [-]
        E = trajectories[index:(trajectory_length+index),2] # energy [eV]
        x = trajectories[index:(trajectory_length+index),3] # x position [μm]
        y = trajectories[index:(trajectory_length+index),4] # y position [μm]
        z = trajectories[index:(trajectory_length+index),5] # z position [μm]

        x_max, x_min, y_max, y_min = max_min_finder(x,y, x_max, x_min, y_max, y_min)
        ax1.plot(x,y,'k-',linewidth=0.5)
        index += trajectory_length

    ax1.axvspan(0,x_max*2,color='k',alpha=0.2,label='material')
    ax1.set_xlabel('x [μm]')
    #ax1.set_xlim(x_min*2,x_max*2)
    ax1.set_ylabel('y [μm]')
    ax1.set_ylim((-0.4,0.4))
    ax1.axis('square')
    ax1.legend()
    plt.title(energy+' eV '+particle+' → '+target+' with '+angle+'$\degree$')
    plt.savefig('Trajectory_'+name+'.png',dpi=300)
    #plt.show()

    return