import time
import pandas as pd
import numpy as np
from itertools import product


pd.set_option("display.max_columns", None)

df = pd.read_csv('Ov_data.csv')


def calc_conjoint_triads(dataframe=df.loc[range(2)]):

    #Dictionary mapping each Amino-Acid to its respective group-value
    AA_classes_dict = {'A': '0', 'G': '0', 'V': '0', 'C': '1', 'F': '2', 'I': '2', 'L': '2', 'P': '2', 'M': '3', 'S': '3', 'T': '3', 'Y': '3',
                       'H': '4', 'N': '4', 'Q': '4', 'W': '4', 'K': '5', 'R': '5', 'D': '6', 'E': '6'}

    # Create columns for each possible 3-number (group-value) combination and fill them with 0 [with the name format: feat_CT_XXX ]
    df = pd.concat(
        [dataframe, (pd.DataFrame(
            columns=['feat_CT_{}'.format(''.join(c)) for c in product('0123456', repeat=3)]))])
    df.fillna(0, inplace=True)

    for row in df.itertuples():
        peptide = row.Info_window_seq
        kFreq = {}

        #represent each Peptide by its made-up-of Amino-Acids' group-value equivelant
        peptide_grp_val_eqv = ''.join(AA_classes_dict.get(aminoacid) for aminoacid in peptide)

        #calculate the frequencies of each 3-number subsequence and store them in kFreq dictionary in the format {subsequence: frequency, ...}
        for i in range(len(peptide_grp_val_eqv)):

            subsequence = peptide_grp_val_eqv[i:i + 3]

            #Filling dict kFreq
            if len(subsequence) == 3:
                if subsequence in kFreq:
                    kFreq[subsequence] += 1
                else:
                    kFreq[subsequence] = 1

        # set the frequencies to corresponding columns for each row of df
        for sequence, freq in kFreq.items():
            df.loc[row.Index, 'feat_CT_{}'.format(sequence)] = freq

    return(df)

start_time = time.time()
print(calc_conjoint_triads())
print("--- %s seconds ---" % (time.time() - start_time))


#Above code is tested and it works.

# Time Results for df.loc[range(2)] calculation:
# --- 0.11994695663452148 seconds ---

# Time Results for df.loc[range(100)] calculation:
# --- 0.37883639335632324 seconds ---

# Time Results for df.loc[range(100)] calculation:
# --- 2.6594951152801514 seconds ---

# Time Results for df.loc[range(10000)] calculation:
# --- 27.527163982391357 seconds ---



#Orignal task example to replicate:
# d = {'Info_window_seq': ['MVRKGEKKKAKP']}
# print(calc_conjoint_triads(pd.DataFrame(data=d)))