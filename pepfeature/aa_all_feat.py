"""
    This module contains methods to Calculate all features at once either returned as a DataFrame or stored into CSV.

    Methods user can call from this module:
        calc_csv,
        calc_df
"""

from pepfeature import _utils
import pepfeature as pep
import pandas as pd

def _algorithm(dataframe: object, k: int, aa_column: str = 'Info_window_seq') -> object:
    """
    Not intended to be called directly by the user, use the functions calc_csv or calc_df instead as they have
    multi-processing functionality and more.

    Executes all feature calculation routines in this project
    and combines the returned dataframes into a single dataframe which is returned by this function.

    This method is utilized in calc_all_features_csv & calc_all_features_df

    :param dataframe: A pandas DataFrame.
    :param aa_column: Name of column in dataframe consisting of Protein Sequences to process. Default='Info_window_seq'
    :return: A Pandas DataFrame containing the calculated features appended as new columns.
    """

    # Creating a back-up of the original dataframe as later below when the dataframe is passed into df_chunking then
    # the original dataframe has parts deleted as chunks are returned by df_chunking (there is pass by reference in
    # python)
    df_copy = dataframe.copy()

    # #Functions that will be run to create the dataframes with features
    # functions = [
    #     pep.aa_seq_entropy._algorithm,
    #     pep.aa_num_of_atoms._algorithm,
    #     pep.aa_molecular_weight._algorithm,
    #     pep.aa_composition._algorithm,
    #     pep.aa_descriptors._algorithm,
    #     pep.aa_CT._algorithm,
    #     pep.aa_proportion._algorithm,
    #     #pep.aa_kmer_composition._calc_kmer_composition #This one requires different arguments so will have to deal with it seperatly
    # ]

    #Functions that will be run to create the dataframes with features
    functions = [
        pep.aa_seq_entropy.calc_df,
        pep.aa_num_of_atoms.calc_df,
        pep.aa_molecular_weight.calc_df,
        pep.aa_composition.calc_df,
        pep.aa_descriptors.calc_df,
        pep.aa_CT.calc_df,
        pep.aa_proportion.calc_df,
        #pep.aa_proportion.calc_df #This one requires different arguments so will have to deal with it seperatly
    ]

    df_results_list = []
    for func in functions:

        df_results_list.append(func(df_copy, 1, aa_column)) #execute each function and store its result into a df

        #Refresh the Dataset for next use since in python everything is by reference
        df_copy = dataframe.copy()

    # Seperate line for k-mer as it requires extra 'k' argument
    df_results_list.append(pep.aa_kmer_composition.calc_df(dataframe=df_copy, Ncores=1, k=k, aa_column=aa_column))

    for df in df_results_list:
        #Remove original dataframe columns
        df.drop(dataframe.columns, axis = 1 , inplace=True)

    #Join all df in list into one df
    df_with_features = pd.concat(df_results_list, axis=1)

    # Re-concat both dataframes
    df_with_features = pd.concat([dataframe, df_with_features], axis=1)

    # Re-concat both dataframes to get original DF + calculated DF
    return df_with_features


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
    _utils.calculate_export_csv(dataframe=dataframe, function=_algorithm, Ncores=Ncores,
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

    return _utils.calculate_return_df(dataframe=dataframe, function=_algorithm, Ncores=Ncores,
                                      aa_column=aa_column, k=k)
