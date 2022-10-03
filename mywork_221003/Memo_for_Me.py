'''
This is the memo from the NPRE 598 class on 22-10-03
Step-by-step for using the rustBCA.

Useful commands:
pwd              = showing the full pathname to the current folder location
ls               = showing the files in the current folder location
ls -la           = showing the full details of the files in the current folder location
mkdir FOLDERNAME = making the new folder as FILENAME in the current folder location
cd FOLDERNAME    = moving to the FILENAME folder from the current folder location
cp FILENAME .    = copying the FILENAME file to the current folder location
rm FILENAME      = removing the FILENAME file from the current folder location
rm FILANEME*     = removing the files containing FILENAME from the current folder location

Opening terminal in your folder: 
1.  Go to the folder "RustBCA"
    /Users/toyo/Library/CloudStorage/GoogleDrive-ty20@illinois.edu/My Drive/NPRE598 Computational Plasma Physics/RustBCA
2.  Finder -> Service -> New Terminal at Folder
3.  You should have something like:
        Last login: Mon Oct  3 11:09:46 on ttys002
        (base) toyo@wirelessprv-10-194-45-235 RustBCA % 

Checking the cargo:
1.  In terminal, 'cargo test'
2.  You shoud get something like: 
        test result: ok. 10 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.00s
        and
        test result: ok. 10 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.01s

Setting up the folder:
1.  In terminal, 'mkdir FOLDERNAME_YYMMDD'
    For example, FOLDERNAME_YYMMDD = mywork_221003
2.  In terminal, 'cd FOLDERNAME_YYMMDD'
3.  In terminal, 'cp ../scripts/formulas.py .'
4.  In terminal, 'cp ../scripts/materials.py .'
5.  In terminal, 'cp ../scripts/rustbca.py .'

Running rustBCA (e.g., layered_geometry.toml)
1.  In terminal, 'cp ../examples/layered_geometry.toml .'
2.  Open layered_geometry.toml in the FOLDERNAME_YYMMDD:
    For example, make changes:
        3    track_trajectories = false -> true
        5    track_recoil_trajectories = false -> true
        17   num_chunks = 10 -> 1
        19   track_energy_losses = false -> true
        40   N = [ 10000,] -> [ 5,]
3.  In terminal, 'cargo run --release layered_geometry.toml':
4.  You should have something like:
        Finished release [optimized] target(s) in 0.15s
        Running `/Users/toyo/Library/CloudStorage/GoogleDrive-ty20@illinois.edu/My Drive/NPRE598 Computational Plasma Physics/RustBCA/target/release/RustBCA layered_geometry.toml`
        Processing 5 ions...
        Initializing with 4 threads...
        [00:00:00][########################################][00:00:00] 100%
        Finished!
5. In the FOLDERNAME_YYMMDD, you should have the files of:
    2000.0eV_0.0001deg_He_TiO2_Al_Sideposited.output
    2000.0eV_0.0001deg_He_TiO2_Al_Sidisplacements.output
    2000.0eV_0.0001deg_He_TiO2_Al_Sienergy_loss.output
    2000.0eV_0.0001deg_He_TiO2_Al_Sireflected.output
    2000.0eV_0.0001deg_He_TiO2_Al_Sisputtered.output
    2000.0eV_0.0001deg_He_TiO2_Al_Sisummary.output
    2000.0eV_0.0001deg_He_TiO2_Al_Sitrajectories.output
    2000.0eV_0.0001deg_He_TiO2_Al_Sitrajectory_data.output
6. In terminal, 'cp ../Memo_for_Me.py . '
7. Open Memo_for_Me.py in the FOLDERNAME_YYMMDD:
    For example, make changes:
        name = "2000.0eV_0.0001deg_He_TiO2_Al_Si"
        N = 5
8. In terminal, 'python3 Memo_for_Me.py'

'''
from materials import *
from formulas import *
from rustbca import *

def main():
    name = "2000.0eV_0.0001deg_He_TiO2_Al_Si"
    N = 5
    do_trajectory_plot(name)
    plot_energy_loss(name,N)
    #plot_distributions_rustbca('2000.0eV_0.0001deg_He_TiO2_Al_Si')

if __name__ == '__main__':
    main()