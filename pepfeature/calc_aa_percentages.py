from pepfeature import utils

def calc_aa_percentages(dataframe, aa_column = 'Info_window_seq'):

    valid_letters = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    # Create columns
    for letter in valid_letters:
        dataframe['feat_Perc_{}'.format(letter)] = 0

    for row in dataframe.itertuples():

        peptide = getattr(row, aa_column)
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


def calculate_csv(dataframe, Ncores=4, chunksize = 50000, csv_path_filename = ['', 'result'], aa_column = 'Info_window_seq'): #function that the client should call.
    utils.calculate_export_csv(dataframe = dataframe, function = calc_aa_percentages, Ncores= Ncores, chunksize= chunksize, aa_column = aa_column, csv_path_filename = csv_path_filename)

def calculate_df(dataframe, Ncores=4, chunksize = 50000, aa_column = 'Info_window_seq'): #function that the client should call.
    return utils.calculate_return_df(dataframe = dataframe, function = calc_aa_percentages, Ncores= Ncores, aa_column = aa_column, chunksize= chunksize)