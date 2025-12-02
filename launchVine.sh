#!/bin/bash
#SBATCH --job-name="vines"
#SBATCH --partition=geocean
#SBATCH --time=08:00:00
#SBATCH --ntasks=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=2GB
#SBATCH --array=0,221,222,225,448,449,450,476,576,577,580,684


##SBATCH --output=compiled.log

# # Initialize mamba shell
# export MAMBA_EXE='/home/vfernandezquir/miniforge3/bin/mamba';
# export MAMBA_ROOT_PREFIX='/home/vfernandezquir/miniforge3';
# eval "$($MAMBA_EXE shell hook --shell bash --root-prefix $MAMBA_ROOT_PREFIX)"

# Activate pytorch environment
python copulas_T24.py $SLURM_ARRAY_TASK_ID 
