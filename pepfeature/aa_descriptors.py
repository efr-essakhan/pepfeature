from pepfeature import utils
import pepfeature as pep
import numpy as np
import pandas as pd

def _calc_aa_descriptors(dataframe, aa_column= 'Info_window_seq'):
    """
    Not intended to be called directly by the user, use the functions calculate_csv or calculate_df instead.

    Calculates AA descriptors features

    Results appended as a new columns named feat_{property} e.g. feat_BLOSUM9

    :param dataframe: A pandas DataFrame
    :param aa_column: Name of column in dataframe consisting of Protein Sequences to process
    :return: A Pandas DataFrame containing the calculated features appended as new columns.
    """

    # Dictionary mapping each Amino-Acid to its respective group-value
    AA_properties_df = []
    properties = ['crucianiProperties', 'kideraFactors', 'zScales', 'FASGAI', 'stScales', 'tScales', 'VHSE', 'ProtFP',
                  'BLOSUM','MSWHIM']
    for sheet in properties:
        AA_properties_df.append(pd.read_excel('AAdescriptors.xlsx', sheet, index_col=0, header=0))

    for row in dataframe.itertuples():

        peptide = list(getattr(row, aa_column))

        every_unique_aa, counts_of_every_unique_aa = np.unique(peptide, return_counts=True)

        for df in AA_properties_df:

            for row_df in df.itertuples():
                # to keep count of weighted sum for each aa in the peptide
                weight = 0
                for aa, counts in zip(every_unique_aa, counts_of_every_unique_aa):
                    weight += counts * getattr(row_df, aa)

                    # Creating the features and setting them
                    dataframe.loc[row.Index, 'feat_{}'.format(row_df.Index)] = weight / len(peptide)

    return (dataframe)

#Import Sample Data that has Sample Amino-Acid sequences
df = pd.read_csv('Ov_data.csv', dtype=float)

#df = df.loc[range()] #Making the dataset smaller

print(_calc_aa_descriptors(df))


def calc_csv(dataframe: object, save_folder: str, aa_column: str = 'Info_window_seq', Ncores: int = 1, chunksize: int = None):
    """
    Calculates AA descriptors features for given amino acid sequences chunk by chunk from the inputted 'dataframe'.
    It saves each processed chunk as a CSV(s).

    Results appended as a new columns named feat_{property} e.g. feat_BLOSUM9

    This is a Ram efficient way of calculating the Features as the features are calculated on a single chunk of the dataframe (of
    chunksize number of rows) at a time and when a chunk has been been processed and saved as a CSV, then the chunk
    is deleted freeing up RAM.

    :param dataframe: A pandas DataFrame that contains a column/feature that is composed of purely Amino-Acid sequences (pepides).
    :param save_folder: Path to folder for saving the output.
    :param aa_column: Name of column in dataframe consisting of Amino-Acid sequences to process. Default='Info_window_seq'
    :param Ncores: Number of cores to use. default=1
    :param chunksize: Number of rows to be processed at a time. default=None (Where a 'None' object denotes no chunks but the entire dataframe to be processed)
    """

    utils.calculate_export_csv(dataframe=dataframe, function=_calc_aa_descriptors, Ncores=Ncores,
                               chunksize=chunksize, csv_path_filename=csv_path_filename, aa_column=aa_column)


def calc_df(dataframe: object, Ncores: object = 1, aa_column: object = 'Info_window_seq'):
    """
 Calculates AA descriptors features

    Results appended as a new columns named feat_{property} e.g. feat_BLOSUM9

    :param dataframe: A pandas DataFrame that contains a column/feature that is composed of purely Amino-Acid sequences (pepides).
    :param Ncores: Number of cores to use. default=1
    :param aa_column: Name of column in dataframe consisting of Amino-Acid sequences to process. Default='Info_window_seq'
    :return: Pandas DataFrame

    """


    return utils.calculate_return_df(dataframe=dataframe, function=_calc_aa_descriptors, Ncores=Ncores,
                                     aa_column=aa_column)
