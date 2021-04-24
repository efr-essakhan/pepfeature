"""
    *** A private module ***

"""


import os
import re
import multiprocessing as mp
import pandas as pd
import functools
import datetime
import numpy as np
from datetime import datetime


def _df_chunking(df, chunksize):
    """Splits df into chunks, drops data of original df inplace"""
    count = 0  # Counter for chunks
    while len(df):
        count += 1
        # Return df chunk
        yield df.iloc[:chunksize].copy()
        # Delete data in place because it is no longer needed
        df.drop(df.index[:chunksize], inplace=True)


# Pre-processing of data
def _remove_invalid_aa(df, aa_column):
    """Removes invalid characters from each AA sequence in the DataFrame"""
    df[aa_column] = [re.sub("[BJXZ]", "", str(x)) for x in df[aa_column]]
    return df



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

    p.close()
    p.join()




def calculate_return_df(dataframe, function, Ncores=1, aa_column='Info_window_seq',
                        **kwargs):

    dataframe = _remove_invalid_aa(dataframe, aa_column) #Data preprocessing

    if Ncores > 1: # if Ncore = 1 or lower then not point of multiprocessing
        df_split = np.array_split(dataframe, Ncores)

        ctx = mp.get_context(
            'spawn')  # This guarantees that the Pool processes are just spawned and not forked from the parent process. Accordingly, none of them has access to the original DataFrame and all of them only need a tiny fraction of the parent's memory.
        p = ctx.Pool(processes=Ncores)

        # Running each of the chunks in list_df to one of the cores available and saving the DF with the features calculated as a csv
        result_df = pd.concat(p.map(functools.partial(function, aa_column=aa_column, **kwargs), df_split))

        p.close()
        p.join()  # the process will complete and only then any code after can be ran

    else:
        result_df = function(dataframe=dataframe, aa_column=aa_column, **kwargs)


    return result_df






''''chunksize parameter will cause the iterable to be split into pieces of approximately that size, and each piece is submitted as a separate task.

So in your example, yes, map will take the first 10 (approximately), submit it as a task for a single processor... then the next 10 will be submitted as another task, and so on. Note that it doesn't mean that this will make the processors alternate every 10 files, it's quite possible that processor #1 ends up getting 1-10 AND 11-20, and processor #2 gets 21-30 and 31-40.'''
