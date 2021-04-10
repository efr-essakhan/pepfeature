"""
    Contains example use cases of this library.
"""

import pandas as pd
import time
import pepfeature as pep

# df = pd.DataFrame(data={ 'Info_window_seq': ['CCAKJATJXARRRZS'], 'yolo': ['CCAKJATJXARRRZS'], 'Info_window_seq': ['CCAKJAdJXARRRZS']})
#
# #For testing purposes of the functions in this file
# def dummydataframe(rows):
#
#     dc = pd.DataFrame(np.random.randint(0, 100, size=(rows, 12))) #8500 total features from methods
#     dc['Info_window_seq'] = "LLLLLLLLDVHIESG"
#
#     return (dc)
from pepfeature import all_features

if __name__ == '__main__':

    start = time.time()  # For timing purposes

    df = pd.read_csv('example_peptide_data.csv')
    #print(df.loc[range(2)].to_dict('series'))
    pep.all_features.calc_df(dataframe=df.loc[range(200)], k=1, Ncores=2)



    ##############            Example Use Cases                 ###############


    """Calculate all features and store result into CSV"""
    #pep.all_features.calc_csv(dataframe=df.loc[range(1000)], k=1, Ncores=4, chunksize=200)
    #print(pep.all_features.calc_df(dataframe=df.loc[range(10)], k=1, Ncores=4, chunksize=2))

    #print(pep.aa_percentages.calculate_df(Ncores=1, dataframe=df.loc[range(1)], chunksize=2, aa_column="Info_window_seq"))


    print(f'time taken: {time.time() - start}')

