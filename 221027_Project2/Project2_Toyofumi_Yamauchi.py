from materials import *
from formulas import *
from rustbca import *
from Project2_functions import *

def main():
    particle = 'He'
    target = 'TiO2_Al_Si_'
    energy = '200'

    angle = np.array(('0','15','30'))
    name = np.array(('1_','2_','3_'))
    for i in range(0,len(angle)):
        pie_chart_maker(name[i],particle,target,energy,angle[i])
        trajectory_plot_maker(name[i],particle,target,energy,angle[i])

if __name__ == '__main__':
    main()
