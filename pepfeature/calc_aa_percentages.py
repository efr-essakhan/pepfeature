import pandas as pd
from pepfeature import utils

def _calc_aa_percentages(dataframe):

    valid_letters = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    # Create columns
    for letter in valid_letters:
        dataframe['feat_Perc_{}'.format(letter)] = 0

    for row in dataframe.itertuples():

        peptide = row.Info_window_seq
        length_of_peptide = len(peptide)
        number_of_occurrences_of_letter_dict = {}

        # 1) Find out number of occurences of each letter in the peptide & figure out peptide length (i.e. number of valid amino-acid letters)
        for i in range(len(peptide)):
            peptide_letter = peptide[i]

            if peptide_letter in valid_letters:
                if peptide_letter in number_of_occurrences_of_letter_dict:
                    number_of_occurrences_of_letter_dict[peptide_letter] += 1
                else:
                    number_of_occurrences_of_letter_dict[peptide_letter] = 1
            else:
                length_of_peptide -= 1

        # 2) Find out & set the percentage of each letter in the peptides
        for aa, freq in number_of_occurrences_of_letter_dict.items():
            dataframe.loc[row.Index, 'feat_Perc_{}'.format(aa)] = (freq / length_of_peptide) * 100

    return (dataframe)


def calculate_csv(dataframe, Ncores=4, chunksize = 50000, csv_path_filename = ['', 'result']): #function that the client should call.
    utils.calculate_export_csv(dataframe = dataframe, function = _calc_aa_percentages, Ncores= Ncores, chunksize= chunksize, csv_path_filename = csv_path_filename)
