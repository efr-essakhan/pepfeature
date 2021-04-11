from pepfeature import utils


def _calc_aa_composition(dataframe: object, aa_column: str = 'Info_window_seq') -> object:
    """
    Not intended to be called directly by the user, use the functions calculate_csv or calculate_df instead.

    Calculates Frequency of AA types for given amino acid sequences

    For each sequence calculates nine features corresponding to the percentage of each Amino Acid type in the sequences

    Results appended as a new columns named feat_perc_{group-value} e.g.  feat_Perc_Tiny, feat_Perc_Small etc.

    :param dataframe: A pandas DataFrame
    :param aa_column: Name of column in dataframe consisting of Protein Sequences to process
    :return: A Pandas DataFrame containing the calculated features appended as new columns.
    """
    # Dictionary mapping each Amino-Acid to its respective group-value
    AA_groups_dict = {'Tiny': ["A", "C", "G", "S", "T"], 'Small': ["A", "B", "C", "D", "G", "N", "P", "S", "T", "V"],
                      'Aliphatic': ["A", "I", "L", "V"], 'Aromatic': ["F", "H", "W", "Y"],
                      'NonPolar': ["A", "C", "F", "G", "I", "L", "M", "P", "V", "W", "Y"],
                      'Polar': ["D", "E", "H", "K", "N", "Q", "R", "S", "T", "Z"],
                      'Charged': ["B", "D", "E", "H", "K", "R", "Z"], 'Basic': ["H", "K", "R"],
                      'Acidic': ["B", "D", "E", "Z"]}

    # ==================== Calculate feature ==================== #

    for row in dataframe.itertuples():

        peptide = getattr(row, aa_column)
        peptide_length = len(peptide)

        for group_name, group_aa_values in AA_groups_dict.items():
            count = 0
            for aa in peptide:
                # accumlate number of times the aas appears in the particular group
                count += group_aa_values.count(aa)

            # set the frequency to corresponding columns for each row of the dataframe, column is automatically created if it doesn't exist
            dataframe.loc[row.Index, 'feat_Perc_{}'.format(group_name)] = (count / peptide_length) #* 100

    return dataframe


def calc_csv(dataframe, Ncores=4, rows_per_csv=None, csv_path_filename=['', 'result'],
                  aa_column='Info_window_seq'):  # function that the client should call.
    utils.calculate_export_csv(dataframe=dataframe, function=_calc_aa_composition, Ncores=Ncores,
                               rows_per_csv=rows_per_csv, csv_path_filename=csv_path_filename, aa_column=aa_column)


def calc_df(dataframe, Ncores=4, chunksize=50000,
                 aa_column='Info_window_seq'):  # function that the client should call.
    return utils.calculate_return_df(dataframe=dataframe, function=_calc_aa_composition, Ncores=Ncores,
                                     aa_column=aa_column, chunksize=chunksize)
