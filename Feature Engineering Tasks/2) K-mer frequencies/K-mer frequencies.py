import time
import pandas as pd
import numpy as np
from itertools import product


pd.set_option("display.max_columns", None)

df = pd.read_csv('Ov_data.csv')

#print(df)

valid_letters = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']





print(df)


def kmer(peptide_row, k=2):
    # Create columns
    df = pd.concat([df, (pd.DataFrame(columns=[''.join(c) for c in product('ARNDCEQGHILKMFPSTWYV', repeat=k)])).fillna(0, inplace=True)])
    #df.fillna(0, inplace=True)
    peptide = peptide_row['Info_window_seq']
    length_of_peptide = len(peptide)
    kFreq = {}

    for i in range(peptide_row(i))


#k  = [''.join(c) for c in product('ARNDCEQGHILKMFPSTWYV', repeat=1)] #https://stackoverflow.com/questions/48677692/generating-all-possible-k-mers-string-combinations-from-a-given-list https://www.geeksforgeeks.org/python-itertools-product/