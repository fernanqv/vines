import numpy as np
import pyvinecopulib as pv
import time
from get_matrices import load_matrices_from_h5
import csv
import argparse
import os
import os.path as op


def fit_copula_block(block_id, vines_per_block, u, matrices7):
    """
    Procesa un bloque de 'vines_per_block' estructuras a partir de block_id.
    """
    results = []

    first_vine = block_id * vines_per_block
    for i in range(vines_per_block):
        vine_id = first_vine + i

        if vine_id >= len(matrices7):
            break

        controls = pv.FitControlsVinecop(
            family_set=pv.one_par,
            selection_criterion="aic",
            show_trace=False,
            parametric_method="mle",
        )

        cop = pv.Vinecop.from_data(u, matrix=matrices7[vine_id], controls=controls)
        aic = cop.aic()
        results.append((int(vine_id), int(cop.npars), aic))

        # MARCEL'S WAY: We have verified both ways give the same AIC
        # matrixVC = pv.Vinecop.from_structure(matrix=matrices7[vine_id])
        # selection = matrixVC.select(data=u, controls=controls)
        # matrixVC.fit(u)
        # aic2 = matrixVC.aic()

    return results


def main(block_id, vines_per_block):
    data = np.loadtxt("input7.txt")

    # Transformar datos en pseudo-observaciones
    u = pv.to_pseudo_obs(data)

    # Cargar matrices
    matrices7 = load_matrices_from_h5("matrices_nodes7.h5")

    os.makedirs("salidas", exist_ok=True)

    start_time = time.time()
    results = fit_copula_block(block_id, vines_per_block, u, matrices7)
    elapsed = time.time() - start_time

    print(
        f"Time taken for block {block_id} with {vines_per_block} vines per block: {elapsed:.2f} s"
    )

    output_file = f"salidas/results7_id{block_id}.csv"
    with open(output_file, "w", newline="") as f_output_file:
        writer = csv.writer(f_output_file)
        writer.writerows(results)

    print(f"Wrote {len(results)} rows to {output_file}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process a block of vine matrices")
    parser.add_argument("block_id", type=int, help="Block ID (0-based)")
    parser.add_argument(
        "vines_per_block", type=int, help="Number of vines to process in this block"
    )
    args = parser.parse_args()

    main(args.block_id, args.vines_per_block)
    print(
        f"Processed block {args.block_id} with {args.vines_per_block} vines per block."
    )
