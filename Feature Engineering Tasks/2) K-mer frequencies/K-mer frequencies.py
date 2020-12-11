import time
import pandas as pd
import numpy as np
from itertools import product


pd.set_option("display.max_columns", None)

df = pd.read_csv('Ov_data.csv')

#print(df)

valid_letters = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

def calculate_kmer(k=3, dataframe=df.loc[range(2)]):
    # Create columns
    df = pd.concat(
        [dataframe, (pd.DataFrame(columns=['feat_perc_{}'.format(''.join(c)) for c in product(''.join(valid_letters), repeat=k)]))])
    df.fillna(0, inplace=True)

    #print(df)
    for row in df.itertuples():
        peptide = row.Info_window_seq
        length_of_peptide = len(peptide) #future use for excluding invalid values in frequence
        kFreq = {}

        for i in range(len(peptide)):

            k_mer = peptide[i:i + k]

            if len(k_mer) == k:
                if k_mer in kFreq:
                    kFreq[k_mer] += 1
                else:
                    kFreq[k_mer] = 1


        #set the kmer frequencies to corresponding columns for each row of df
        for kmer, freq in kFreq.items():
            df.loc[row.Index, 'feat_perc_{}'.format(kmer)] = freq #(value / length_of_peptide) * 100

    return df



start_time = time.time()
test = calculate_kmer(1, df)

print(test)
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