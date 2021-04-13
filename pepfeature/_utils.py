import os
import re
import multiprocessing as mp
import pandas as pd
import functools
import datetime
import numpy as np
import pepfeature as pep
from datetime import datetime


def _df_chunking(df, chunksize):
    """Splits df into chunks, drops data of original df inplace"""
    count = 0  # Counter for chunks
    while len(df):
        count += 1
        print(f'Preparing chunk {count}')
        # Return df chunk
        yield df.iloc[:chunksize].copy()
        # Delete data in place because it is no longer needed
        df.drop(df.index[:chunksize], inplace=True)


# Pre-processing of data
def _remove_invalid_aa(df, aa_column):
    """Removes invalid characters from each AA sequence in the DataFrame"""
    df[aa_column] = [re.sub("[BJXZ]", "", str(x)) for x in df[aa_column]]
    return df

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
        pep.aa_seq_entropy._algorithm,
        pep.aa_num_of_atoms._algorithm,
        pep.aa_molecular_weight._algorithm,
        pep.aa_composition._algorithm,
        pep.aa_descriptors._algorithm,
        pep.aa_CT._algorithm,
        pep.aa_percentages._algorithm,
        #pep.aa_kmer_composition._calc_kmer_composition #This one requires different arguments so will have to deal with it seperatly
    ]

    df_results_list = []
    for func in functions:

        df_results_list.append(func(df_copy, aa_column))

        #Refresh the Dataset for next use since in python everything is by reference
        df_copy = dataframe.copy()

    # Seperate line for k-mer as it requires extra 'k' argument
    df_results_list.append(pep.aa_kmer_composition._algorithm(df_copy, k, aa_column))

    for df in df_results_list:
        #Remove original dataframe columns
        df.drop(dataframe.columns, axis = 1 , inplace=True)

    #Join all df in list into one df
    df_with_features = pd.concat(df_results_list, axis=1)

    # Re-concat both dataframes
    df_with_features = pd.concat([dataframe, df_with_features], axis=1)

    # Re-concat both dataframes to get original DF + calculated DF
    return df_with_features



# Chunksize technique saves ram for processed results and results are processed in chunks
def calculate_export_csv(dataframe, function, Ncores=1, chunksize=None, save_folder='',
                         aa_column='Info_window_seq',
                         **kwargs):  # **kwargs used as a compromise to generalise this function to also be compatible with k-mer calc routine

    if chunksize == None:
        chunksize = dataframe.shape[0] #number of rows = number of rows in dataframe

    if save_folder != "":
        save_folder = f'{save_folder}' + "\\"


    dataframe = _remove_invalid_aa(dataframe, aa_column)

    ctx = mp.get_context(
        'spawn')  # This guarantees that the Pool processes are just spawned and not forked from the parent process. Accordingly, none of them has access to the original DataFrame and all of them only need a tiny fraction of the parent's memory.
    p = ctx.Pool(processes=Ncores)

    # Running each of the chunks in list_df across one of the cores available and saving the (chunk) DF with the features calculated as a csv
    for idx, result_df in enumerate(p.imap(functools.partial(function, aa_column=aa_column, **kwargs),
                                           _df_chunking(dataframe, chunksize))):

        result_df.to_csv(os.path.join(save_folder + f"_{datetime.now().strftime('%d%m%Y-%H%M%S')}_{idx}.csv"),
                         index=False)

        print(result_df)
        print('-------------------------------------------------')

    p.close()
    p.join()




def calculate_return_df(dataframe, function, Ncores=1, aa_column='Info_window_seq',
                        **kwargs):

    dataframe = _remove_invalid_aa(dataframe, aa_column)

    df_split = np.array_split(dataframe, Ncores)

    ctx = mp.get_context(
        'spawn')  # This guarantees that the Pool processes are just spawned and not forked from the parent process. Accordingly, none of them has access to the original DataFrame and all of them only need a tiny fraction of the parent's memory.
    p = ctx.Pool(processes=Ncores)

    # Running each of the chunks in list_df to one of the cores available and saving the DF with the features calculated as a csv
    result_df = pd.concat(p.map(functools.partial(function, aa_column=aa_column, **kwargs), df_split))

    p.close()
    p.join()  # the process will complete and only then any code after can be ran

    return result_df






''''chunksize parameter will cause the iterable to be split into pieces of approximately that size, and each piece is submitted as a separate task.

So in your example, yes, map will take the first 10 (approximately), submit it as a task for a single processor... then the next 10 will be submitted as another task, and so on. Note that it doesn't mean that this will make the processors alternate every 10 files, it's quite possible that processor #1 ends up getting 1-10 AND 11-20, and processor #2 gets 21-30 and 31-40.'''
