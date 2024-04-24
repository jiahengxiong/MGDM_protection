#!/bin/sh

# https://www.hpc.dtu.dk/?page_id=2021
# For more information on batch jobs, see the page on LSF jobs: https://www.hpc.dtu.dk/?page_id=1416.

# Parallel Run
# MATLAB can also run in parallel, both in a shared memory and in a distributed memory environment. If you want to run MATLAB on a single node, like on your personal computer, you have to follow the instructions for the shared memory script. This limits the number of workers that you can define in your MATLAB session to the number of cores available on a single node. Currently in the general HPC cluster we have 8 core and 20 core nodes.

# Shared Memory Script
# Assuming that your script is called MATLAB_MAINFILE .m , your script could look like this:

# embedded options to bsub - start with #BSUB
# -- our name ---
#BSUB -J ECOC22_Op
# -- choose queue --s
#BSUB -q b # in espo server
# -- specify that we need 2GB of memory per core/slot – (total requested memory is multiplied by number of requested cores)
#BSUB -R "rusage[mem=0.5GB]"
# -- Notify me by email when execution begins --
#           BSUB -B
# -- Notify me by email when execution ends   --
#           BSUB -N
# -- email address --
# please uncomment the following line and put in your e-mail address,
# if you want to receive e-mail notifications on a non-default address
# BSUB -u qiaolun.zhang@nokia.com
#export LSB_JOB_REPORT_MAIL=N #prevent job emails
# -- Output File --
#BSUB -o Output_%J.txt
# -- Error File --
#BSUB -e Error_%J.txt
# -- estimated wall clock time (execution time): hh:mm --
#       #       BSUB -W 04:00
# -- Number of cores requested – make sure to request the minimum required to avoid blocking cores that aren’t needed (larger number of reserved cores => longer queue waiting time for all users and a down-prioritization of your next jobs according to fair runtime resources policy). FYI, if you are not using parallel toolbox (e.g., parfor) in matlab only one core is needed. If parfor as example is used in matlab, set the number of cores below as the number of works in parallel preferences settings in matlab.
#BSUB -n 4
# -- Specify the distribution of the cores: on a single node --
#BSUB -R "span[hosts=1]"
# -- end of LSF options --

# -- commands you want to execute --
#
# If you want a specific matlab module remember to load it
# Example: module load matlab/R2021a
#matlab -nodisplay -batch MATLAB_MAINFILE -logfile txtLogFileName

# The option #BSUB -n 4 specifies that you reserve 4 cores, and the line #BSUB -R "span[hosts=1]" specifies that these cores need to be on the same node. This means that you are reserving 4 cores for your MATLAB job, and you should not use more than 4 workers!

# NOTE:
#         If you use more workers inside matlab than cores that you have reserved, MATLAB will only run slowly! So use at most as many workers than the cores you asked for.
#         You can get the number of cores reserved from inside MATLAB, and assign them to a variable:
#         nw=str2num(getenv('LSB_DJOB_NUMPROC'));


for i in 5 6 7 8
do
#  python3 runHeuristicIns.py $i &
  python3 test_long_network_capacity_grooming_loop.py $i &
  wait
#  cust_func $i & # Put a function in the background
done

## Put all cust_func in the background and bash
## would wait until those are completed
## before displaying all done message
wait
echo "All done for all cases of opaque"
