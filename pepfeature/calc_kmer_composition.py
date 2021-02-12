import pandas as pd
from itertools import product

def calc_kmer_composition(dataframe, k):

    valid_letters = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

    # Create columns for each possible Amino-Acid k-letter combination and fill the values as 0 [e.g. for k=3, with the name format: feat_freq_XXX ]
    dataframe = pd.concat(
        [dataframe, (pd.DataFrame(columns=['feat_freq_{}'.format(''.join(c)) for c in product(''.join(valid_letters), repeat=k)]))])
    dataframe.fillna(0, inplace=True)

    # ==================== Calculate feature ==================== #

    for row in dataframe.itertuples():
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


        #set the kmer frequencies to corresponding columns for each row of the dataframe
        totalQuantity = sum(kFreq.values())
        for kmer, quantity in kFreq.items():
            dataframe.loc[row.Index, 'feat_freq_{}'.format(kmer)] = (quantity / totalQuantity)

    return dataframe
