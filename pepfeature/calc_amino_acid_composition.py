#calc_amino_acid_composition.py
import os
from multiprocessing import Pool
import multiprocessing as mp
import numpy as np
import pandas as pd
#from pandarallel import pandarallel
import datetime
from datetime import datetime

import psutil

pd.set_option("display.max_columns", None)

df = pd.read_csv('Ov_data.csv')

def calc_aa_composition(dataframe):

    # Dictionary mapping each Amino-Acid to its respective group-value
    AA_groups_dict = {'Tiny': ["A", "C", "G", "S", "T"], 'Small': ["A", "B", "C", "D", "G", "N", "P", "S", "T", "V"],
                       'Aliphatic': ["A", "I", "L", "V"], 'Aromatic': ["F", "H", "W", "Y"],'NonPolar':["A", "C", "F", "G", "I", "L", "M", "P", "V", "W", "Y"],
                       'Polar':["D", "E", "H", "K", "N", "Q", "R", "S", "T", "Z"],'Charged':["B", "D", "E", "H", "K", "R", "Z"],'Basic':["H", "K", "R"],
                       'Acidic':["B", "D", "E", "Z"]}

    # ==================== Calculate feature ==================== #

    for row in dataframe.itertuples():

        peptide = row.Info_window_seq
        peptide_length = len(peptide)

        for group_name, group_aa_values in AA_groups_dict.items():
            count = 0
            for aa in peptide:
                #accumlate number of times the aas appears in the particular group
                count += group_aa_values.count(aa)

            # set the frequency to corresponding columns for each row of the dataframe, column is automatically created if it doesn't exist
            dataframe.loc[row.Index, 'feat_Perc_{}'.format(group_name)] = (count / peptide_length) * 100

    return dataframe

def df_chunking(df, chunksize):
    """Splits df into chunks, drops data of original df inplace"""
    count = 0 # Counter for chunks
    while len(df):
        count += 1
        print(f'Preparing chunk {count}')
        # Return df chunk
        yield df.iloc[:chunksize].copy()
        # Delete data in place because it is no longer needed
        df.drop(df.index[:chunksize], inplace=True)


def calculate(dataframe, Ncores=4, chunksize = 50000, csv_path = 'result'): #function that the client should call.


    #list_df = [dataframe[i:i + chunksize] for i in range(0, dataframe.shape[0], chunksize)]
    #list_df = (dataframe[i:i + chunksize] for i in range(0, dataframe.shape[0], chunksize)) #generator used insted (done using round brackets instead of square)

    # creating a pool obj
    #p = Pool(processes=Ncores)

    ctx = mp.get_context('spawn')
    p = ctx.Pool(processes=Ncores)

    #Running each of the chunks in list_df to one of the cores available and saving the DF with the features calculated as a csv
    #for idx, result_df in enumerate(p.imap(calc_aa_composition, list_df)):
    for idx, result_df in enumerate(p.imap(calc_aa_composition, df_chunking(dataframe, chunksize))):
        result_df.to_csv(f'{csv_path}_{datetime.now().strftime("%d%m%Y-%H%M%S")}_{idx}.csv', index = False)
        print(result_df)
        print('-------------------------------------------------')

    p.close()
    p.join() # the process will complete and only then any code after can be ran





def dummydataframe(rows):

    dc = pd.DataFrame(np.random.randint(0, 100, size=(rows, 12))) #8500 total features from methods
    dc['Info_window_seq'] = "LLLLLLLLDVHIESG"

    return (dc)

