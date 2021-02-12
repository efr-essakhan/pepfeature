import pandas as pd
import numpy as np

def calc_number_of_atoms(dataframe):

    # Dataframe holding the number of each type of atom (C, H, O, N, S) for each AA:
    atom_groups_df = pd.DataFrame(data={'nC': [3, 3, 4, 5, 9, 2, 6, 6, 6, 6, 5, 4, 5, 5, 6, 3, 4, 5, 11, 9],
                                        'nH': [7, 7, 7, 9, 11, 5, 9, 13, 14, 13, 11, 8, 9, 10, 14, 7, 9, 11, 12, 11],
                                        'nN': [1, 1, 1, 1, 1, 1, 3, 1, 2, 1, 1, 2, 1, 2, 4, 1, 1, 1, 2, 1],
                                        'nO': [2, 2, 4, 4, 2, 2, 2, 2, 2, 2, 2, 3, 2, 3, 2, 3, 3, 2, 2, 3],
                                        'nS': [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]},
                                  index=['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S',
                                         'T', 'V', 'W', 'Y'])

    # ==================== Calculate feature ==================== #

    for row in dataframe.itertuples():

        peptide = list(row.Info_window_seq)

        every_unique_aa, counts_of_every_unique_aa = np.unique(peptide, return_counts=True)

        #Variables for each atom, to keep count of weighted sum for each aa in the peptide
        count_nC = 0
        count_nH = 0
        count_nN = 0
        count_nO = 0
        count_nS = 0


        for i in range(len(every_unique_aa)):
            count_nC+= (counts_of_every_unique_aa[i] * atom_groups_df.loc[every_unique_aa[i], 'nC'])
            count_nH+= (counts_of_every_unique_aa[i] * atom_groups_df.loc[every_unique_aa[i], 'nH'])
            count_nN+= (counts_of_every_unique_aa[i] * atom_groups_df.loc[every_unique_aa[i], 'nN'])
            count_nO+= (counts_of_every_unique_aa[i] * atom_groups_df.loc[every_unique_aa[i], 'nO'])
            count_nS+= (counts_of_every_unique_aa[i] * atom_groups_df.loc[every_unique_aa[i], 'nS'])

        #Creating the features and setting them
        dataframe.loc[row.Index, 'feat_nC'] = count_nC
        dataframe.loc[row.Index, 'feat_nH'] = count_nH
        dataframe.loc[row.Index, 'feat_nN'] = count_nN
        dataframe.loc[row.Index, 'feat_nO'] = count_nO
        dataframe.loc[row.Index, 'feat_nS'] = count_nS

    return dataframe
