"""
    This module contains methods to Calculate all the proportion (out of 1) of each Amino Acid in the peptide. Results
    returned as CSV(s) or DataFrame.

    Methods user can call from this module:
        calc_csv,
        calc_df
"""

from pepfeature import _utils
import pandas as pd


def _algorithm(dataframe: object, aa_column: str = 'Info_window_seq') -> object:
    """
    Not intended to be called directly by the user, use the functions calc_csv or calc_df instead as they have
    multi-processing functionality and more.

    Calculates the proportion (out of 1) of each aminoacid in the peptides (Amino Acid Sequences).

    Results appended as a new column named feat_Perc_{aa letter} e.g. feat_Perc_A, feat_Perc_C, ..., feat_Perc_Y.

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
        # for i in range(len(peptide)):
        #     peptide_letter = peptide[i]
        #
        #     if peptide_letter in valid_letters:
        #         if peptide_letter in number_of_occurrences_of_letter_dict:
        #             number_of_occurrences_of_letter_dict[peptide_letter] += 1
        #         else:
        #             number_of_occurrences_of_letter_dict[peptide_letter] = 1
        #     else:
        #         length_of_peptide -= 1

        for letter in peptide:
            if letter in number_of_occurrences_of_letter_dict:
                number_of_occurrences_of_letter_dict[letter] += 1
            else:
                number_of_occurrences_of_letter_dict[letter] = 1



        # 2) Find out & set the percentage of each letter in the peptides
        for aa, freq in number_of_occurrences_of_letter_dict.items():
            dataframe.loc[row.Index, f'feat_Perc_{aa}'] = (freq / length_of_peptide) #* 100

    return dataframe





def calc_csv(dataframe: object, save_folder: str, aa_column: str = 'Info_window_seq', Ncores: int = 1, chunksize: int = None):
    """
    Calculates the proportion (out of 1) od each Amino-Acid in the peptides (Amino Acid Sequences) chunk by chunk of the inputted 'dataframe'.
    It saves each processed chunk as a CSV(s).

    This results in 20 new features per chunk, appended as new columns named feat_Perc_{Amino-Acid letter} e.g. feat_Per_A,
    feat_Perc_C, ..., feat_Perc_Y.

    This is a Ram efficient way of calculating the Features as the features are calculated on a single chunk of the dataframe (of
    chunksize number of rows) at a time and when a chunk has been been processed and saved as a CSV, then the chunk
    is deleted freeing up RAM.

    :param dataframe: A pandas DataFrame that contains a column/feature that is composed of purely Amino-Acid sequences (pepides).
    :param save_folder: Path to folder for saving the output.
    :param aa_column: Name of column in dataframe consisting of Amino-Acid sequences to process. Default='Info_window_seq'
    :param Ncores: Number of cores to use. default=1
    :param chunksize: Number of rows to be processed at a time. default=None (Where a 'None' object denotes no chunks but the entire dataframe to be processed)
    """
    _utils.calculate_export_csv(dataframe=dataframe, function=_algorithm, Ncores=Ncores,
                                save_folder=save_folder, aa_column=aa_column, chunksize=chunksize)

def calc_df(dataframe: object, Ncores: object = 1, aa_column: object = 'Info_window_seq'):
    """
     Calculates the proportion (out of 1) of each aminoacid in the peptides (Amino Acid Sequences).

    Results appended as a new column named feat_Perc_{aa letter} e.g. feat_Perc_A, feat_Perc_C, ..., feat_Perc_Y.

    :param dataframe: A pandas DataFrame that contains a column/feature that is composed of purely Amino-Acid sequences (pepides).
    :param Ncores: Number of cores to use. default=1
    :param aa_column: Name of column in dataframe consisting of Amino-Acid sequences to process. Default='Info_window_seq'
    :return: Pandas DataFrame

    """

    return _utils.calculate_return_df(dataframe=dataframe, function=_algorithm, Ncores=Ncores,
                                      aa_column=aa_column)
