from math import log
import numpy as np
from pepfeature import utils

def calc_sequence_entropy(dataframe, aa_column = 'Info_window_seq'):
    """ Computes entropy of Amino Acid sequence. """

    # Create column
    dataframe['feat_entropy'] = 0

    for row in dataframe.itertuples():

        aa_sequence = list(getattr(row, aa_column))

        total_aa_in_seq = len(aa_sequence)

        arr_counts_of_every_unique_aa = (np.unique(aa_sequence, return_counts=True))[1]

        arr_probability_of_every_aa = arr_counts_of_every_unique_aa / total_aa_in_seq

        entropy = 0.

        # Compute entropy
        for i in arr_probability_of_every_aa:
            entropy -= i * log(i, 2)

        # Store calculated entropy in corresponding row value
        dataframe.loc[row.Index, 'feat_entropy'] = entropy

    return dataframe

def calculate_csv(dataframe, Ncores=4, chunksize = 50000, csv_path_filename = ['', 'result'], aa_column = 'Info_window_seq'): #function that the client should call.
    utils.calculate_export_csv(dataframe = dataframe, function = calc_sequence_entropy, Ncores= Ncores, aa_column = aa_column, chunksize= chunksize, csv_path_filename = csv_path_filename)

def calculate_df(dataframe, Ncores=4, chunksize = 50000, aa_column = 'Info_window_seq'): #function that the client should call.
    return utils.calculate_return_df(dataframe = dataframe, function = calc_sequence_entropy, Ncores= Ncores, aa_column = aa_column, chunksize= chunksize)