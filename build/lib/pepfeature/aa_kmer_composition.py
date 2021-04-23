"""
    This module contains methods to Calculates frequency of each k-length contiguous combination of subsequence of amino acid letters in the
    sequence. Results returned as CSV(s) or DataFrame.

    Methods user can call from this module:
        calc_csv,
        calc_df
"""

import pandas as pd
from itertools import product
from pepfeature import _utils

def _algorithm(dataframe: object, k: int, aa_column: str = 'Info_window_seq') -> object:
    """
    Not intended to be called directly by the user, use the functions calc_csv or calc_df instead as they have
    multi-processing functionality and more.

    Calculates frequency of each k-length contiguous combination of subsequence of amino acid letters in the
    sequence. (k-mers in a sequence are all the subsubsequence of length k.)

    Since there are 20 valid Amino Acid letters, there can be 400 ( 20x20) possible 2-letter combination,
    8000 (20x20x20) 3-letter combinations, etc.

    Results appended as a new column named feat_Perc_{subsequence} e.g. feat_Perc_AB, feat_Perc_BC etc.

     :param dataframe: A pandas DataFrame
     :param aa_column: Name of column in dataframe consisting of Protein Sequences to process
     :param k: The length of the contiguous combinations of subsequences of the amino acid letters in the sequence
     :return: A Pandas DataFrame containing the calculated features appended as new columns.
     """

    valid_letters = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

    # Create columns for each possible Amino-Acid k-letter combination and fill the values as 0 [e.g. for k=3, with the name format: feat_freq_XXX ]
    dataframe = pd.concat(
        [dataframe, (pd.DataFrame(columns=['feat_Perc_{}'.format(''.join(c)) for c in product(''.join(valid_letters), repeat=k)]))])
    dataframe.fillna(0, inplace=True)

    # ==================== Calculate feature ==================== #

    for row in dataframe.itertuples():
        peptide = getattr(row, aa_column)
        kFreq = {}

        # calculate the frequencies of each k-pair of letters in the peptide and store them in kFreq dictionary in the format {Amino-acid-subsequence : Frequency, ...}
        for i in range(len(peptide)):

            k_mer = peptide[i:i + k]

            # Filling dict kFreq
            if len(k_mer) == k:
                if k_mer in kFreq:
                    kFreq[k_mer] += 1
                else:
                    kFreq[k_mer] = 1


        #set the kmer frequencies to corresponding columns for each row of the dataframe
        totalQuantity = sum(kFreq.values())
        for kmer, quantity in kFreq.items():
            dataframe.loc[row.Index, 'feat_Perc_{}'.format(kmer)] = (quantity / totalQuantity)

    return dataframe



def calc_csv(k: int, dataframe: object, save_folder: str, aa_column: str = 'Info_window_seq', Ncores: int = 1, chunksize: int = None):
    """

    Calculates frequency of each k-length contiguous combination of subsequence of amino acid letters in the
    sequence chunk by chunk from the inputted 'dataframe'.
    It saves each processed chunk as a CSV(s).

    Since there are 20 valid Amino Acid letters, there can be 400 ( 20x20) possible 2-letter combination,
    8000 (20x20x20) 3-letter combinations, etc.

    Results appended as a new column named feat_Perc_{subsequence} e.g. feat_Perc_AB, feat_Perc_BC etc.

    This is a Ram efficient way of calculating the Features as the features are calculated on a single chunk of the dataframe (of
    chunksize number of rows) at a time and when a chunk has been been processed and saved as a CSV, then the chunk
    is deleted freeing up RAM.

    :param k: Length of subsequences.
    :param dataframe: A pandas DataFrame that contains a column/feature that is composed of purely Amino-Acid sequences (pepides).
    :param save_folder: Path to folder for saving the output.
    :param aa_column: Name of column in dataframe consisting of Amino-Acid sequences to process. Default='Info_window_seq'
    :param Ncores: Number of cores to use. default=1
    :param chunksize: Number of rows to be processed at a time. default=None (Where a 'None' object denotes no chunks but the entire dataframe to be processed)
    """
    _utils.calculate_export_csv(dataframe=dataframe, function=_algorithm, Ncores=Ncores,
                                chunksize=chunksize, save_folder=save_folder, aa_column=aa_column, k=k)

def calc_df(k: int, dataframe: object, Ncores: int = 1, aa_column: str = 'Info_window_seq'):
    """
    Calculates frequency of each k-length contiguous combination of subsequence of amino acid letters in the
    sequence. (k-mers in a sequence are all the subsubsequence of length k.)

    Since there are 20 valid Amino Acid letters, there can be 400 ( 20x20) possible 2-letter combination,
    8000 (20x20x20) 3-letter combinations, etc.

    Results appended as a new column named feat_Perc_{subsequence} e.g. feat_Perc_AB, feat_Perc_BC etc.


    :param k: Length of subsequences.
    :param dataframe: A pandas DataFrame that contains a column/feature that is composed of purely Amino-Acid sequences (pepides).
    :param Ncores: Number of cores to use. default=1
    :param aa_column: Name of column in dataframe consisting of Amino-Acid sequences to process. Default='Info_window_seq'
    :return: pandas DataFrame
    """
    return _utils.calculate_return_df(dataframe = dataframe, function = _algorithm, Ncores= Ncores, aa_column = aa_column, k=k)