from pepfeature import utils

def _calc_aa_composition(dataframe, aa_column = 'Info_window_seq'):

    # Dictionary mapping each Amino-Acid to its respective group-value
    AA_groups_dict = {'Tiny': ["A", "C", "G", "S", "T"], 'Small': ["A", "B", "C", "D", "G", "N", "P", "S", "T", "V"],
                       'Aliphatic': ["A", "I", "L", "V"], 'Aromatic': ["F", "H", "W", "Y"],'NonPolar':["A", "C", "F", "G", "I", "L", "M", "P", "V", "W", "Y"],
                       'Polar':["D", "E", "H", "K", "N", "Q", "R", "S", "T", "Z"],'Charged':["B", "D", "E", "H", "K", "R", "Z"],'Basic':["H", "K", "R"],
                       'Acidic':["B", "D", "E", "Z"]}

    # ==================== Calculate feature ==================== #

    for row in dataframe.itertuples():

        peptide = getattr(row, aa_column)
        peptide_length = len(peptide)

        for group_name, group_aa_values in AA_groups_dict.items():
            count = 0
            for aa in peptide:
                #accumlate number of times the aas appears in the particular group
                count += group_aa_values.count(aa)

            # set the frequency to corresponding columns for each row of the dataframe, column is automatically created if it doesn't exist
            dataframe.loc[row.Index, 'feat_Perc_{}'.format(group_name)] = (count / peptide_length) * 100

    return dataframe

def calculate_csv(dataframe, Ncores=4, chunksize = 50000, csv_path_filename = ['', 'result'], aa_column = 'Info_window_seq'): #function that the client should call.
    utils.calculate_export_csv(dataframe = dataframe, function = _calc_aa_composition, Ncores= Ncores, chunksize= chunksize, aa_column = aa_column, csv_path_filename = csv_path_filename)

def calculate_df(dataframe, Ncores=4, chunksize = 50000, aa_column = 'Info_window_seq'): #function that the client should call.
    return utils.calculate_return_df(dataframe = dataframe, function = _calc_aa_composition, Ncores= Ncores, aa_column = aa_column, chunksize= chunksize)