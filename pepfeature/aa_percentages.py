from pepfeature import utils


def _calc_aa_percentages(dataframe: object, aa_column: str = 'Info_window_seq') -> object:
    """
    Not intended to be called directly by the user, use the functions calculate_csv or calculate_df instead.

    Calculates the percent of each aminoacid in the peptides (Amino Acid Sequences). This results in 20 new features,
    which should be called feat_perc_A, feat_perc_C, ..., feat_perc_Y.

    Results appended as a new column named feat_Perc_{aa letter} e.g. feat_Perc_A, feat_Perc_C, ..., feat_perc_Y.

    :param dataframe: A pandas DataFrame
    :param aa_column: Name of column in dataframe consisting of Protein Sequences to process
    :return: A Pandas DataFrame containing the calculated features appended as new columns.
    """
    valid_letters = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    # Create columns
    for letter in valid_letters:
        dataframe['feat_Perc_{}'.format(letter)] = 0

    for row in dataframe.itertuples():

        peptide = getattr(row, aa_column)
        length_of_peptide = len(peptide)
        number_of_occurrences_of_letter_dict = {}

        # 1) Find out number of occurences of each letter in the peptide & figure out peptide length (i.e. number of
        # valid amino-acid letters)
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

    return dataframe


def calc_csv(dataframe, Ncores=4, rows_per_csv=None, csv_path_filename=['', 'result'],
                  aa_column='Info_window_seq'):  # function that the client should call.
    utils.calculate_export_csv(dataframe=dataframe, function=_calc_aa_percentages, Ncores=Ncores,
                               rows_per_csv=rows_per_csv, csv_path_filename=csv_path_filename, aa_column=aa_column)


def calc_df(dataframe, Ncores=4, chunksize=50000,
                 aa_column='Info_window_seq'):  # function that the client should call.
    return utils.calculate_return_df(dataframe=dataframe, function=_calc_aa_percentages, Ncores=Ncores,
                                     aa_column=aa_column, chunksize=chunksize)
