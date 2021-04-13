"""
    Methods to Calculate all features at once either returned as a DataFrame or stored into CSV

"""

import _utils

def calc_csv(dataframe: object, k: int, save_folder: str, aa_column: str = 'Info_window_seq', Ncores: int = 1, chunksize: int = None):
    """
    Calculates all features that this package calculates at once chunk by chunk from the inputted 'dataframe'.
    It saves each processed chunk as a CSV(s).

    Results appended as a new column to dataframe

    This is a Ram efficient way of calculating the Features as the features are calculated on a single chunk of the dataframe (of
    chunksize number of rows) at a time and when a chunk has been been processed and saved as a CSV, then the chunk
    is deleted freeing up RAM.

    :param dataframe: A pandas DataFrame that contains a column/feature that is composed of purely Amino-Acid sequences (pepides).
    :param k: Length of subsequences (this is used to calculate k-mer composition features)
    :param save_folder: Path to folder for saving the output.
    :param aa_column: Name of column in dataframe consisting of Amino-Acid sequences to process. Default='Info_window_seq'
    :param Ncores: Number of cores to use. default=1
    :param chunksize: Number of rows to be processed at a time. default=None (Where a 'None' object denotes no chunks but the entire dataframe to be processed)
    """
    _utils.calculate_export_csv(dataframe=dataframe, function=_utils._execute_all_routines, Ncores=Ncores,
                                chunksize=chunksize, save_folder=save_folder, aa_column=aa_column, k=k)


def calc_df(dataframe: object, k: int, Ncores: int = 1, aa_column: str = 'Info_window_seq'):
    """
    Calculate all features that this package calculates at once

    Results appended as a new column to dataframe

    :param dataframe: A pandas DataFrame that contains a column/feature that is composed of purely Amino-Acid sequences (pepides).
    :param k: Length of subsequences (this is used to calculate k-mer composition features)
    :param Ncores: Number of cores to use. default=1
    :param aa_column: Name of column in dataframe consisting of Amino-Acid sequences to process. Default='Info_window_seq'
    :return: pandas DataFrame
    """

    return _utils.calculate_return_df(dataframe=dataframe, function=_utils._execute_all_routines, Ncores=Ncores,
                                      aa_column=aa_column, k=k)
