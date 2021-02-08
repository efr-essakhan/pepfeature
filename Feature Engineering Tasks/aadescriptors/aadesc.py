import pandas as pd
import numpy as np
import time

pd.set_option("display.max_columns", None)

df = pd.read_csv('Ov_data.csv')


def aadesc(dataframe):
    # Dictionary mapping each Amino-Acid to its respective group-value

    AA_properties_df_dict = {}
    properties = ['crucianiProperties', 'kideraFactors', 'zScales', 'FASGAI', 'VHSE', 'ProtFP', 'stScales', 'tScales', 'MSWHIM', 'BLOSUM']
    for sheet in properties:
        AA_properties_df_dict[sheet] = pd.read_excel('AAdescriptors.xls', sheet, index=0, header=0)

    for row in dataframe.itertuples():

        peptide = list(row.Info_window_seq)

        every_unique_aa, counts_of_every_unique_aa = np.unique(peptide, return_counts=True)
        peptide_info = dict(zip(every_unique_aa, counts_of_every_unique_aa))

        for property, df in AA_properties_df_dict.items():
            for row_df in df.iterrows():
                # Variables for each atom, to keep count of weighted sum for each aa in the peptide
                weight = 0
                for aa, counts in peptide_info.items():
                    print(row_df[aa])
                    weight += counts * row_df[aa]

                    # Creating the features and setting them
                    dataframe.loc[row.Index, 'feat_{}'.format(row_df.header)] = weight/len(peptide)

start_time = time.time()
print(aadesc(df.loc[range(1)]))
print("--- %s seconds ---" % (time.time() - start_time))