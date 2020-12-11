import time
import pandas as pd
import numpy as np
from itertools import product


pd.set_option("display.max_columns", None)

df = pd.read_csv('Ov_data.csv')


def calc_conjoint_triads(dataframe=df.loc[range(2)]):
    AA_classes_dict = {'A': '0', 'G': '0', 'V': '0', 'C': '1', 'F': '2', 'I': '2', 'L': '2', 'P': '2', 'M': '3', 'S': '3', 'T': '3', 'Y': '3',
                       'H': '4', 'N': '4', 'Q': '4', 'W': '4', 'K': '5', 'R': '5', 'D': '6', 'E': '6'}

    # return ''.join(AA_classes_dict.get(ch) for ch in 'MVRKGEKKKAKP')

    # Create columns
    df = pd.concat(
        [dataframe, (pd.DataFrame(
            columns=['feat_perc_{}'.format(''.join(c)) for c in product('0123456', repeat=3)]))])
    df.fillna(0, inplace=True)

    for row in df.itertuples():
        peptide = row.Info_window_seq
        kFreq = {}

        #represent each AA by its group value
        eqv_val = ''.join(AA_classes_dict.get(ch) for ch in peptide)

        #calculate the frequencies of each 3-number subsequence
        for i in range(len(eqv_val)):

            subsequence = eqv_val[i:i + 3]

            #Filling dict kFreq
            if len(subsequence) == 3:
                if subsequence in kFreq:
                    kFreq[subsequence] += 1
                else:
                    kFreq[subsequence] = 1

        # set the frequencies to corresponding columns for each row of df
        for sequence, freq in kFreq.items():
            df.loc[row.Index, 'feat_perc_{}'.format(sequence)] = freq  # (value / length_of_peptide) * 100

    return(df)

print(calc_conjoint_triads(df))