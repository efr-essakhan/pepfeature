import numpy as np
from pepfeature import utils

def _calc_molecular_weight(dataframe):

    # Dictionary mapping each Amino-Acid to its respective group-value
    AA_weights_dict = {'A': 89.09, 'G': 75.07, 'V': 117.15, 'C': 121.16, 'F': 165.19, 'I': 131.17, 'L': 131.17,
                       'P': 115.13, 'M': 149.21,
                       'S': 105.09, 'T': 119.12, 'Y': 181.19,
                       'H': 155.16, 'N': 132.12, 'Q': 146.15, 'W': 204.22, 'K': 146.19, 'R': 174.20, 'D': 133.10,
                       'E': 147.13}

    # ==================== Calculate feature ==================== #

    for row in dataframe.itertuples():

        peptide = list(row.Info_window_seq)

        every_unique_aa, counts_of_every_unique_aa = np.unique(peptide, return_counts=True)

        #Variables for each atom, to keep count of weighted sum for each aa in the peptide
        weight = 0

        for aa, counts in zip(every_unique_aa, counts_of_every_unique_aa):
            weight += (counts * AA_weights_dict[aa])

        # for i in range(len(every_unique_aa)):
        #     weight += (counts_of_every_unique_aa[i] * AA_weights_dict[every_unique_aa[i]])

        #Creating the features and setting them
        dataframe.loc[row.Index, 'feat_weight'] = weight

    return dataframe

def calculate_csv(dataframe, Ncores=4, chunksize = 50000, csv_path_filename = ['', 'result']): #function that the client should call.
    utils.calculate_export_csv(dataframe = dataframe, function = _calc_molecular_weight, Ncores= Ncores, chunksize= chunksize, csv_path_filename = csv_path_filename)