"""
    Contains example use cases for this package.
"""

import pandas as pd
import time
import pepfeature as pep

if __name__ == '__main__':
    # For timing purposes
    start = time.time()

    #Import Sample Data that has Sample Amino-Acid sequences to run our calculations on (download from github: pepfeature/data/Sample_Data.csv)
    df = pd.read_csv('pepfeature/data/Sample_Data.csv') #adjust path to point towards Sample_Data.csv

    # ########################################## Example Use cases: ##########################################
    # INSTURCTIONS: Uncomment what line you want to test from below & Set Ncores arugment appropiately & save_folder arguments to correct path of your choice (tip: use "" <- for save_Folder variable to save in working directory)

    savefolder =r""
    Ncores = 4 #Num. of cores to use for multiprocessing.

    '''Calculate all features at once'''
    #As CSV
    # pep.aa_all_feat.calc_csv(dataframe=df, save_folder=savefolder,aa_column='Info_window_seq'
    #                                  ,Ncores=Ncores,chunksize=None, k=2)

    # #As DF
    # pep.aa_all_feat.calc_df(dataframe=df, aa_column='Info_window_seq', Ncores=Ncores, k=2)



    '''Calculate features individually and output result as CSV'''
    # pep.aa_molecular_weight.calc_csv(dataframe=df, save_folder=savefolder, aa_column='Info_window_seq'
    #                                  ,Ncores=Ncores,chunksize=30)

    # pep.aa_seq_entropy.calc_csv(dataframe=df, save_folder=savefolder,
    #                                  aa_column='Info_window_seq'
    #                                  , Ncores=Ncores, chunksize=None)
    #
    # pep.aa_num_of_atoms.calc_csv(dataframe=df, save_folder=savefolder,
    #                             aa_column='Info_window_seq'
    #                             , Ncores=Ncores, chunksize=None)
    #
    # pep.aa_descriptors.calc_csv(dataframe=df, save_folder=savefolder,
    #                             aa_column='Info_window_seq'
    #                             , Ncores=Ncores, chunksize=None)
    #
    # pep.aa_composition.calc_csv(dataframe=df, save_folder=savefolder,
    #                             aa_column='Info_window_seq'
    #                             , Ncores=Ncores, chunksize=None)
    #
    # pep.aa_proportion.calc_csv(dataframe=df, save_folder=savefolder,
    #                             aa_column='Info_window_seq'
    #                             , Ncores=Ncores, chunksize=None)
    #
    # pep.aa_CT.calc_csv(dataframe=df, save_folder=savefolder,
    #                             aa_column='Info_window_seq'
    #                             , Ncores=Ncores, chunksize=None)
    #
    # pep.aa_kmer_composition.calc_csv(dataframe=df, save_folder=savefolder,
    #                             aa_column='Info_window_seq'
    #                             , Ncores=Ncores, chunksize=None, k=2)

    '''Calculate all features and output result as CSV in chunks'''
    # pep.aa_all_feat.calc_csv(dataframe=df, save_folder=savefolder,aa_column='Info_window_seq'
    #                                  ,Ncores=Ncores,chunksize=20, k=2)


    '''Calculate features individually and output results as pandas DF'''
    # print(pep.aa_molecular_weight.calc_df(dataframe=df, Ncores=Ncores, aa_column='Info_window_seq'))
    # print(pep.aa_seq_entropy.calc_df(dataframe=df, Ncores=Ncores, aa_column='Info_window_seq'))
    # print(pep.aa_num_of_atoms.calc_df(dataframe=df, Ncores=Ncores, aa_column='Info_window_seq'))
    # print(pep.aa_descriptors.calc_df(dataframe=df, Ncores=Ncores, aa_column='Info_window_seq'))
    # print(pep.aa_composition.calc_df(dataframe=df, Ncores=Ncores, aa_column='Info_window_seq'))
    # print(pep.aa_proportion.calc_df(dataframe=df, Ncores=Ncores, aa_column='Info_window_seq'))
    # print(pep.aa_CT.calc_df(dataframe=df, Ncores=Ncores))
    # print(pep.aa_kmer_composition.calc_df(k=2, dataframe=df, Ncores=Ncores, aa_column='Info_window_seq'))

    print(f'time taken: {time.time() - start}')


