from math import log
import numpy as np
from pepfeature import utils


def _calc_sequence_entropy(dataframe: object, aa_column: str = 'Info_window_seq') -> object:
    """
    Not intended to be called directly by the user, use the functions calculate_csv or calculate_df instead.

    Calculates the entropy of given amino acid sequences

    Results appended as a new column named feat_entropy

    :param dataframe: A pandas DataFrame
    :param aa_column: Name of column in dataframe consisting of Protein Sequences to process
    :return: A Pandas DataFrame containing the calculated features appended as new columns.
    """
    """ Computes entropy of Amino Acid sequence. """

    # Create column
    dataframe['feat_entropy'] = 0

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
        dataframe.loc[row.Index, 'feat_entropy'] = entropy

    return dataframe


def calc_csv(dataframe, Ncores=4, chunksize=50000, csv_path_filename=['', 'result'],
                  aa_column='Info_window_seq'):  # function that the client should call.
    utils.calculate_export_csv(dataframe=dataframe, function=_calc_sequence_entropy, Ncores=Ncores, aa_column=aa_column,
                               chunksize=chunksize, csv_path_filename=csv_path_filename)


def calc_df(dataframe, Ncores=4, chunksize=50000,
                 aa_column='Info_window_seq'):  # function that the client should call.
    return utils.calculate_return_df(dataframe=dataframe, function=_calc_sequence_entropy, Ncores=Ncores,
                                     aa_column=aa_column, chunksize=chunksize)
