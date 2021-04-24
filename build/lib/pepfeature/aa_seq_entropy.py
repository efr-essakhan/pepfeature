"""
    This module contains methods to calculate the entropy of given amino acid sequence
    returned as CSV(s) or DataFrame.

    Methods user can call from this module:
        calc_csv,
        calc_df
"""

from math import log
import numpy as np
from pepfeature import _utils


def _algorithm(dataframe: object, aa_column: str = 'Info_window_seq') -> object:
    """
    Not intended to be called directly by the user, use the functions calc_csv or calc_df instead as they have
    multi-processing functionality and more.

    Calculates the entropy of given amino acid sequences

    Results appended as a new column named feat_seq_entropy

    :param dataframe: A pandas DataFrame
    :param aa_column: Name of column in dataframe consisting of Protein Sequences to process
    :return: A Pandas DataFrame containing the calculated features appended as new columns.
    """

    # Create column
    dataframe['feat_seq_entropy'] = 0

    for row in dataframe.itertuples():

        aa_sequence = list(getattr(row, aa_column))

        total_aa_in_seq = len(aa_sequence)

        arr_counts_of_every_unique_aa = (np.unique(aa_sequence, return_counts=True))[1]

        arr_probability_of_every_aa = arr_counts_of_every_unique_aa / total_aa_in_seq

        entropy = 0.

        # Compute entropy
        for i in arr_probability_of_every_aa:
            entropy -= i * log(i, 2)

        # Store calculated entropy in corresponding row value
        dataframe.loc[row.Index, 'feat_seq_entropy'] = entropy

    return dataframe




def calc_csv(dataframe: object, save_folder: str, aa_column: str = 'Info_window_seq', Ncores: int = 1, chunksize: int = None):
    """
    Calculates the entropy of given amino acid sequences chunk by chunk from the inputted 'dataframe'.
    It saves each processed chunk as a CSV(s).

    Results appended as a new column named feat_seq_entropy

    This is a Ram efficient way of calculating the Features as the features are calculated on a single chunk of the dataframe (of
    chunksize number of rows) at a time and when a chunk has been been processed and saved as a CSV, then the chunk
    is deleted freeing up RAM.

    :param dataframe: A pandas DataFrame that contains a column/feature that is composed of purely Amino-Acid sequences (pepides).
    :param save_folder: Path to folder for saving the output.
    :param aa_column: Name of column in dataframe consisting of Amino-Acid sequences to process. Default='Info_window_seq'
    :param Ncores: Number of cores to use. default=1
    :param chunksize: Number of rows to be processed at a time. default=None (Where a 'None' object denotes no chunks but the entire dataframe to be processed)
    """

    _utils.multiprocessing_export_csv(dataframe=dataframe, function=_algorithm, Ncores=Ncores, chunksize=chunksize,
                                      save_folder=save_folder, aa_column=aa_column)


def calc_df(dataframe: object, Ncores: int = 1, aa_column: str = 'Info_window_seq'):
    """
    Calculates the entropy of given amino acid sequences

    Results appended as a new column named feat_seq_entropy

    :param dataframe: A pandas DataFrame that contains a column/feature that is composed of purely Amino-Acid sequences (pepides).
    :param Ncores: Number of cores to use. default=1
    :param aa_column: Name of column in dataframe consisting of Amino-Acid sequences to process. Default='Info_window_seq'
    :return: Pandas DataFrame

    """
    return _utils.multiprocessing_return_df(dataframe=dataframe, function=_algorithm, Ncores=Ncores,
                                            aa_column=aa_column)
