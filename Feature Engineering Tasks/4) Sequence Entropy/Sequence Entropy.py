from math import log
import numpy as np
import pandas as pd
import time

pd.set_option("display.max_columns", None)

df = pd.read_csv('Ov_data.csv')

def entropy(dataframe):

    dataframe['feat_entropy'] = 0

    for row in dataframe.itertuples():

        """ Computes entropy of Amino Acid sequence. """
        aa_sequence = list(row.Info_window_seq)
        total_aa_in_seq = len(aa_sequence)

        arr_values, arr_counts = np.unique(aa_sequence, return_counts=True)
        arr_probs_of_every_aa = arr_counts / total_aa_in_seq

        entropy = 0.

        # Compute entropy
        for i in arr_probs_of_every_aa:
            entropy -= i * log(i, 2)

        dataframe.loc[row.Index, 'feat_entropy'] = entropy

    return dataframe

start_time = time.time()
print(entropy(df.loc[range(100)]))
print("--- %s seconds ---" % (time.time() - start_time))
