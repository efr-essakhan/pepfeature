"""
    Contains methods to Calculate all features at once if called and have the results returned as a
    DataFrame or stored into CSV

"""

import pepfeature as pep
# from utils import calculate_export_csv, calculate_return_df
import utils
import pandas as pd

def _execute_all_routines(dataframe, k, aa_column='Info_window_seq'):
    """Executes all feature calculation routines in this project
    and combines the returned dataframe into a single dataframe.

    This method is utilized in calc_all_features_csv & calc_all_features_df

    Parameters
    ----------
    dataframe : pandas DataFrame
        The file location of the spreadsheet
    k : int
        A flag used to print the columns to the console (default is False)
    aa_column : str, optional
        A flag used to print the columns to the console (default is False)

    Returns
    -------
    pandas DataFrame

    """
    # Creating a back-up of the original dataframe as later below when the dataframe is passed into df_chunking then
    # the original dataframe has parts deleted as chunks are returned by df_chunking (there is pass by reference in
    # python)
    df_copy = dataframe.copy()

    #Functions that will be run to create the dataframes with features
    functions = [
        pep.aa_descriptors._calc_aa_descriptors,
        pep.aa_composition._calc_aa_composition,
        pep.aa_percentages._calc_aa_percentages,
        pep.aa_cojoint_triads._calc_cojoint_triads,
        pep.aa_molecular_weight._calc_molecular_weight,
        pep.aa_number_of_atoms._calc_number_of_atoms,
        pep.aa_sequence_entropy._calc_sequence_entropy,
        #pep.aa_kmer_composition._calc_kmer_composition
    ]

    df_results_list = []
    for func in functions:

        df_results_list.append(func(df_copy, aa_column))

        #Refresh the Dataset for next use since in python everything is by reference
        df_copy = dataframe.copy()

    # Seperate line for k-mer as it requires extra 'k' argument
    df_results_list.append(pep.aa_kmer_composition._calc_kmer_composition(df_copy, k, aa_column))

    for df in df_results_list:
        #Remove original dataframe columns
        df.drop(dataframe.columns, axis = 1 , inplace=True)

    #Join all df in list into one df
    df_with_features = pd.concat(df_results_list, axis=1)

    # Re-concat both dataframes
    df_with_features = pd.concat([dataframe, df_with_features], axis=1)


    # Re-concat both dataframes to get original DF + calculated DF
    return df_with_features



def calc_csv(dataframe, k, Ncores=4, rows_per_csv=None, csv_path_filename=['', 'result'], aa_column='Info_window_seq'):
    utils.calculate_export_csv(dataframe=dataframe, function=_execute_all_routines, Ncores=Ncores, rows_per_csv=rows_per_csv,
                         csv_path_filename=csv_path_filename, aa_column=aa_column, k=k)


def calc_df(dataframe, k, Ncores=4, aa_column='Info_window_seq'):

    return utils.calculate_return_df(dataframe=dataframe, function=_execute_all_routines, Ncores=Ncores,
                               aa_column=aa_column, k=k)
