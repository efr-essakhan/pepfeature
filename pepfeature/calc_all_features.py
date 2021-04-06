#' Calculate statistical and physicochemical features for peptides
#'
#' This function is used to calculate several distinct families of features for
#' a vector of peptides.

from calc_aa_composition import _calc_aa_composition
from calc_aa_descriptors import _calc_aa_descriptors
from calc_aa_percentages import _calc_aa_percentages
from calc_cojoint_triads import _calc_cojoint_triads
from calc_molecular_weight import _calc_molecular_weight
from calc_number_of_atoms import _calc_number_of_atoms
from calc_sequence_entropy import _calc_sequence_entropy
from calc_kmer_composition import _calc_kmer_composition

from utils import remove_invalid_aa, df_chunking
import os
import multiprocessing as mp
import functools
import datetime
from datetime import datetime
import numpy as np
import pandas as pd

functions = [
    _calc_aa_descriptors,
    _calc_aa_composition,
    _calc_aa_percentages,
    _calc_cojoint_triads,
    _calc_molecular_weight,
    _calc_number_of_atoms,
    _calc_sequence_entropy
    #_calc_kmer_composition
]


#CSV to contain amount of rows = chunksize
#Chunksize technique saves ram for processed results and results are processed in chunks
def calc_all_features_csv(dataframe, Ncores=4, k=2, chunksize = 50000, csv_path_filename = ['', 'result'], aa_column = 'Info_window_seq'):

    dataframe = remove_invalid_aa(dataframe)
    #Creating a back-up of the original dataframe as later below when the dataframe is passed into df_chunking then the original dataframe has parts deleted as chunks are returned by df_chunking (there is pass by reference in python)
    original_dataframe = dataframe.copy()

    ctx = mp.get_context('spawn')  # This guarantees that the Pool processes are just spawned and not forked from the parent process. Accordingly, none of them has access to the original DataFrame and all of them only need a tiny fraction of the parent's memory.
    p = ctx.Pool(processes=Ncores)

    dataframe_results = []

    for func in functions:

        dataframe = original_dataframe.copy()
        # Running each of the chunks in list_df to one of the cores available and saving the (chunk) DF with the features calculated as a csv
        for idx, result_df in enumerate(p.imap(func, df_chunking(dataframe, chunksize))):

            dataframe_results.append(result_df)

            print(result_df)
            print('-------------------------------------------------')




    p.close()
    p.join()  # the process will complete and only then any code after can be ran


    dataframe_results = pd.concat(dataframe_results, axis=1)
    dataframe_results.to_csv(os.path.join(csv_path_filename[0], csv_path_filename[1]
                                + f"_{datetime.now().strftime('%d%m%Y-%H%M%S')}_{idx}.csv"), index=False)



    #appended_data = pd.concat(appended_data)

# def calc_all_features_csv(dataframe, csv_path_filename = ['', 'result'], Ncores=4, chunksize=50000):
#
#     for module in module_names:
#         module.calculate_csv(dataframe=dataframe, Ncores=Ncores,
#                                    chunksize=chunksize, csv_path_filename=csv_path_filename)


def calc_all_features_df(dataframe, Ncores=4, chunksize=50000):

    for module in module_names:
        module.calculate_df(dataframe=dataframe, Ncores=Ncores,
                             chunksize=chunksize)
