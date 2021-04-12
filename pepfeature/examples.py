"""
    Contains example use cases of this library.
"""

import pandas as pd
import time
import pepfeature as pep
import numpy as np

def dummydataframe(rows):

    dc = pd.DataFrame(np.random.randint(0, 100, size=(rows, 12))) #8500 total features from methods
    dc['Info_window_seq'] = "LLLLLLLLDVHIESG"

    return (dc)

if __name__ == '__main__':
    # For timing purposes
    start = time.time()

    #Import Sample Data that has Sample Amino-Acid sequences
    df = pd.read_csv('Ov_data.csv')

    #df = df.loc[range()] #Making the dataset smaller

    print(pep.aa_descriptors._calc_aa_descriptors(df))

    '''Calculate All features at once'''

    #Calculate all features and store result as csv
    # pep.all_features.calc_csv(dataframe=df, k=1,chunksize=50, Ncores=4, save_folder=r'C:\Users\xbox_\Documents\Pepfeature DS', aa_column='Info_window_seq')

    #Calculate all features and return result as DataFrame
    #print(pep.all_features.calc_df(dataframe=df, k=1,Ncores=4, aa_column='Info_window_seq'))

<<<<<<< HEAD
=======
    df = pd.read_csv('example_peptide_data.csv')
    #print(df.loc[range(2)].to_dict('series'))
    #pep.all_features.calc_df(dataframe=df.loc[range(100)], k=1, Ncores=2)
    pep.all_features.calc_csv(dataframe=df.loc[range(100)], k=2, Ncores=4)
    #yolo = pep.all_features.calc_df(dataframe=df.loc[range(15)], k=1, Ncores=2)
    #print(yolo)
    #print(pep.aa_cojoint_triads._calc_cojoint_triads(df.loc[range(5)]))
>>>>>>> parent of 6905cbe (created test)




    ##############            Example Use Cases                 ###############


    """Calculate all features and store result into CSV"""
    #pep.all_features.calc_csv(dataframe=df.loc[range(1000)], k=1, Ncores=4, chunksize=200)
    #print(pep.all_features.calc_df(dataframe=df.loc[range(10)], k=1, Ncores=4, chunksize=2))

    #print(pep.aa_percentages.calculate_df(Ncores=1, dataframe=df.loc[range(1)], chunksize=2, aa_column="Info_window_seq"))


    print(f'time taken: {time.time() - start}')

