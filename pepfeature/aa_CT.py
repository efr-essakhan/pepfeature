import pandas as pd
from pepfeature import _utils
from itertools import product


def _algorithm(dataframe: object, aa_column: str = 'Info_window_seq') -> object:
    """
    Not intended to be called directly by the user, use the functions calc_csv or calc_df instead as they have
    multi-processing functionality and more.

    Calculates conjoint triads features - the actual algorithm to do so

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
    # feat_CTXXX ]
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



def calc_csv(dataframe: object, save_folder: str, aa_column: str = 'Info_window_seq', Ncores: int = 1, chunksize: int = None):
    """
    Calculates conjoint triads features chunk by chunk from the inputted 'dataframe'.
    It saves each processed chunk as a CSV(s).

    Results appended as a new column named feat_CT_{subsequence} e.g. feat_CT_305 etc.

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
                                chunksize=chunksize, save_folder=save_folder, aa_column=aa_column)


def calc_df(dataframe: object, Ncores: object = 1, aa_column: object = 'Info_window_seq'):
    """
    Calculates conjoint triads features

    Results appended as a new column named feat_CT_{subsequence} e.g. feat_CT_305 etc.

    :param dataframe: A pandas DataFrame that contains a column/feature that is composed of purely Amino-Acid sequences (pepides).
    :param Ncores: Number of cores to use. default=1
    :param aa_column: Name of column in dataframe consisting of Amino-Acid sequences to process. Default='Info_window_seq'
    :return: Pandas DataFrame

    """

    return _utils.calculate_return_df(dataframe=dataframe, function=_algorithm, Ncores=Ncores,
                                      aa_column=aa_column)
