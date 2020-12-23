import time
import pandas as pd
import numpy as np
from itertools import product


pd.set_option("display.max_columns", None)

df = pd.read_csv('Ov_data.csv')

valid_letters = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

def calculate_kmer(k=2, dataframe=df.loc[range(2)]):
    # Create columns for each possible Amino-Acid k-letter combination and fill the values as 0 [e.g. for k=3, with the name format: feat_freq_XXX ]
    df = pd.concat(
        [dataframe, (pd.DataFrame(columns=['feat_freq_{}'.format(''.join(c)) for c in product(''.join(valid_letters), repeat=k)]))])
    df.fillna(0, inplace=True)


    for row in df.itertuples():
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


        #set the kmer frequencies to corresponding columns for each row of df
        for kmer, freq in kFreq.items():
            df.loc[row.Index, 'feat_freq_{}'.format(kmer)] = freq #(value / length_of_peptide) * 100

    return df



start_time = time.time()
print(calculate_kmer(1))
print("--- %s seconds ---" % (time.time() - start_time))



#Results for full df kmer calculation
#1) calculate_kmer(2, df)  --- 541.756192445755 seconds ---
#2) calculate_kmer(3, df) MemoryError: Unable to allocate 5.30 GiB for an array with shape (8000, 88842) and data type object

#Results for df.loc[range(10) kmer calculation
#1) calculate_kmer(2)  --- 0.18497300148010254 seconds ---
#2) calculate_kmer(3) --- 2.7471680641174316 seconds ---
#3)  k=4 --- 48.9020516872406 seconds ---

# As an example, consider the sequence:
#
# LLLLLLLLDVHIESG
#
# The non-zero values of 2-mer features would be (following our naming standard):
#
# LL
# LL
# LL
# ll
# ll
# ll
# ll
# ld
# dv
# vh
# hi
# ie
# es
# sg











#k  = [''.join(c) for c in product('ARNDCEQGHILKMFPSTWYV', repeat=1)] #https://stackoverflow.com/questions/48677692/generating-all-possible-k-mers-string-combinations-from-a-given-list https://www.geeksforgeeks.org/python-itertools-product/