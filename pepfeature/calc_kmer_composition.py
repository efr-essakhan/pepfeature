import functools
import os

import pandas as pd
from itertools import product
from pepfeature import utils
import multiprocessing as mp

def kmer_composition(dataframe, k):

    valid_letters = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

    # Create columns for each possible Amino-Acid k-letter combination and fill the values as 0 [e.g. for k=3, with the name format: feat_freq_XXX ]
    dataframe = pd.concat(
        [dataframe, (pd.DataFrame(columns=['feat_freq_{}'.format(''.join(c)) for c in product(''.join(valid_letters), repeat=k)]))])
    dataframe.fillna(0, inplace=True)

    # ==================== Calculate feature ==================== #

    for row in dataframe.itertuples():
        peptide = row.Info_window_seq
        kFreq = {}

        # calculate the frequencies of each k-pair of letters in the peptide and store them in kFreq dictionary in the format {Amino-acid-subsequence : Frequency, ...}
        for i in range(len(peptide)):

            k_mer = peptide[i:i + k]

            # Filling dict kFreq
            if len(k_mer) == k:
                if k_mer in kFreq:
                    kFreq[k_mer] += 1
                else:
                    kFreq[k_mer] = 1


        #set the kmer frequencies to corresponding columns for each row of the dataframe
        totalQuantity = sum(kFreq.values())
        for kmer, quantity in kFreq.items():
            dataframe.loc[row.Index, 'feat_freq_{}'.format(kmer)] = (quantity / totalQuantity)

    return dataframe


# def calculate_export_csv(k, dataframe, Ncores=4, chunksize = 50000, csv_path_filename = ['', 'result']): #function that the client should call.
#
#     ctx = mp.get_context('spawn') #This guarantees that the Pool processes are just spawned and not forked from the parent process. Accordingly, none of them has access to the original DataFrame and all of them only need a tiny fraction of the parent's memory.
#     p = ctx.Pool(processes=Ncores)
#
#     #Running each of the chunks in list_df to one of the cores available and saving the DF with the features calculated as a csv
#     #for idx, result_df in enumerate(p.imap(_calc_kmer_composition, df_chunking(dataframe, chunksize))):
#     for idx, result_df in enumerate(p.imap(functools.partial(_calc_kmer_composition, k = k), utils.df_chunking(dataframe, chunksize))):
#         result_df.to_csv(os.path.join(csv_path_filename[0], csv_path_filename[1] + f"_{idx}.csv"), index = False) #_{datetime.now().strftime('d%m%Y-%H%M%S')}
#         print(result_df)
#         print('-------------------------------------------------')
#
#     p.close()
#     p.join() # the process will complete and only then any code after can be ran


def calc_kmer_composition_csv(k, dataframe, Ncores=4, chunksize = 50000, csv_path_filename = ['', 'result']): #function that the client should call.
    utils.calculate_export_csv(dataframe = dataframe, function = kmer_composition, Ncores= Ncores, chunksize= chunksize, csv_path_filename = csv_path_filename, k=k)


