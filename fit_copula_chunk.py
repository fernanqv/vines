import numpy as np
import pyvinecopulib as pv
import time
from get_matrices import load_matrices_from_h5
import csv
import argparse
import os
import os.path as op


def fit_copula_chunk(data_file, chunk_index, vines_per_index, matrices_file="matrices7.h5",output_dir="salidas"):
    """
    Processes a chunk of 'vines_per_index' structures starting from chunk_index.

    Parameters
    ----------
    data_file: str
        Path to the data file to fit the copulas.
    chunk_index: int
        Index of the current block.
    vines_per_index: int
        Number of vines per block.
    matrices_file: str
        HDF5 file containing the vinecopula structure matrices.
    output_dir: str
        Directory where the results will be saved.
    """
    results = []

    os.makedirs(output_dir, exist_ok=True)
    data_csv = np.loadtxt(data_file)
    # Transformar datos en pseudo-observaciones
    data = pv.to_pseudo_obs(data_csv)

    matrices = load_matrices_from_h5(matrices_file)

    first_vine = chunk_index * vines_per_index
    start_time = time.time()
    for i in range(vines_per_index):
        vine_id = first_vine + i

        if vine_id >= len(matrices):
            break

        controls = pv.FitControlsVinecop(
            family_set=pv.one_par,
            selection_criterion="aic",
            show_trace=False,
            parametric_method="mle",
        )
        #print(matrices[vine_id])
        cop = pv.Vinecop.from_data(data, matrix=matrices[vine_id], controls=controls)
        aic = cop.aic()
        #print(cop)
        results.append((int(vine_id), int(cop.npars), aic))

        # MARCEL'S WAY: We have verified both ways give the same AIC
        # matrixVC = pv.Vinecop.from_structure(matrix=matrices7[vine_id])
        # selection = matrixVC.select(data=u, controls=controls)
        # matrixVC.fit(u)
        # aic2 = matrixVC.aic()

        
    elapsed = time.time() - start_time
    print(
        f"Time taken: {elapsed:.2f} s"
    )

    output_file = f"{output_dir}/results7_id{chunk_index}.csv"
    with open(output_file, "w", newline="") as f_output_file:
        writer = csv.writer(f_output_file)
        writer.writerows(results)

    #return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a block of vine matrices")
    parser.add_argument("data_file", type=str, help="Path to the data file")
    parser.add_argument("chunk_index", type=int, help="Index of the current block")
    parser.add_argument("vines_per_index", type=int, help="Number of vines per block")
    parser.add_argument("--matrices_file", type=str, default="matrices7.h5", help="HDF5 file containing matrices")
    parser.add_argument("--output_dir", type=str, default="salidas", help="Output directory")
    
    args = parser.parse_args()

    fit_copula_chunk(args.data_file, args.chunk_index, args.vines_per_index, args.matrices_file, args.output_dir)
    
    #print(f"cat {args.output_dir}/results7_id* | sort -n > resultados.csv")
