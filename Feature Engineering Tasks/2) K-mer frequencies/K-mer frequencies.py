import time
import pandas as pd
import numpy as np
from itertools import product


pd.set_option("display.max_columns", None)

df = pd.read_csv('Ov_data.csv')

#print(df)

valid_letters = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

#print(''.join(valid_letters))

#print(df)
df = pd.concat([df.loc[range(10)], (pd.DataFrame(columns=[''.join(c) for c in product(''.join(valid_letters), repeat=2)]))])
df.fillna(0, inplace=True)
print([''.join(c) for c in product(''.join(valid_letters), repeat=2)])
#print(df.loc[range(10)])
#
# def calculate_kmer(k=2, dataframe=df.loc[range(10)]):
#     # Create columns
#     df = pd.concat(
#         [dataframe, (pd.DataFrame(columns=[''.join(c) for c in product(''.join(valid_letters), repeat=k)]))])
#     df.fillna(0, inplace=True)
#
#     #print(df)
#     for row in df.itertuples():
#         peptide = row.Info_window_seq
#         length_of_peptide = len(peptide) #future use for excluding invalid values in frequence
#         kFreq = {}
#
#         for i in range(len(peptide)):
#
#             k_mer = peptide[i:i + k]
#             # print(peptide)
#             # print(k_mer)
#
#             if len(k_mer) == k:
#                 if k_mer in kFreq:
#                     kFreq[k_mer] += 1
#                 else:
#                     kFreq[k_mer] = 1
#
#
#         #print(row)
#         for key, value in kFreq.items():
#             df.loc[row.Index, 'feat_perc_{}'.format(key)] = value #(value / length_of_peptide) * 100
#
#         return df
#
#
#
#
# test = calculate_kmer()
#
# print(test)


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