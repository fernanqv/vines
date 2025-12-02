# Valva MAC: Time taken: 90s a 4 cores
# UNICAN:    Time taken: 24s a 20 cores, 12s a 40 cores

from concurrent.futures import ProcessPoolExecutor
import numpy as np
import pandas as pd
import pyvinecopulib as pv

def create_vinecop(i):
    """
    Función que realiza el trabajo de una sola iteración del bucle.
    Retorna la tupla (clave, valor) para el diccionario.
    """
    key = str(i)
    value = pv.Vinecop.from_data(np.array(u), matrix=matrices_5_nodes[i].matrix)
    return (key, value)



data = pd.read_csv('data_savannah.csv', sep = ',')
# Transform copula data using the empirical distribution
u = pv.to_pseudo_obs(np.array(data))
# Visualize the pair-copula data
#pv.pairs_copula_data(u, scatter_size=0.5)
# first we import a function to extract the matrices from a files
from get_matrices import get_matrices

#Import matrices
matrices_5_nodes = get_matrices('./CHIMERA_5/', nodes=5)
# Fitting the 480 regular vines (matrices) to data. This cell will take some minutes to run (5mins in Patricia's laptop).

#Define a dictionary to store all the models
myDictionary = {} 

def main():
    # Crea una lista de índices [0, 1, 2, ...] para mapear
    indices = list(range(len(matrices_5_nodes)))
    # measure time
    import time
    start_time = time.time()
    with ProcessPoolExecutor(max_workers=4) as executor:
        # executor.map runs my_function(i) in parallel for each i
        results = list(executor.map(create_vinecop, indices))

    print("Time taken:", time.time() - start_time)
    #print(results)

if __name__ == "__main__":
    # Optional but sometimes nice to be explicit on macOS:
    # import multiprocessing
    # multiprocessing.set_start_method("spawn", force=True)

    main()