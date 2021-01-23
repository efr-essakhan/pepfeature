from math import log, e
import numpy as np
import pandas as pd

pd.set_option("display.max_columns", None)

df = pd.read_csv('Ov_data.csv')

a = "DSSHESDSNSNEGRH"


def entropy2(aa_sequence, base=2):

    for letter in valid_letters:
        df['feat_perc_{}'.format(letter)] = 0

    """ Computes entropy of label distribution. """
    aa_sequence = list(aa_sequence)
    total_aa_in_seq = len(aa_sequence)

    if total_aa_in_seq <= 1:
        return 0

    arr_values, arr_counts = np.unique(aa_sequence, return_counts=True)
    print(arr_values)
    print(arr_counts)
    arr_probs_of_every_aa = arr_counts / total_aa_in_seq
    print(arr_probs_of_every_aa)
    n_classes = np.count_nonzero(arr_probs_of_every_aa)

    if n_classes <= 1:
        return 0

    ent = 0.

    # Compute entropy
    for i in arr_probs_of_every_aa:
        ent -= i * log(i, base)

    return ent

print(entropy2(a))

# #a = pd.Series(a)
# en(a)
# print(a)
# print(a.value_counts())
# print(en(a.value_counts()))
