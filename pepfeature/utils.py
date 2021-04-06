import os
import re
from multiprocessing import Pool
import multiprocessing as mp
import numpy as np
import pandas as pd
import functools
import datetime
from datetime import datetime



def df_chunking(df, chunksize):
    """Splits df into chunks, drops data of original df inplace"""
    count = 0  # Counter for chunks
    while len(df):
        count += 1
        print(f'Preparing chunk {count}')
        # Return df chunk
        yield df.iloc[:chunksize].copy()
        # Delete data in place because it is no longer needed
        df.drop(df.index[:chunksize], inplace=True)


#CSV to contain amount of rows = chunksize
#Chunksize technique saves ram for processed results and results are processed in chunks
def calculate_export_csv(dataframe, function, Ncores=4, chunksize = 50000, csv_path_filename = ['', 'result'], aa_column = 'Info_window_seq',
                         **kwargs): # **kwargs used as a compromise to generalise this function to also be compatible with k-mer calc routine

    dataframe = remove_invalid_aa(dataframe, aa_column)
    ctx = mp.get_context('spawn') #This guarantees that the Pool processes are just spawned and not forked from the parent process. Accordingly, none of them has access to the original DataFrame and all of them only need a tiny fraction of the parent's memory.
    p = ctx.Pool(processes=Ncores)

    #Running each of the chunks in list_df to one of the cores available and saving the (chunk) DF with the features calculated as a csv
    for idx, result_df in enumerate(p.imap(functools.partial(function, aa_column=aa_column, **kwargs), df_chunking(dataframe, chunksize))):
        result_df.to_csv(os.path.join(csv_path_filename[0], csv_path_filename[1] + f"_{datetime.now().strftime('%d%m%Y-%H%M%S')}_{idx}.csv"), index = False) #_{datetime.now().strftime('d%m%Y-%H%M%S')}

        print(result_df)
        print('-------------------------------------------------')

    p.close()
    p.join() # the process will complete and only then any code after can be ran

#Here chunksize's utility is for distributing how many (chunksize) rows across cores rather then also only proccesing the chunk at a time in memory - here saving ram is not an objective unlike the csv routine above
def calculate_return_df(dataframe, function, Ncores=4, chunksize = 500, aa_column = 'Info_window_seq', **kwargs): #function that the client should call.

    list_df = [dataframe[i:i + chunksize] for i in range(0, dataframe.shape[0], chunksize)]

    ctx = mp.get_context('spawn') #This guarantees that the Pool processes are just spawned and not forked from the parent process. Accordingly, none of them has access to the original DataFrame and all of them only need a tiny fraction of the parent's memory.
    p = ctx.Pool(processes=Ncores)

    #Running each of the chunks in list_df to one of the cores available and saving the DF with the features calculated as a csv
    result_df = pd.concat(p.map(functools.partial(function, aa_column=aa_column, **kwargs), list_df))

    p.close()
    p.join() # the process will complete and only then any code after can be ran

    return result_df

#Pre-processing of data
def remove_invalid_aa(df, aa_column):
    df[aa_column] = [re.sub("[BJXZ]", "", str(x)) for x in df[aa_column]]
    return df


#For testing purposes of the functions in this file
def dummydataframe(rows):

    dc = pd.DataFrame(np.random.randint(0, 100, size=(rows, 12))) #8500 total features from methods
    dc['Info_window_seq'] = "LLLLLLLLDVHIESG"

    return (dc)