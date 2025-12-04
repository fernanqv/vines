from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pyvinecopulib as pv
import time
from get_matrices import load_matrices_from_h5
import csv
import argparse


def fit_copula(index, vines_per_core, u, matrices7):
    # index: starting index for this core.
    # vines_per_core: number of vines to process per core

    results = []    
    first_vine=index*vines_per_core
    for i in range(vines_per_core):
        id=first_vine+i
        #print([f.name for f in pv.BicopFamily])
        controls = pv.FitControlsVinecop(family_set=pv.one_par, selection_criterion="aic", show_trace=False,parametric_method='mle')
        cop = pv.Vinecop.from_data(u, matrix=matrices7[id], controls=controls)
        aic = cop.aic()
        results.append((int(id),int(cop.npars), aic))
        # fit the sample to the structure wit specified controls
        # get the AIC score for the matrix on the sample

    return results

    # Write to file after finishing the loop

def main(index,cores,vines_per_core):
    data = np.loadtxt('input7.txt')

    # Transform copula data using the empirical distribution
    u = pv.to_pseudo_obs(data)   
    matrices7 = load_matrices_from_h5("matrices_nodes7.h5")
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=cores) as ex:
        futures = [ex.submit(fit_copula, index*cores+i, vines_per_core, u, matrices7) for i in np.arange(cores)]

    print(f"Time taken for {cores} parallel cores running {vines_per_core} vines per core: "  , time.time() - start_time)    
    output_file = f"salidas/results7_id{index}.csv"
    with open(output_file, "w", newline="") as f_output_file:        
        writer = csv.writer(f_output_file)
        for f in futures:           
            writer.writerows(f.result())


if __name__ == "__main__":
    # Change this variable to 0 to use command line arguments
    internal=0
    if internal==0:
        parser = argparse.ArgumentParser(description="Process one matrix by id")
        parser.add_argument("id", type=int, help="ID (0-based) of the matrix to process")
        parser.add_argument("cores", type=int, help="Number of cores to use for processing")
        parser.add_argument("vines_per_core", type=int, help="Number of vines to process per core")
        args = parser.parse_args()
        main(args.id, args.cores, args.vines_per_core)
        print(f"Processed {args.id} using {args.cores} cores with {args.vines_per_core} vines per core.")
    else:
        main(5,16,100)

