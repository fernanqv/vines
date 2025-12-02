import numpy as np
import pyvinecopulib as pv
import time
from get_matrices import load_matrices_from_h5
import csv
import argparse

def main(index):
    data = np.loadtxt('input7.txt')

    # Transform copula data using the empirical distribution
    u = pv.to_pseudo_obs(data)   
    matrices7 = load_matrices_from_h5("matrices_nodes7.h5")

    #Fit all the model
    # measure time
    # Iterate through all loaded matrices
    #for i in range(5):
    results=[]
    
    start_time = time.time()
    for i in range(100):
        id=2000*index+i
        #print([f.name for f in pv.BicopFamily])
        controls = pv.FitControlsVinecop(family_set=pv.one_par, selection_criterion="aic", show_trace=False,parametric_method='mle')
        cop = pv.Vinecop.from_data(u, matrix=matrices7[id], controls=controls)
        aic = cop.aic()
        results.append((id,int(cop.npars), aic))
        # fit the sample to the structure wit specified controls
        # get the AIC score for the matrix on the sample
    print("Time taken for 100:", time.time() - start_time)

    # Write to file after finishing the loop
    output_file = f"salidas/results_run_{index}.csv"

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(results)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process one matrix by id")
    parser.add_argument("id", type=int, help="ID (0-based) of the matrix to process")
    args = parser.parse_args()

    # call main with the selected id (modify main to accept this argument)
    main(args.id)
    #main(1000)

