#!/bin/bash
#SBATCH --job-name="vines"
#SBATCH --partition=compute
#SBATCH --time=03:59:00
#SBATCH --ntasks=16
##SBATCH --nodes=1
#SBATCH --ntasks-per-node=16
#SBATCH --cpus-per-task=1
#SBATCH --mem-per-cpu=1024MB
#SBATCH --array=0-3


#N_VINES=2580480
VINES_PER_BLOCK=40320
N_BLOCKS=16
#N_BLOCKS=$(( (N_VINES + VINES_PER_BLOCK - 1) / VINES_PER_BLOCK ))

for block in $(seq 0 $((N_BLOCKS-1))); do
    id=$(($SLURM_ARRAY_TASK_ID*$N_BLOCKS+${block}))
    echo ${id} ${VINES_PER_BLOCK}
    srun -N1 -n1 --exclusive python copulas_chat.py ${id} ${VINES_PER_BLOCK} &
done

wait
echo "Todos los bloques terminados"