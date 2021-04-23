"""
    Contains example use cases for this package
"""

import pandas as pd
import time
import pepfeature as pep

if __name__ == '__main__':
    # For timing purposes
    start = time.time()

    #Import Sample Data that has Sample Amino-Acid sequences to run our calculations on (download from github: pepfeature/data/Sample_Data.csv)

    df = pd.read_csv('pepfeature/data/Sample_Data.csv')


    #Example Use cases: ##########################################
    # Make sure to: Uncomment what line you want to test from below & Set save_folder arguments to correct path of your choice (tip: use "" <- to for save_Folder variable to save in working directory)

    savefolder =r"C:\Users\xbox_\Documents\Pepfeature DS"

    '''Calculate all features at once'''
    #As CSV
    # pep.aa_all_feat.calc_csv(dataframe=df, save_folder=savefolder,aa_column='Info_window_seq'
    #                                  ,Ncores=4,chunksize=None, k=2)

    # #As DF
    # pep.aa_all_feat.calc_df(dataframe=df, aa_column='Info_window_seq', Ncores=4, k=2)



    '''Calculate features individually and output result as CSV'''
    # pep.aa_molecular_weight.calc_csv(dataframe=df, save_folder=savefolder, aa_column='Info_window_seq'
    #                                  ,Ncores=4,chunksize=None)

    # pep.aa_seq_entropy.calc_csv(dataframe=df, save_folder=savefolder,
    #                                  aa_column='Info_window_seq'
    #                                  , Ncores=4, chunksize=None)
    #
    # pep.aa_num_of_atoms.calc_csv(dataframe=df, save_folder=savefolder,
    #                             aa_column='Info_window_seq'
    #                             , Ncores=4, chunksize=None)
    #
    # pep.aa_descriptors.calc_csv(dataframe=df, save_folder=savefolder,
    #                             aa_column='Info_window_seq'
    #                             , Ncores=4, chunksize=None)
    #
    # pep.aa_composition.calc_csv(dataframe=df, save_folder=savefolder,
    #                             aa_column='Info_window_seq'
    #                             , Ncores=4, chunksize=None)
    #
    # pep.aa_proportion.calc_csv(dataframe=df, save_folder=savefolder,
    #                             aa_column='Info_window_seq'
    #                             , Ncores=4, chunksize=None)
    #
    # pep.aa_CT.calc_csv(dataframe=df, save_folder=savefolder,
    #                             aa_column='Info_window_seq'
    #                             , Ncores=4, chunksize=None)
    #
    # pep.aa_kmer_composition.calc_csv(dataframe=df, save_folder=savefolder,
    #                             aa_column='Info_window_seq'
    #                             , Ncores=4, chunksize=None, k=2)


    '''Calculate features individually and output results as pandas DF'''
    # print(pep.aa_molecular_weight.calc_df(dataframe=df, Ncores=4, aa_column='Info_window_seq'))
    # print(pep.aa_seq_entropy.calc_df(dataframe=df, Ncores=4, aa_column='Info_window_seq'))
    # print(pep.aa_num_of_atoms.calc_df(dataframe=df, Ncores=4, aa_column='Info_window_seq'))
    # print(pep.aa_descriptors.calc_df(dataframe=df, Ncores=4, aa_column='Info_window_seq'))
    # print(pep.aa_composition.calc_df(dataframe=df, Ncores=4, aa_column='Info_window_seq'))
    # print(pep.aa_proportion.calc_df(dataframe=df, Ncores=4, aa_column='Info_window_seq'))
    # print(pep.aa_CT.calc_df(dataframe=df, Ncores=4))
    # print(pep.aa_kmer_composition.calc_df(k=2, dataframe=df, Ncores=4, aa_column='Info_window_seq'))

    print(f'time taken: {time.time() - start}')