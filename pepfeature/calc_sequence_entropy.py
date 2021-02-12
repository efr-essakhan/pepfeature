from math import log
import numpy as np
import pandas as pd
import time

pd.set_option("display.max_columns", None)

df = pd.read_csv('Ov_data.csv')

def calc_sequence_entropy(dataframe):
    """ Computes entropy of Amino Acid sequence. """

    # Create column
    dataframe['feat_entropy'] = 0

    for row in dataframe.itertuples():

        aa_sequence = list(row.Info_window_seq)

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

start_time = time.time()
print(entropy(df))
print("--- %s seconds ---" % (time.time() - start_time))


#Above code works 23 Jan 2021
#--- 45.34812784194946 seconds --- for full df