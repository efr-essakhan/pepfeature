#' Calculate statistical and physicochemical features for peptides
#'
#' This function is used to calculate several distinct families of features for
#' a vector of peptides.

import calc_aa_composition
import calc_aa_descriptors
import calc_aa_percentages
import calc_cojoint_triads
import calc_molecular_weight
import calc_number_of_atoms
import calc_sequence_entropy
import calc_kmer_composition

from utils import calculate_export_csv, calculate_return_df
import os
import multiprocessing as mp
import functools
import datetime
from datetime import datetime
import numpy as np
import pandas as pd


# #CSV to contain amount of rows = chunksize
# #Chunksize technique saves ram for processed results and results are processed in chunks
# def calc_all_features_csv(dataframe, Ncores=4, k=2, chunksize = 50000, csv_path_filename = ['', 'result'], aa_column = 'Info_window_seq'):
#     functions = [
#         calc_aa_descriptors.calc_aa_descriptors,
#         calc_aa_composition.calc_aa_composition,
#         calc_aa_percentages.calc_aa_percentages,
#         calc_cojoint_triads.calc_cojoint_triads,
#         calc_molecular_weight.calc_molecular_weight,
#         calc_number_of_atoms.calc_number_of_atoms,
#         calc_sequence_entropy.calc_sequence_entropy
#     ]
#
#     dataframe = remove_invalid_aa(dataframe, aa_column)
#     #Creating a back-up of the original dataframe as later below when the dataframe is passed into df_chunking then the original dataframe has parts deleted as chunks are returned by df_chunking (there is pass by reference in python)
#     original_dataframe = dataframe.copy()
#
#     ctx = mp.get_context('spawn')  # This guarantees that the Pool processes are just spawned and not forked from the parent process. Accordingly, none of them has access to the original DataFrame and all of them only need a tiny fraction of the parent's memory.
#     p = ctx.Pool(processes=Ncores)
#
#     dataframe_results = []
#
#     for func in functions:
#
#         # Running each of the chunks in list_df to one of the cores available and saving the (chunk) DF with the features calculated as a csv
#         for idx, result_df in enumerate(p.imap(functools.partial(func, aa_column=aa_column), df_chunking(dataframe, chunksize))):
#
#             dataframe_results.append(result_df)
#
#             print(result_df)
#             print('-------------------------------------------------')
#
#         dataframe = original_dataframe.copy()
#
#     # Seperate loop for k-mer as it requires extra argument
#     for idx, result_df in enumerate(
#             p.imap(functools.partial(calc_kmer_composition.calc_kmer_composition, aa_column=aa_column, k=k), df_chunking(dataframe, chunksize))):
#         dataframe_results.append(result_df)
#
#         print(result_df)
#         print('-------------------------------------------------')
#
#
#     p.close()
#     p.join()  # the process will complete and only then any code after can be ran
#
    # dataframe_results = pd.concat(dataframe_results, axis=1)
    #
    # # Remove all columns of the original dataframe (as there will be duplicates)
    # dataframe_results = dataframe_results[dataframe_results.columns.difference(original_dataframe)]
    #
    # # Re-concat both dataframes
    # dataframe_results = pd.concat([original_dataframe, dataframe_results], axis=1)
    #
    # dataframe_results.to_csv(
    #     os.path.join(csv_path_filename[0], csv_path_filename[1] + f"_{datetime.now().strftime('%d%m%Y-%H%M%S')}_{idx}.csv"),
    #     index=False)

def _execute_all_routines(dataframe, k, aa_column = 'Info_window_seq'):

    original_dataframe = dataframe.copy()

    functions = [
        calc_aa_descriptors.calc_aa_descriptors,
        calc_aa_composition.calc_aa_composition,
        calc_aa_percentages.calc_aa_percentages,
        calc_cojoint_triads.calc_cojoint_triads,
        calc_molecular_weight.calc_molecular_weight,
        calc_number_of_atoms.calc_number_of_atoms,
        calc_sequence_entropy.calc_sequence_entropy,
        calc_kmer_composition.calc_kmer_composition
    ]

    dataframe_results = []
    for func in functions:

        dataframe_results.append(func(dataframe, aa_column))
        dataframe = original_dataframe.copy()



    dataframe_results.append(calc_kmer_composition.calc_kmer_composition(dataframe, k, aa_column))


    dataframe_results = pd.concat(dataframe_results, axis=1)

    #Remove all columns of the original dataframe (as there will be duplicates)
    dataframe_results = dataframe_results[dataframe_results.columns.difference(original_dataframe)]

    #Re-concat both dataframes to get original DF + calulcated DF
    return pd.concat([original_dataframe, dataframe_results], axis=1)

    # dataframe_results.to_csv(
    #     os.path.join(csv_path_filename[0], csv_path_filename[1] + f"_{datetime.now().strftime('%d%m%Y-%H%M%S')}_{idx}.csv"),
    #     index=False)



#CSV to contain amount of rows = chunksize
#Chunksize technique saves ram for processed results and results are processed in chunks
def calc_all_features_csv(dataframe, Ncores=4, k=2, chunksize = 50000, csv_path_filename = ['', 'result'], aa_column = 'Info_window_seq'):
    calculate_export_csv(dataframe=dataframe , function = _execute_all_routines, Ncores=4, chunksize = 500, aa_column = 'Info_window_seq', **kwargs)







def calc_all_features_df(dataframe, Ncores=4, chunksize=50000):

    functions = [
        calc_aa_descriptors.calculate_df,
        calc_aa_composition.calculate_df,
        calc_aa_percentages.calculate_df,
        calc_cojoint_triads.calculate_df,
        calc_molecular_weight.calculate_df,
        calc_number_of_atoms.calculate_df,
        calc_sequence_entropy.calculate_df
    ]

    for module in module_names:
        module.calculate_df(dataframe=dataframe, Ncores=Ncores,
                             chunksize=chunksize)
