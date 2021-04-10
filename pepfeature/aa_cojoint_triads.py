import pandas as pd
from pepfeature import utils
from itertools import product


def _calc_cojoint_triads(dataframe: object, aa_column: str = 'Info_window_seq') -> object:
    """
    Not intended to be called directly by the user, use the functions calculate_csv or calculate_df instead.

    Calculates conjoint triads features

    Results appended as a new column named feat_CT_{subsequence} e.g. feat_CT_305 etc.

    :param dataframe: A pandas DataFrame
    :param aa_column: Name of column in dataframe consisting of Protein Sequences to process
    :return: A Pandas DataFrame containing the calculated features appended as new columns.
    """

    # Dictionary mapping each Amino-Acid to its respective group-value
    AA_classes_dict = {'A': '0', 'G': '0', 'V': '0', 'C': '1', 'F': '2', 'I': '2', 'L': '2', 'P': '2', 'M': '3',
                       'S': '3', 'T': '3', 'Y': '3',
                       'H': '4', 'N': '4', 'Q': '4', 'W': '4', 'K': '5', 'R': '5', 'D': '6', 'E': '6'}

    # Create columns for each possible 3-number (group-value) combination and fill them with 0 [with the name format:
    # feat_CT_XXX ]
    dataframe = pd.concat(
        [dataframe, (pd.DataFrame(
            columns=['feat_CT{}'.format(''.join(c)) for c in product('0123456', repeat=3)]))])
    dataframe.fillna(0, inplace=True)

    # ==================== Calculate feature ==================== #

    for row in dataframe.itertuples():
        peptide = getattr(row, aa_column)
        kFreq = {}

        # represent each Peptide by its made-up-of Amino-Acids' group-value equivelant
        peptide_grp_val_eqv = ''.join(AA_classes_dict.get(aminoacid) for aminoacid in peptide)

        # calculate the frequencies of each 3-number subsequence and store them in kFreq dictionary in the format {
        # subsequence: frequency, ...}
        for i in range(len(peptide_grp_val_eqv)):

            subsequence = peptide_grp_val_eqv[i:i + 3]

            # Fil
            # ling dict kFreq
            if len(subsequence) == 3:

                if subsequence in kFreq:
                    kFreq[subsequence] += 1
                else:
                    kFreq[subsequence] = 1

        # set the frequencies to corresponding columns for each row of the dataframe
        totalQuantity = sum(kFreq.values())
        for sequence, quantity in kFreq.items():
            dataframe.loc[row.Index, 'feat_CT{}'.format(sequence)] = (quantity / totalQuantity)

    return (dataframe)


def calc_csv(dataframe, Ncores=4, chunksize=50000, csv_path_filename=['', 'result'],
                  aa_column='Info_window_seq'):  # function that the client should call.
    utils.calculate_export_csv(dataframe=dataframe, function=_calc_cojoint_triads, Ncores=Ncores, aa_column=aa_column,
                               chunksize=chunksize, csv_path_filename=csv_path_filename)


def calc_df(dataframe, Ncores=4, chunksize=50000,
                 aa_column='Info_window_seq'):  # function that the client should call.
    return utils.calculate_return_df(dataframe=dataframe, function=_calc_cojoint_triads, Ncores=Ncores,
                                     aa_column=aa_column, chunksize=chunksize)
