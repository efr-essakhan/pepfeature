"""
    This module contains methods to Calculates total molecular weight for given amino acid sequences. Results
    returned as CSV(s) or DataFrame.

    Methods user can call from this module:
        calc_csv,
        calc_df
"""

import numpy as np
from pepfeature import _utils


def _algorithm(dataframe: object, aa_column: str = 'Info_window_seq') -> object:
    """
    Not intended to be called directly by the user, use the functions calc_csv or calc_df instead as they have
    multi-processing functionality and more.

    Calculates total molecular weight of the sequence.

    Calculated as a simple weighted sum of aminoacid counts, with AA weights

    Results appended as a new column named feat_molecular_weight

    :param dataframe: A pandas DataFrame
    :param aa_column: Name of column in dataframe consisting of Protein Sequences to process
    :return: A Pandas DataFrame containing the calculated features appended as new columns.
    """

    # Dictionary mapping each Amino-Acid to its respective group-value
    AA_weights_dict = {'A': 89.09, 'G': 75.07, 'V': 117.15, 'C': 121.16, 'F': 165.19, 'I': 131.17, 'L': 131.17,
                       'P': 115.13, 'M': 149.21,
                       'S': 105.09, 'T': 119.12, 'Y': 181.19,
                       'H': 155.16, 'N': 132.12, 'Q': 146.15, 'W': 204.22, 'K': 146.19, 'R': 174.20, 'D': 133.10,
                       'E': 147.13}

    # ==================== Calculate feature ==================== #

    for row in dataframe.itertuples():

        peptide = list(getattr(row, aa_column))

        every_unique_aa, counts_of_every_unique_aa = np.unique(peptide, return_counts=True)

        #Variables for each atom, to keep count of weighted sum for each aa in the peptide
        weight = 0

        for aa, counts in zip(every_unique_aa, counts_of_every_unique_aa):
            weight += (counts * AA_weights_dict[aa])

        # for i in range(len(every_unique_aa)):
        #     weight += (counts_of_every_unique_aa[i] * AA_weights_dict[every_unique_aa[i]])

        #Creating the features and setting them
        dataframe.loc[row.Index, 'feat_molecular_weight'] = weight

    return dataframe





def calc_csv(dataframe: object, save_folder: str, aa_column: str = 'Info_window_seq', Ncores: int = 1, chunksize: int = None):
    """
    Calculates total molecular weight of the amino acid sequence chunk by chunk from the inputted 'dataframe'.
    It saves each processed chunk as a CSV(s).

    Results appended as a new column named feat_molecular_weight

    This is a Ram efficient way of calculating the Features as the features are calculated on a single chunk of the dataframe (of
    chunksize number of rows) at a time and when a chunk has been been processed and saved as a CSV, then the chunk
    is deleted freeing up RAM.

    :param dataframe: A pandas DataFrame that contains a column/feature that is composed of purely Amino-Acid sequences (pepides).
    :param save_folder: Path to folder for saving the output.
    :param aa_column: Name of column in dataframe consisting of Amino-Acid sequences to process. Default='Info_window_seq'
    :param Ncores: Number of cores to use. default=1
    :param chunksize: Number of rows to be processed at a time. default=None (Where a 'None' object denotes no chunks but the entire dataframe to be processed)
    """

    #function that the client should call.
    _utils.calculate_export_csv(dataframe=dataframe, function=_algorithm, Ncores=Ncores,
                                chunksize=chunksize, save_folder=save_folder, aa_column=aa_column)

def calc_df(dataframe: object, Ncores: int = 1, aa_column: str = 'Info_window_seq'):
    """
      Calculates total molecular weight of the sequence.

    Calculated as a simple weighted sum of aminoacid counts, with AA weights

    :param dataframe: A pandas DataFrame that contains a column/feature that is composed of purely Amino-Acid sequences (pepides).
    :param Ncores: Number of cores to use. default=1
    :param aa_column: Name of column in dataframe consisting of Amino-Acid sequences to process. Default='Info_window_seq'
    :return: Pandas DataFrame

    """
    return _utils.calculate_return_df(dataframe = dataframe, function = _algorithm, Ncores= Ncores, aa_column = aa_column)