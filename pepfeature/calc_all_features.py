"""
    Calculate statistical and physicochemical features for peptides

"""

import calc_aa_composition
import calc_aa_descriptors
import calc_aa_percentages
import calc_cojoint_triads
import calc_molecular_weight
import calc_number_of_atoms
import calc_sequence_entropy
import calc_kmer_composition

from utils import calculate_export_csv, calculate_return_df
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
# # Re-concat both dataframes
# dataframe_results = pd.concat([original_dataframe, dataframe_results], axis=1)
#
# dataframe_results.to_csv(
#     os.path.join(csv_path_filename[0], csv_path_filename[1] + f"_{datetime.now().strftime('%d%m%Y-%H%M%S')}_{idx}.csv"),
#     index=False)

def _execute_all_routines(dataframe, k, aa_column='Info_window_seq'):
    """Executes all feature calculation routines in this project
    and combines the returned dataframe into a single dataframe.

    This method is utilized in calc_all_features_csv & calc_all_features_df

    Parameters
    ----------
    dataframe : pandas DataFrame
        The file location of the spreadsheet
    k : int
        A flag used to print the columns to the console (default is False)
    aa_column : str, optional
        A flag used to print the columns to the console (default is False)

    Returns
    -------
    pandas DataFrame

    """
    # Creating a back-up of the original dataframe as later below when the dataframe is passed into df_chunking then
    # the original dataframe has parts deleted as chunks are returned by df_chunking (there is pass by reference in
    # python)
    df_copy = dataframe.copy()

    #Functions that will be run to create the dataframes with features
    functions = [
        calc_aa_descriptors._calc_aa_descriptors,
        calc_aa_composition._calc_aa_composition,
        calc_aa_percentages._calc_aa_percentages,
        calc_cojoint_triads._calc_cojoint_triads,
        calc_molecular_weight._calc_molecular_weight,
        calc_number_of_atoms._calc_number_of_atoms,
        calc_sequence_entropy._calc_sequence_entropy,
        #calc_kmer_composition._calc_kmer_composition
    ]

    df_results_list = []
    for func in functions:

        df_results_list.append(func(df_copy, aa_column))

        #Refresh the Dataset for next use since in python everything is by reference
        df_copy = dataframe.copy()

    # Seperate line for k-mer as it requires extra 'k' argument
    df_results_list.append(calc_kmer_composition._calc_kmer_composition(df_copy, k, aa_column))

    for df in df_results_list:
        #Remove original dataframe columns
        df.drop(dataframe.columns, axis = 1 , inplace=True)

    #Join all df in list into one df
    df_with_features = pd.concat(df_results_list, axis=1)

    # Re-concat both dataframes
    df_with_features = pd.concat([dataframe, df_with_features], axis=1)


    # Re-concat both dataframes to get original DF + calculated DF
    return df_with_features



def calc_all_features_csv(dataframe, k, Ncores=4, chunksize=50000, csv_path_filename=['', 'result'], aa_column='Info_window_seq'):

    calculate_export_csv(dataframe=dataframe, function=_execute_all_routines, csv_path_filename=csv_path_filename,
                         Ncores=Ncores, chunksize=chunksize, aa_column=aa_column, k=k)


def calc_all_features_df(dataframe, k, Ncores=4, chunksize=50000, aa_column='Info_window_seq'):

    return calculate_return_df(dataframe=dataframe, function=_execute_all_routines, Ncores=Ncores,
                               aa_column=aa_column, chunksize=chunksize, k=k)
