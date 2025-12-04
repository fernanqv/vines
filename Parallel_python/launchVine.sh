#!/bin/bash
#SBATCH --job-name="vines"
#SBATCH --partition=compute
#SBATCH --time=00:10:00
#SBATCH --ntasks=16
##SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1024MB
#SBATCH --array=3
##SBATCH --array=0-4


##SBATCH --output=compiled.log

# # Initialize mamba shell
# export MAMBA_EXE='/home/vfernandezquir/miniforge3/bin/mamba';
# export MAMBA_ROOT_PREFIX='/home/vfernandezquir/miniforge3';
# eval "$($MAMBA_EXE shell hook --shell bash --root-prefix $MAMBA_ROOT_PREFIX)"

# Activate pytorch environment
# Launch 4 jobs. Each uses 16 cores and runs 645120/16=40320

python copulas7.py $SLURM_ARRAY_TASK_ID 16 4032
